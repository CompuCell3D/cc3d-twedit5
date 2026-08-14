from cc3d.twedit5.twedit.utils.global_imports import *


class SnippetPreviewPopup(QFrame):

    MAX_VISIBLE_LINES = 18
    TRUNCATION_MARKER = "\n..."

    def __init__(self, editor_window=None, fallback_lexer_cls=None):
        super().__init__(None, Qt.ToolTip | Qt.FramelessWindowHint)

        self.editor_window = editor_window
        self.fallback_lexer_cls = fallback_lexer_cls or QsciLexerCPP
        self.previewLexer = None

        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setObjectName("snippetPreviewPopup")
        self.setWindowOpacity(0.97)
        self.setStyleSheet("""
            QFrame#snippetPreviewPopup {
                background: #faf8f3;
                border: 1px solid #cfc7b8;
                border-radius: 8px;
            }
            QLabel#snippetPreviewTitle {
                background: transparent;
                border: none;
                color: #5e584d;
                padding: 0px 2px 2px 2px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 8)
        layout.setSpacing(3)

        self.titleLabel = QLabel(self)
        self.titleLabel.setObjectName("snippetPreviewTitle")
        title_font = self.titleLabel.font()
        title_font.setBold(True)
        title_font.setPointSize(max(9, title_font.pointSize() - 1))
        self.titleLabel.setFont(title_font)
        layout.addWidget(self.titleLabel)

        self.previewEdit = QsciScintilla(self)
        self.previewEdit.setReadOnly(True)
        self.previewEdit.setWrapMode(QsciScintilla.WrapNone)
        self.previewEdit.setFolding(QsciScintilla.NoFoldStyle)
        self.previewEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.previewEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.previewEdit.setMarginWidth(0, 0)
        self.previewEdit.setMarginWidth(1, 0)
        self.previewEdit.setMarginWidth(2, 0)
        self.previewEdit.setMarginWidth(3, 0)
        self.previewEdit.setCaretLineVisible(False)
        self.previewEdit.setCaretWidth(0)
        self.previewEdit.setAutoCompletionSource(QsciScintilla.AcsNone)
        self.previewEdit.setWhitespaceVisibility(QsciScintilla.SCWS_INVISIBLE)
        self.previewEdit.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, QsciScintilla.CARETSTYLE_INVISIBLE)
        self.previewEdit.SendScintilla(QsciScintilla.SCI_SETCODEPAGE, QsciScintilla.SC_CP_UTF8)
        self.previewEdit.setMinimumSize(420, 220)
        self.previewEdit.setStyleSheet("""
            QsciScintilla {
                background: #fffdf8;
                border: 1px solid #ddd4c4;
                border-radius: 6px;
                padding: 4px;
            }
        """)
        layout.addWidget(self.previewEdit)

    def _configure_preview_lexer(self, source_editor=None):
        source_lexer = source_editor.lexer() if source_editor is not None else None
        lexer = None

        if source_lexer is not None:
            try:
                lexer = type(source_lexer)(self.previewEdit)
            except Exception:
                lexer = None

        if lexer is None:
            lexer = self.fallback_lexer_cls(self.previewEdit)

        preview_font = None
        if self.editor_window is not None:
            preview_font = getattr(self.editor_window, 'baseFont', None)
        if preview_font is not None:
            lexer.setFont(preview_font)

        self.previewEdit.setLexer(lexer)
        self.previewLexer = lexer

        if self.editor_window is not None and hasattr(self.editor_window, 'setEditorProperties'):
            self.editor_window.setEditorProperties(self.previewEdit)

        self.previewEdit.setFolding(QsciScintilla.NoFoldStyle)
        self.previewEdit.setWrapMode(QsciScintilla.WrapNone)
        self.previewEdit.setMarginLineNumbers(0, False)
        self.previewEdit.setMarginWidth(0, 0)
        self.previewEdit.setMarginWidth(1, 0)
        self.previewEdit.setMarginWidth(2, 0)
        self.previewEdit.setMarginWidth(3, 0)
        self.previewEdit.setCaretLineVisible(False)
        self.previewEdit.setCaretWidth(0)
        self.previewEdit.setReadOnly(True)
        self.previewEdit.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, QsciScintilla.CARETSTYLE_INVISIBLE)

    def _format_preview_text(self, snippet_text):
        lines = snippet_text.rstrip().splitlines()
        if len(lines) <= self.MAX_VISIBLE_LINES:
            return "\n".join(lines)

        visible_snippet_lines = max(1, self.MAX_VISIBLE_LINES - 1)
        truncated_lines = lines[:visible_snippet_lines]
        return "\n".join(truncated_lines) + self.TRUNCATION_MARKER

    def show_snippet(self, title, snippet_text, anchor_pos, screen=None, source_editor=None):
        self.titleLabel.setText(title)
        self._configure_preview_lexer(source_editor=source_editor)
        self.previewEdit.setText(self._format_preview_text(snippet_text))

        reference_widget = self.editor_window if self.editor_window is not None else None
        reference_frame = reference_widget.frameGeometry() if reference_widget is not None else QRect()

        if screen is None and reference_widget is not None:
            screen = reference_widget.screen()
        if screen is None:
            screen = QApplication.screenAt(anchor_pos)
        if screen is None:
            screen = QApplication.primaryScreen()

        available_geometry = screen.availableGeometry()
        if reference_frame.isValid():
            width_basis = reference_frame.width()
            height_basis = reference_frame.height()
        else:
            width_basis = available_geometry.width()
            height_basis = available_geometry.height()

        width = min(760, max(420, width_basis // 3))
        height = min(520, max(220, height_basis // 3))
        self.resize(width, height)

        if reference_frame.isValid():
            x = reference_frame.right() - self.width()
            y = reference_frame.bottom() - self.height()
        else:
            margin = 12
            x = available_geometry.right() - self.width() - margin
            y = available_geometry.bottom() - self.height() - margin

        margin = 8
        if x < available_geometry.left() + margin:
            x = available_geometry.left() + margin
        if y < available_geometry.top() + margin:
            y = available_geometry.top() + margin

        self.move(x, y)
        self.show()


class SnippetPreviewController(QObject):

    def __init__(self, ui, snippet_dictionary, fallback_lexer_cls=None):
        super().__init__(ui)
        self.ui = ui
        self.snippet_dictionary = snippet_dictionary
        self.popup = SnippetPreviewPopup(editor_window=ui, fallback_lexer_cls=fallback_lexer_cls)

    def attach_menu(self, menu):
        menu.hovered.connect(self._handle_snippet_hovered)
        menu.aboutToHide.connect(self.hide)
        menu.aboutToShow.connect(lambda menu_ref=menu: self.preview_first_action(menu_ref))

    def preview_first_action(self, menu):
        active_action = menu.activeAction()
        if active_action:
            self.show_for_action(active_action, menu)
            return

        for action in menu.actions():
            if not action.isSeparator():
                self.show_for_action(action, menu)
                return

        self.hide()

    def _handle_snippet_hovered(self, action):
        self.show_for_action(action, self.sender())

    def show_for_action(self, action, menu=None):
        if not action or action.isSeparator():
            self.hide()
            return

        action_key = action.data()
        snippet_data = self.snippet_dictionary.get(action_key)
        if snippet_data is None:
            self.hide()
            return

        snippet_text = getattr(snippet_data, 'snippet_text', snippet_data)
        source_editor = self.ui.getCurrentEditor()

        if menu is not None:
            action_rect = menu.actionGeometry(action)
            anchor_pos = menu.mapToGlobal(action_rect.topRight())
            title = menu.title() + " / " + action.text()
            preview_screen = menu.screen()
            if preview_screen is None and menu.window().windowHandle() is not None:
                preview_screen = menu.window().windowHandle().screen()
        else:
            anchor_pos = QCursor.pos()
            title = action.text()
            preview_screen = None

        self.popup.show_snippet(
            title=title,
            snippet_text=snippet_text,
            anchor_pos=anchor_pos,
            screen=preview_screen,
            source_editor=source_editor
        )

    def hide(self):
        self.popup.hide()
