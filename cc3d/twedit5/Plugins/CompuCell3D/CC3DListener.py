"""
todo fix Socket - rewrite signals to use qt5 style
"""

SIZEOF_UINT16 = 2
from cc3d.twedit5.twedit.utils.global_imports import *
from cc3d.twedit5.windowsUtils import *
import getopt
import sys
# this class runs inside Qt event loop we can use slots and signals to handle communication
from cc3d.twedit5.Messaging import dbgMsg
from cc3d.twedit5.Plugins import installed_player
from subprocess import Popen


class Socket(QTcpSocket):
    def __init__(self, parent=None):

        super(Socket, self).__init__(parent)

        self.editorWindow = parent.editorWindow

        self.listener = parent

        self.readyRead.connect(self.readRequest)

        self.disconnected.connect(self.listener.maybeCloseEditor)

        self.disconnected.connect(self.deleteLater)

        self.nextBlockSize = 0

        self.line = 0

        self.col = 0

        self.errorLine = -1

    def disconnectDisconnectedSignal(self):

        self.disconnected.disconnect(self.listener.maybeCloseEditor)

    def connectDisconnectedSignal(self):

        self.disconnected.connect(self.listener.maybeCloseEditor)

    def disconnectReadyReadSignal(self):

        self.readyRead.disconnect(self.readRequest)

    def readRequest(self):

        dbgMsg("INSIDE READ REQUEST")

        stream = QDataStream(self)

        stream.setVersion(QDataStream.Qt_5_2)

        dbgMsg("BYTES AVAILABLE:", self.bytesAvailable())

        if self.nextBlockSize == 0:

            if self.bytesAvailable() < SIZEOF_UINT16:
                return

        self.nextBlockSize = stream.readUInt16()

        if self.bytesAvailable() < self.nextBlockSize:
            return

        action = stream.readQString()

        dbgMsg("ACTION=", action)

        if str(action) in ("FILEOPEN"):

            fileName = stream.readQString()

            line = stream.readUInt16()

            col = stream.readUInt16()

            self.editorWindow.loadFile(str(fileName))

            currentEditor = self.editorWindow.getCurrentEditor()

            currentEditor.setCursorPosition(line - 1, 0)

            dbgMsg(
                "THIS IS FILENAME READ FROM CLIENT=",
                str(fileName),
                " line=",
                line,
                " col=",
                col,
            )

            dbgMsg("currentEditor=", " line=", line, " col=", col)

            self.setCurrentLineBackgroundColor(currentEditor)

            self.line = line - 1

            self.col = 0

            # bring up the window

            if sys.platform.startswith("win"):
                print("calling script")
                # aparently

                # showTweditWindowInForeground() will not work because we are
                # trying to set current window in the foreground using win32Api
                # doing the same from separate process works fine
                # have to construct full path from env vars
                # have to get python path here as well
                # from subprocess import Popen
                # p = Popen(["python", self.bringupTweditPath,str(self.editorWindow.getProcessId())])

            else:

                self.editorWindow.showNormal()
                self.editorWindow.activateWindow()
                self.editorWindow.raise_()
                self.editorWindow.setFocus(True)

        elif str(action) in ("NEWCONNECTION"):

            print("\n\n\n \t\t\t NEW CONNECTION")

            self.sendEditorOpen()

            # self.sendEditorClosed()

            self.flush()

        elif str(action) in ("CONNECTIONESTABLISHED"):

            print("CONNECTION ESTABLISHED - LISTENER ACKNOWLEDGED")

            self.flush()

        elif str(action) in ("NEWSIMULATIONRECEIVED"):
            print("NEWSIMULATIONRECEIVED SIMULATION NAME SENT SUCCESFULLY")
            self.flush()

    def setCurrentLineBackgroundColor(self, currentEditor):

        print("SETTING CARET LINE BACKGROUND")

        print("position=", currentEditor.getCursorPosition())

        line, col = currentEditor.getCursorPosition()

        lineLen = currentEditor.lineLength(line)

        currentEditor.setCaretLineVisible(True)

        currentEditor.setCaretLineBackgroundColor(
            QColor("#FE2E2E")
        )  # current line has this color

        currentEditor.setCaretLineVisible(True)

        currentEditor.hide()

        currentEditor.show()

        errorBookmark = (
            self.editorWindow.lineBookmark
        )  # All editors tab share same markers

        currentEditor.setMarkerBackgroundColor(QColor("red"), errorBookmark)

        self.errorLine = line

        marker = currentEditor.markerAdd(self.errorLine, errorBookmark)

        print(
            "currentEditor.markersAtLine(self.errorLine)=",
            currentEditor.markersAtLine(self.errorLine),
        )

        # print self.errorLine

        currentEditor.cursorPositionChanged.connect(self.cursorPositionChangedHandler)

    def cursorPositionChangedHandler(self, line, col):

        print("\n\n\n\n\n\n\n ERROR LINE: ", self.errorLine)

        if line != self.line or col != self.col:

            for editor in self.editorWindow.getEditorList():

                try:  # in case signal is not connected exception is thrown - we simply ignore it

                    # restoring original styling for the editor
                    self.editorWindow.setEditorProperties(
                        editor
                    )

                    editor.markerDelete(self.errorLine)

                    editor.cursorPositionChanged.disconnect(
                        self.cursorPositionChangedHandler
                    )

                    self.errorLine = -1
                except:

                    pass

    # IMPORTANT: whenever you send message composed of e.g. int, Qstring, Qstring,
    # int  you have to read all of these items otherwise socket state will be corrupted
    # and result in undefined behavior during subsequent reads

    def sendError(self, msg):

        reply = QByteArray()

        stream = QDataStream(reply, QIODevice.WriteOnly)

        stream.setVersion(QDataStream.Qt_5_2)

        stream.writeUInt16(0)

        stream.writeQString("ERROR")

        stream.writeQString(msg)

        stream.device().seek(0)

        stream.writeUInt16(reply.size() - SIZEOF_UINT16)

        self.write(reply)

    def sendEditorClosed(self):

        reply = QByteArray()

        stream = QDataStream(reply, QIODevice.WriteOnly)

        stream.setVersion(QDataStream.Qt_5_2)

        stream.writeUInt16(0)

        stream.writeQString("EDITORCLOSED")

        stream.device().seek(0)

        print("EDITOR CLOSED SIGNAL SIZE=", reply.size() - SIZEOF_UINT16)

        stream.writeUInt16(reply.size() - SIZEOF_UINT16)

        print("EDITOR CLOSED reply=", reply)

        self.write(reply)

    def sendEditorOpen(self):

        reply = QByteArray()

        stream = QDataStream(reply, QIODevice.WriteOnly)

        stream.setVersion(QDataStream.Qt_5_2)

        stream.writeUInt16(0)

        stream.writeQString("EDITOROPEN")

        stream.writeUInt16(self.editorWindow.getProcessId())

        stream.device().seek(0)

        stream.writeUInt16(reply.size() - SIZEOF_UINT16)

        self.write(reply)

    def sendNewSimulation(self, _simulationName=""):

        reply = QByteArray()

        stream = QDataStream(reply, QIODevice.WriteOnly)

        stream.setVersion(QDataStream.Qt_5_2)

        stream.writeUInt16(0)

        stream.writeQString("NEWSIMULATION")

        stream.writeQString(_simulationName)

        stream.device().seek(0)

        print("NEW SIMULATION reply=", reply)

        stream.writeUInt16(reply.size() - SIZEOF_UINT16)

        self.write(reply)

    def sendReply(self, action, room, date):

        reply = QByteArray()

        stream = QDataStream(reply, QIODevice.WriteOnly)

        stream.setVersion(QDataStream.Qt_5_2)

        stream.writeUInt16(0)

        stream << action << room << date

        stream.device().seek(0)

        stream.writeUInt16(reply.size() - SIZEOF_UINT16)

        self.write(reply)


class CC3DListener(QTcpServer):
    newlyReadFileName = QtCore.pyqtSignal(("char*",))

    def __init__(self, parent=None):

        super(CC3DListener, self).__init__(parent)

        self.editorWindow = parent

        # initial port - might be reassigned by calling program - vial --port=... command line option
        self.port = (-1)

        self.socketId = -1

        self.port, self.socketId = self.getPortFromCommandLine()

        dbgMsg("PORT=", self.port)

        print("PORT=", self.port)

        self.clientSocket = None

        # on some linux distros QHostAddress.LocalHost does not work

        # if not self.tcpServer.listen(QHostAddress.LocalHost,47405):

        dbgMsg("\n\n\n LISTENING ON PORT ", self.port)

        self.nextBlockSize = 0

        self.socket = None

        self.socketSender = None

        self.nextBlockSize = 0

        self.pluginObj = None

        self.cc3dProcess = None

        if self.port > 0 and not self.listen(QHostAddress("127.0.0.1"), self.port):
            QMessageBox.critical(
                None,
                "FileNameReceiver",
                "CONSTRUCTOR Unable to start the server: %s." % str(self.errorString()),
            )

            return

    def setPluginObject(self, plugin):

        self.pluginObj = plugin

    def maybeCloseEditor(self):

        if self.socket:
            self.socket.disconnectDisconnectedSignal()

            print("CLOSING LOCAL SOCKET")

            self.socket.disconnectFromHost()
            self.socket = None

        if self.pluginObj:
            self.pluginObj.enableStartCC3DAction(True)

    def startServer(self):

        port = self.getOpenPort()

        if self.port > 0 and not self.listen(QHostAddress("127.0.0.1"), self.port):

            ret = QMessageBox.critical(
                None,
                "FileNameReceiver",
                "STARTSERVER Unable to start the server: %s." % str(self.errorString()),
            )

            if ret == QMessageBox.Ok:
                print("\n\n\n START SERVER: SERVER STARTED")

        return port

    def getOpenPort(self):

        print("TRY TO FIGURE OUT PORT\n\n\n\n\n\n")

        for port in range(47406, 47506):

            print("CHECKING PORT=", port)

            tcp_server = QTcpServer(self)

            if tcp_server.listen(QHostAddress("127.0.0.1"), port):
                self.port = port

                tcp_server.close()

                print("established empty port=", self.port)

                break

        return self.port

    def startCC3D(self, _simulationName=""):
        if not installed_player:
            print("Player not found!")
            return

        popen_args = [sys.executable, "-m", "cc3d.player5", f"--port={self.port}" ]

        if _simulationName != "":
            popen_args.append("-i")

            popen_args.append(_simulationName)
            # starting cc3d in stepping mode
            popen_args.append("--run-action")
            popen_args.append("step")



        print("Executing Popen command with following arguments=", popen_args)

        self.cc3dProcess = Popen(popen_args)

    def getPortFromCommandLine(self):

        try:

            opts, args = getopt.getopt(sys.argv[1:], "p", ["file=", "port=", "socket="])

            dbgMsg("opts=", opts)

            dbgMsg("args=", args)

        except getopt.GetoptError as err:

            dbgMsg(str(err))  # will print something like "option -a not recognized")

            sys.exit(2)

        port = -1

        socket_id = 1

        for o, a in opts:

            dbgMsg("o=", o)

            dbgMsg("a=", a)

            if o in ("--port"):
                port = a

                dbgMsg("THIS IS PORT=", port)

            if o in ("--socket"):
                socket_id = a

                dbgMsg("THIS IS SOCKET=", socket_id)

            if o in ("--file"):
                file = a

                dbgMsg("THIS IS file=", file)

        return int(port), int(socket_id)

    def incomingConnection(self, socketId):

        dbgMsg("GOT INCOMMING CONNECTION self.socket=", self.socket)

        self.socket = Socket(self)

        self.socket.setSocketDescriptor(socketId)

        # once we get connection we disable start CC3D action on the tool bar to
        # prevent additional copies of CC3D being open

        if self.pluginObj:
            self.pluginObj.enableStartCC3DAction(False)

        dbgMsg("\n\n\n\n\n socket ID = ", socketId)

    def deactivate(self):

        if self.socket:
            self.socket.disconnectDisconnectedSignal()

        self.close()

        self.getOpenPort()
        if self.socket and self.socket.state() == QAbstractSocket.ConnectedState:
            print("SENDING EDITOR CLOSED SIGNAL")

            self.socket.sendEditorClosed()

            self.socket.waitForReadyRead(3000)

        self.close()
