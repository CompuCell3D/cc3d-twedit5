from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from cc3d.twedit5.Plugins.CC3DProject.ui_contactpluginwidget import Ui_contactPluginWidget

class ContactPluginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_contactPluginWidget()
        self.ui.setupUi(self)
        #uic.loadUi("Plugins/CC3DProject/ContactPlugin_widget.ui", self)  # Alternative approach
        self.ui.contact_value_LE.setText("100,000")

