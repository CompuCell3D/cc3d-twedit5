from cc3d.twedit5.twedit.utils.global_imports import *
from . import ui_steppablegeneratordialog
import sys

MAC = "qt_mac_set_native_menubar" in dir()


class SteppableGeneratorDialog(QDialog, ui_steppablegeneratordialog.Ui_SteppableGenerator):

    def __init__(self, parent=None):

        super(SteppableGeneratorDialog, self).__init__(parent)

        self.cc3dProjectTreeWidget = parent

        # self.cc3dProject=_cc3dProject

        # there are issues with Drawer dialog not getting focus when being displayed on linux

        # they are also not positioned properly so, we use "regular" windows 

        if sys.platform.startswith('win'):
            self.setWindowFlags(Qt.Drawer)  # dialogs without context help - only close button exists

        # self.gotolineSignal.connect(self.editorWindow.goToLine)

        self.projectPath = ""
        self.folderLE = None

        self.setupUi(self)

    def enable_new_file_mode(self, default_folder="Simulation"):
        """Add the folder field used when creating a standalone steppable file."""
        if self.folderLE is not None:
            return

        folder_layout = QFormLayout()
        folder_label = QLabel("Folder")
        self.folderLE = QLineEdit(default_folder)
        folder_layout.addRow(folder_label, self.folderLE)
        self.verticalLayout_2.insertLayout(1, folder_layout)

    def generated_file_name(self):
        name = str(self.steppebleNameLE.text()).strip()
        base_name = name.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        base_name = base_name.rsplit(".", 1)[0]
        if not base_name.lower().endswith("steppable"):
            base_name += "Steppable"
        return base_name + ".py"

    def generated_folder(self):
        return str(self.folderLE.text()).strip() if self.folderLE is not None else ""

    @pyqtSlot()
    def on_okPB_clicked(self):

        if str(self.steppebleNameLE.text()).strip() == "":

            QMessageBox.warning(self, "Empty Steppable Name", "Please specify steppable name")

        elif self.folderLE is not None and not self.generated_folder():

            QMessageBox.warning(self, "Empty Folder", "Please specify the steppable folder")

        else:

            self.accept()
