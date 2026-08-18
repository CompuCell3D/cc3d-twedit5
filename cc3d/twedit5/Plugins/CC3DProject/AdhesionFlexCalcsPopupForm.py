from PyQt5.QtWidgets import (
    QDialog, QBoxLayout, QTextBrowser, QDialogButtonBox, QLabel
)
from cc3d.twedit5.Plugins.CC3DProject.adhesion_descr import get_adhesion_flex_description_html

# Popup form listing additional info for Adhesion Flex plugin
class AdhesionFlexCalcsPopupForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adhesion Flex plugin calculation information")
        self.setMinimumSize(800, 400)
        # Layout and form
        self.main_layout = QBoxLayout(QBoxLayout.TopToBottom)

        # QTextBrowser object with calcs here:
        self.text_browser = QTextBrowser(self)

        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setHtml(get_adhesion_flex_description_html())
        self.main_layout.addWidget(self.text_browser)

        # OK / Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.main_layout.addWidget(buttons)
        self.setLayout(self.main_layout)
