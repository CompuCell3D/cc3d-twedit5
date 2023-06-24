"""
Twedit5 CLI
"""

from os import environ
import platform
import getopt
from cc3d.twedit5.twedit.utils.global_imports import *
from cc3d.twedit5.twedit.CQt.CQApplication import CQApplication
from cc3d.twedit5.EditorWindow import EditorWindow
from cc3d.twedit5.DataSocketCommunicators import FileNameSender
from cc3d.twedit5.logger import get_logger
import sys
from cc3d.twedit5.windowsUtils import *
from cc3d.twedit5.Messaging import dbgMsg, setDebugging
import argparse

log = get_logger(__name__)

# this globally enables/disables debug statements
setDebugging(0)

if sys.platform.startswith('win'):
    # this takes care of the need to distribute qwindows.dll with the qt5 application
    # it needs to be located in the directory <library_path>/platforms

    QCoreApplication.addLibraryPath("./bin/")

# instaling message handler to suppres spurious qt messages
if sys.platform == 'darwin':
    mac_ver = platform.mac_ver()
    mac_ver_float = float('.'.join(mac_ver[0].split('.')[:2]))

    if mac_ver_float == 10.11:
        def handler(msg_type, msg_log_context, msg_string=None):

            if msg_log_context.startswith('QCocoaView handleTabletEvent'):
                return

            print(msg_log_context)

    elif mac_ver_float == 10.10:
        def handler(msg_type, msg_log_context, msg_string=None):
            if msg_log_context.startswith('Qt: qfontForThemeFont:'):
                return

            print(msg_log_context)



class Twedit(object):

    def __init__(self):

        self.fileList = []

    def getFileList(self):
        return self.fileList

    def process_cml(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--port', type=int, help='Listening port number')
        # parser.add_argument('-s', '--socket', type=int, help='Listening socket')

        # Parse the arguments
        parsed_args, input_files = parser.parse_known_args(args)


        return parsed_args, input_files

    def process_command_line_options(self):
        log.debug("TWEDIT++ process_command_line_options\n\n\n\n")
        # print("TWEDIT++ process_command_line_options\n\n\n\n")
        args, self.fileList = self.process_cml(args=sys.argv[1:])

        print(args)
        log.debug(f"input_files={self.fileList}")
        # print("input_files=", self.fileList)


    def main(self, argv):

        app = CQApplication(argv)

        QApplication.setWindowIcon(QIcon(':/icons/twedit-icon.png'))

        qt_version = str(QT_VERSION_STR).split('.')

        if platform.mac_ver()[0] != '' and int(qt_version[1]) >= 2:  # style sheets may not work properly for qt < 4.2

            app.setStyleSheet("QDockWidget::close-button, QDockWidget::float-button { padding: 0px;icon-size: 24px;}")

        pixmap = QPixmap("icons/lizard-at-a-computer-small.png")

        log.debug(f"pixmap={pixmap}")
        # print("pixmap=", pixmap)

        splash = QSplashScreen(pixmap)

        splash.showMessage("Please wait.\nLoading Twedit++5 ...", Qt.AlignLeft, Qt.black)

        splash.show()

        app.processEvents()

        # app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

        self.mainWindow = EditorWindow(False)

        self.mainWindow.setArgv(argv)  # passing command line to the code

        self.mainWindow.show()

        splash.finish(self.mainWindow)

        # self.mainWindow.processCommandLine()

        self.mainWindow.openFileList(self.fileList)

        self.mainWindow.raise_()  # to make sure on OSX window is in the foreground

        if sys.platform.startswith('win'):
            import win32process
            self.mainWindow.setProcessId(win32process.GetCurrentProcessId())
            # showTweditWindowInForeground()

        app.exec_()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    sys.exit(1)


def main(argv=None):

    if argv is None:
        argv = []

    try:

        twedit = Twedit()

        twedit.process_command_line_options()

    except OSError as e:
        log.error("GOT OS ERROR")
        # dbgMsg("GOT OS ERROR")

        # argvSendSocket=QUdpSocket()

        fileList = twedit.getFileList()

        print("\n\n\n\n FILE LIST=", fileList)

        for fileName in fileList:
            datagram = fileName

            # argvSendSocket.writeDatagram(datagram,QHostAddress.LocalHost,47405)

            fileSender = FileNameSender(datagram)

            fileSender.send()

        if sys.platform == 'win32':

            showTweditWindowInForeground()

        else:

            # notice, on linux you may have to change "focus stealing prevention level" setting to None in
            # window behavior settings , to enable bringing window to foreground
            log.info("NON-WINDOWS PLATFORM - TRY TO ACTIVATE WINDOW")
            # dbgMsg("NON-WINDOWS PLATFORM - TRY TO ACTIVATE WINDOW")

    twedit.main(argv)


if __name__ == '__main__':

    # enable it during debugging in pycharm
    sys.excepthook = except_hook

    main(sys.argv[1:])
