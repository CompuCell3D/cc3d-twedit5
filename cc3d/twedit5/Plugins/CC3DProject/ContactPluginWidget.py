from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class ContactPluginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Plugins/CC3DProject/ContactPlugin_widget.ui", self)

