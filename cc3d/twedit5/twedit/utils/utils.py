from pathlib import Path
import html
import sys
import traceback

from jinja2 import Environment, StrictUndefined
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QStyle,
    QTextEdit,
    QVBoxLayout,
)


def render_j2_template(source_template, target_path, substitutions):
    """Render a UTF-8 Jinja2 template to a UTF-8 target file."""
    source_template = Path(source_template)
    target_path = Path(target_path)

    environment = Environment(
        autoescape=False,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    template = environment.from_string(source_template.read_text(encoding="utf-8"))
    target_path.write_text(template.render(**substitutions), encoding="utf-8")


def _build_traceback_html(traceback_text):
    line_html = []

    for raw_line in traceback_text.splitlines():
        escaped_line = html.escape(raw_line)
        stripped_line = raw_line.strip()

        if raw_line.startswith("Traceback"):
            color = "#c7922b"
            font_weight = "700"
        elif stripped_line.startswith('File "'):
            color = "#4f8cc9"
            font_weight = "600"
        elif raw_line.startswith("    "):
            color = "#d8dee9"
            font_weight = "400"
        elif stripped_line and not raw_line.startswith(" "):
            color = "#ff8a80"
            font_weight = "700"
        else:
            color = "#d8dee9"
            font_weight = "400"

        line_html.append(
            "<span style='color: %s; font-weight: %s; white-space: pre-wrap;'>%s</span>" %
            (color, font_weight, escaped_line)
        )

    return "<br>".join(line_html) if line_html else (
        "<span style='color: #d8dee9; white-space: pre-wrap;'>No traceback available.</span>"
    )


class ErrorDetailsDialog(QDialog):
    def __init__(self, title, message, informative_text="", detailed_text="", parent=None):
        super().__init__(parent)

        self._compact_size = (900, 170)
        self._expanded_size = (900, 560)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(*self._compact_size)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 12)
        layout.setSpacing(8)

        header_layout = QHBoxLayout()
        icon_label = QLabel(self)
        icon_label.setPixmap(self.style().standardIcon(QStyle.SP_MessageBoxCritical).pixmap(32, 32))
        icon_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        header_layout.addWidget(icon_label, 0, Qt.AlignVCenter)

        title_label = QLabel("<b>%s</b>" % html.escape(message), self)
        title_label.setWordWrap(True)
        title_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        header_layout.addWidget(title_label, 1, Qt.AlignVCenter)
        layout.addLayout(header_layout)

        if informative_text:
            info_label = QLabel(self)
            info_label.setWordWrap(True)
            info_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            info_label.setStyleSheet(
                "QLabel { background: #fff8e1; border: 1px solid #e6cf8b; "
                "border-radius: 6px; padding: 6px 8px; color: #3a3122; }"
            )
            info_label.setText("<pre style='margin: 0;'>%s</pre>" % html.escape(informative_text))
            layout.addWidget(info_label)

        self.details_edit = QTextEdit(self)
        self.details_edit.setReadOnly(True)
        self.details_edit.setAcceptRichText(True)
        self.details_edit.setStyleSheet(
            "QTextEdit { background: #1f2430; color: #d8dee9; border: 1px solid #394150; "
            "border-radius: 8px; padding: 8px; }"
        )
        self.details_edit.setHtml("<body>%s</body>" % _build_traceback_html(detailed_text))
        self.details_edit.setVisible(False)
        layout.addWidget(self.details_edit, 1)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok, parent=self)
        self.details_button = None
        if detailed_text.strip():
            self.details_button = button_box.addButton("Show More", QDialogButtonBox.ActionRole)
            self.details_button.clicked.connect(self._toggle_details)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

    def _toggle_details(self):
        showing_details = self.details_edit.isVisible()
        self.details_edit.setVisible(not showing_details)
        if self.details_button is not None:
            self.details_button.setText("Show Less" if not showing_details else "Show More")
        self.resize(*(self._expanded_size if not showing_details else self._compact_size))


def show_exception_messagebox(title, message, exception, parent=None):
    traceback_text = "".join(traceback.format_exception(
        type(exception), exception, exception.__traceback__
    ))
    dialog = ErrorDetailsDialog(
        title=title,
        message=message,
        informative_text=str(exception),
        detailed_text=traceback_text,
        parent=parent,
    )
    dialog.exec_()
