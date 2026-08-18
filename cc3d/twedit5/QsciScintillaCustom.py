from math import log
from cc3d.twedit5.twedit.utils.global_imports import *
import cc3d.twedit5.twedit.ActionManager as am


# have to implement custom class for QSciScintilla to handle properly wheel even with and without ctrl pressed

class QsciScintillaCustom(QsciScintilla):

    AUTO_PAIR_CHARS = {
        "'": "'",
        '"': '"',
        "(": ")",
        "[": "]",
        "{": "}"
    }

    def __init__(self, parent=None, _panel=None):

        super(QsciScintillaCustom, self).__init__(parent)

        self.editorWindow = parent
        try:
            self.line_numbers_enabled = self.editorWindow.configuration.setting('DisplayLineNumbers')
        except AttributeError:
            self.line_numbers_enabled = False

        self.panel = _panel

        self.mousePressEventOrig = self.mousePressEvent

        self.CtrlKeyEquivalent = Qt.Key_Control

        self.scintillaDefinedLetterShortcuts = [ord('D'), ord('L'), ord('T'), ord('U'), ord('/'), ord(']')]

        self.customContextMenu = None

        self.linesChanged.connect(self.linesChangedHandler)

        if sys.platform.startswith("darwin"):
            self.CtrlKeyEquivalent = Qt.Key_Alt

    def wheelEvent(self, event):

        if qApp.keyboardModifiers() == Qt.ControlModifier:
            # Forwarding wheel event to editor windowwheelEvent

            event.ignore()

        else:
            # # calling wheelEvent from base class - regular scrolling
            super(QsciScintillaCustom, self).wheelEvent(event)

    def handleScintillaDefaultShortcut(self, modifierKeysText, event):

        if event.key() in self.scintillaDefinedLetterShortcuts:

            try:

                action = am.actionDict[am.shortcutToActionDict[modifierKeysText + '+' + chr(event.key())]]
                action.trigger()
                event.accept()
            except LookupError:
                super(QsciScintillaCustom, self).keyPressEvent(event)

        else:

            super(QsciScintillaCustom, self).keyPressEvent(event)

    def registerCustomContextMenu(self, _menu):

        self.customContextMenu = _menu

    def unregisterCustomContextMenu(self):

        self.customContextMenu = None

    def contextMenuEvent(self, _event):

        if not self.customContextMenu:

            super(QsciScintillaCustom, self).contextMenuEvent(_event)

        else:

            self.customContextMenu.exec_(_event.globalPos())

    def keyPressEvent(self, event):
        """
            senses if scintilla predefined keyboard shortcut was pressed.
        """

        if event.modifiers() == Qt.ControlModifier:
            self.handleScintillaDefaultShortcut('Ctrl', event)

        elif event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            self.handleScintillaDefaultShortcut('Ctrl+Shift', event)

        elif self.handle_auto_pair_characters(event):
            event.accept()

        else:
            super(QsciScintillaCustom, self).keyPressEvent(event)

    def handle_auto_pair_characters(self, event):
        """
        Inserts matching closing characters or wraps selected text when enabled.

        :param event: keyboard event
        :return: True when this method handled the event
        """
        typed_text = event.text()
        if len(typed_text) != 1:
            return False

        if not self.__auto_pair_characters_enabled():
            return False

        if event.modifiers() & (Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier):
            return False

        if typed_text in self.AUTO_PAIR_CHARS:
            self.__insert_auto_pair(typed_text, self.AUTO_PAIR_CHARS[typed_text])
            return True

        if typed_text in self.AUTO_PAIR_CHARS.values() and self.__current_char() == typed_text:
            line, index = self.getCursorPosition()
            self.setCursorPosition(line, index + 1)
            return True

        return False

    def __auto_pair_characters_enabled(self):
        try:
            return self.editorWindow.configuration.setting("AutoPairCharacters")
        except AttributeError:
            return True

    def __insert_auto_pair(self, opening_char, closing_char):
        if self.hasSelectedText():
            selected_text = self.selectedText()
            self.beginUndoAction()
            self.replaceSelectedText(opening_char + selected_text + closing_char)
            self.endUndoAction()
            return

        line, index = self.getCursorPosition()
        self.beginUndoAction()
        self.insert(opening_char + closing_char)
        self.endUndoAction()
        self.setCursorPosition(line, index + 1)

    def __current_char(self):
        line, index = self.getCursorPosition()
        line_text = self.text(line)
        if index < len(line_text):
            return line_text[index]

        return ''

    def focusInEvent(self, event):
        editor_tab = 0

        if self.panel == self.editorWindow.panels[1]:
            editor_tab = 1

        self.editorWindow.activeTabWidget = self.panel

        self.editorWindow.handleNewFocusEditor(self)

        super(self.__class__, self).focusInEvent(event)


    def linesChangedHandler(self):
        '''
            adjusting width of the line number margin
        '''

        if not self.line_numbers_enabled:
            return

        if self.marginLineNumbers(0):

            number_of_lines = self.lines()
            number_of_digits = int(log(number_of_lines, 10)) + 2 if number_of_lines > 0 else 2
            self.setMarginWidth(0, '0' * number_of_digits)
