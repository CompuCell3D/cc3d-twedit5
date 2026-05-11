from cc3d.twedit5.twedit.utils.global_imports import *
from cc3d.twedit5.Plugins.CC3DProject.ContactPluginWidget import ContactPluginWidget
from . import ui_contactPlugin_dlg

MAC = "qt_mac_set_native_menubar" in dir()


class ContactPluginDlg(QDialog, ui_contactPlugin_dlg.Ui_contactPluginDlg):

    def __init__(self, cell_types: dict[str: list[int, bool]], _currentEditor=None, parent=None):

        super(ContactPluginDlg, self).__init__(parent)
        self.editorWindow = parent
        self.setupUi(self)
        self.cell_types: list[str] = list(cell_types)  # grab keys (cell types)

        if not MAC:
            self.cancelPB.setFocusPolicy(Qt.NoFocus)
        # Contact plugin specific params:
        self.use_internal_contact_plugin = False

        # Contact plugin Wizard page generation:
        self.contact_form = ContactPluginWidget(None, self.internalContactPluginInUseCallBack)
        self.contact_form.initContactMatrix(self.cell_types)
        c_container = self.findChild(QWidget, "contact_plugin_container")
        if c_container.layout() is None:
            c_container_layout = QVBoxLayout()
            c_container.setLayout(c_container_layout)
        else:
            c_container_layout = c_container.layout()
        c_container_layout.addWidget(self.contact_form)
        c_container.setLayout(c_container_layout)

        self.updateUi()

    def keyPressEvent(self, event):
        pass
        #    cell_type = str(self.cellTypeLE.text()).strip()
        #   if event.key() == Qt.Key_Return:
        # event.accept()

    def internalContactPluginInUseCallBack(self, use: bool):
        # Callback for user checking the contact_form.on_contact_internalCB
        self.use_internal_contact_plugin = use

    def setUseInternalContactPlugin(self, use: bool):
        # ContactPluginWidget will set up internal contact energy matrix based on cell types used in contact energy matrix.
        self.use_internal_contact_plugin = use
        if use:
            self.contact_form.on_contact_internalCB_toggled(use)

    def getContactEnergyMatrixInformation(self) -> list[tuple[str, str, str]]:
        return self.contact_form.getContactEnergyMatrix()

    def setContactEnergyMatrixInformation(self, cell_cell_energies: list[tuple[str, str, str]]) -> bool:
        if len(cell_cell_energies) > 0:
            return self.contact_form.setContactEnergyMatrix(cell_cell_energies)
        else:
            return False

    def getContactInternalEnergyMatrixInformation(self) -> list[tuple[str, str, str]]:
        return self.contact_form.getInternalContactEnergyMatrix()

    def getContactNeighborOrder(self) -> int:
        return self.contact_form.getContactNeighborOrder()

    def getContactInternalNeighborOrder(self) -> int:
        return self.contact_form.getInternalContactNeighborOrder()


    def updateUi(self):
        pass

