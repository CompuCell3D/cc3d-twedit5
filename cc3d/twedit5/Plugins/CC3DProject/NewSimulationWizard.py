import errno
import shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
import os
import sys
from . import ui_newsimulationwizard
from collections import OrderedDict
import cc3d
from cc3d.core.XMLUtils import ElementCC3D
from cc3d.core.Validation.sanity_checkers import validate_cc3d_entity_identifier
from cc3d.twedit5.Plugins.CC3DMLGenerator.CC3DMLGeneratorBase import CC3DMLGeneratorBase
from .CC3DPythonGenerator import CC3DPythonGenerator
from cc3d.twedit5.Plugins.CC3DProject.diffusion_solvers_descr import get_diffusion_solv_description_html
from cc3d.twedit5.Plugins.CC3DProject.additionalRxnDiffFE_PropsPopup import RxnDiffusionPropsPopupForm
#from cc3d.twedit5.Plugins.CC3DProject.ui_reactionDiffusion_additional_settings import Ui_RectionDiffusionExtraSettingsDialog

MAC = "qt_mac_set_native_menubar" in dir()
# Wizard pages:
SIMULATION_DIR_PAGE_NAME = "CompuCell3D Simulation Wizard"
SIMULATION_PROPERTIES_PAGE_NAME = "General Simulation Properties"
CHEMICAL_FIELDS_DIFFUSANTS_PAGE_NAME = "Chemical Fields (Diffusants)"
DIFFUSION_WIZARD_PAGE_NAME = "Chemical field diffusion coefficients and boundary conditions (PDE Solvers Specification)"
CELL_PROPS_BEHAVIORS_PAGE_NAME = "Cell Properties and Behaviors"
SECRETION_DIFFUSION_FE_PAGE_NAME = "Secretion in DiffusionFE plugin"  #  DO not use
CELL_TYPE_SPEC_PAGE_NAME = "Cell Type Specification"
CELL_PROP_BEHAVIORS_PAGE_NAME = "Cell Properties and Behaviors"
SECRETION_PAGE_NAME = "Secretion Plugin"  # deprecated for now
CHEMOTAXIS_PAGE_NAME = "Chemotaxis Plugin"
CONTACT_MULTICAD_PAGE_NAME = "ContactMultiCad Plugin"
ADHESION_FLEX_PAGE_NAME = "AdhesionFlex Plugin"
CONFIG_COMPLETE_PAGE_NAME = "Configuration Complete!"

# Diffusion solvers:
DIFFUSION_SOLVER_FE = "DiffusionSolverFE"
REACT_DIFF_SOLVER_FE = "ReactionDiffusionSolverFE"
REACT_DIFF_SOLVER_FVM = "ReactionDiffusionSolverFVM"
SS_DIFF_SOLVER = "SteadyStateDiffusionSolver"
SS_DIFF_SOLVER_2D = "SteadyStateDiffusionSolver2D"

CONSTANT_BC = "Constant value (Dirichlet) "
CONSTANT_DERIVATIVE_BC = "Constant derivative value (von Neumann)"
PERIODIC_BC = "Periodic BC"
GLOBAL_DIFFUSION_LABEL = "Global (default value)"


class NewSimulationWizard(QWizard, ui_newsimulationwizard.Ui_NewSimulationWizard):
    def __init__(self, parent=None):
        super(NewSimulationWizard, self).__init__(parent)

        self.cc3dProjectTreeWidget = parent
        self.plugin = self.cc3dProjectTreeWidget.plugin
        # there are issues with Drawer dialog not getting focus when being displayed on linux
        # they are also not positioned properly so, we use "regular" windows
        if sys.platform.startswith('win'):
            self.setWindowFlags(Qt.Drawer)  # dialogs without context help - only close button exists

        # self.gotolineSignal.connect(self.editorWindow.goToLine)
        self.mainProjDir = ""
        self.simulationFilesDir = ""
        self.projectPath = ""
        self.setupUi(self)
        self.diff_secretion = None  # Holds Diffusion secretion info

        # This dictionary holds references to certain pages e.g. plugin configuration pages are inserted on demand
        # and access to those pages is facilitated via self.pageDict
        self.pageDict = {}

        self.updateUi()

        self.typeTable = []
        self.diffusantDict = {}
        self.rxn_diffusionFE_add_data: dict[str, str] = {}
        self.chemotaxisData = {}
        self.cellTypeData = {}
        self.field_ic_fileDict = {}  # field_name -> ic file name
        self.diffusion_vals_dict = {}
        self.field_table_dict = {}  # {field -> QTableWidget}
        self.diff_solver_info_textBrowser.clear()
        self.diff_solver_info_textBrowser.setHtml(get_diffusion_solv_description_html())
        if sys.platform.startswith('win'):
            self.setWizardStyle(QWizard.ClassicStyle)

    def nextId(self):  # Override nextId() to set page sequence as needed:
        newId = self.currentId()
        print("Page id: ", newId)
        if self.currentId() == self.get_page_id_by_name(SIMULATION_DIR_PAGE_NAME):
            print(self.get_page_id_by_name(SIMULATION_PROPERTIES_PAGE_NAME))
            return self.get_page_id_by_name(SIMULATION_PROPERTIES_PAGE_NAME)
        elif self.currentId() == self.get_page_id_by_name(SIMULATION_PROPERTIES_PAGE_NAME):
            return self.get_page_id_by_name(CELL_TYPE_SPEC_PAGE_NAME)
        elif self.currentId() == self.get_page_id_by_name(CELL_TYPE_SPEC_PAGE_NAME):
            return self.get_page_id_by_name(CELL_PROPS_BEHAVIORS_PAGE_NAME)
        elif self.currentId() == self.get_page_id_by_name(CELL_PROPS_BEHAVIORS_PAGE_NAME):
            return self.get_page_id_by_name(CHEMICAL_FIELDS_DIFFUSANTS_PAGE_NAME)
        elif self.currentId() == self.get_page_id_by_name(CHEMICAL_FIELDS_DIFFUSANTS_PAGE_NAME):
            if len(self.diffusantDict.items()) > 0 and (DIFFUSION_SOLVER_FE in self.diffusantDict or
                                                        SS_DIFF_SOLVER in self.diffusantDict or
                                                        SS_DIFF_SOLVER_2D in self.diffusantDict):
                return self.get_page_id_by_name(DIFFUSION_WIZARD_PAGE_NAME)
            else:
                if self.chemotaxisCHB.isChecked():
                    return self.get_page_id_by_name(CHEMOTAXIS_PAGE_NAME)
                elif self.adhesionFlexCHB.isChecked():
                    return self.get_page_id_by_name(ADHESION_FLEX_PAGE_NAME)
                elif self.contactMultiCadCHB.isChecked():
                    return self.get_page_id_by_name(CONTACT_MULTICAD_PAGE_NAME)
                else:
                    return self.get_page_id_by_name(CONFIG_COMPLETE_PAGE_NAME)
        elif self.currentId() == self.get_page_id_by_name(DIFFUSION_WIZARD_PAGE_NAME):
            if self.chemotaxisCHB.isChecked():
                return self.get_page_id_by_name(CHEMOTAXIS_PAGE_NAME)
            elif self.adhesionFlexCHB.isChecked():
                return self.get_page_id_by_name(ADHESION_FLEX_PAGE_NAME)
            elif self.contactMultiCadCHB.isChecked():
                return self.get_page_id_by_name(CONTACT_MULTICAD_PAGE_NAME)
            else:
                return self.get_page_id_by_name(CONFIG_COMPLETE_PAGE_NAME)
        elif self.currentId() == self.get_page_id_by_name(CHEMOTAXIS_PAGE_NAME):
            if self.adhesionFlexCHB.isChecked():
                return self.get_page_id_by_name(ADHESION_FLEX_PAGE_NAME)
            elif self.contactMultiCadCHB.isChecked():
                return self.get_page_id_by_name(CONTACT_MULTICAD_PAGE_NAME)
            else:
                return self.get_page_id_by_name(CONFIG_COMPLETE_PAGE_NAME)
        elif self.currentId() == self.get_page_id_by_name(ADHESION_FLEX_PAGE_NAME):
            if self.contactMultiCadCHB.isChecked():
                return self.get_page_id_by_name(CONTACT_MULTICAD_PAGE_NAME)
            else:
                return self.get_page_id_by_name(CONFIG_COMPLETE_PAGE_NAME)
        elif self.currentId() == self.get_page_id_by_name(CONFIG_COMPLETE_PAGE_NAME):
            return -1  # No more pages

    def display_invalid_entity_label_message(self, error_message):
        """
        Displays warning about invalid identifier
        :param error_message:
        :return:
        """
        QMessageBox.warning(self, 'Invalid Identifier', error_message)

    def keyPressEvent(self, event):

        if self.currentId() == self.get_page_id_by_name(CELL_TYPE_SPEC_PAGE_NAME):
            cell_type = str(self.cellTypeLE.text())
            cell_type = cell_type.strip()

            if event.key() == Qt.Key_Return:
                if cell_type != "":
                    self.on_cellTypeAddPB_clicked()
                    event.accept()
                else:
                    next_button = self.button(QWizard.NextButton)
                    next_button.clicked.emit(True)

        elif self.currentId() == self.get_page_id_by_name(CHEMICAL_FIELDS_DIFFUSANTS_PAGE_NAME):

            field_name = str(self.fieldNameLE.text())
            field_name = field_name.strip()
            if event.key() == Qt.Key_Return:
                if field_name != "":
                    self.on_fieldAddPB_clicked()
                    event.accept()
                else:
                    next_button = self.button(QWizard.NextButton)
                    next_button.clicked.emit(True)

        elif self.currentId() == self.get_page_id_by_name(CONTACT_MULTICAD_PAGE_NAME):

            cadherin = str(self.cmcMoleculeLE.text()).strip()

            if event.key() == Qt.Key_Return:
                if cadherin != "":

                    self.on_cmcMoleculeAddPB_clicked()
                    event.accept()

                else:

                    next_button = self.button(QWizard.NextButton)
                    next_button.clicked.emit(True)

        elif self.currentId() == self.get_page_id_by_name(ADHESION_FLEX_PAGE_NAME):

            molecule = str(self.afMoleculeLE.text()).strip()

            if event.key() == Qt.Key_Return:

                if molecule != "":
                    self.on_afMoleculeAddPB_clicked()
                    event.accept()

                else:
                    next_button = self.button(QWizard.NextButton)
                    next_button.clicked.emit(True)

        # last page
        elif self.currentId() == self.get_page_id_by_name(CONFIG_COMPLETE_PAGE_NAME):

            if event.key() == Qt.Key_Return:
                finish_button = self.button(QWizard.FinishButton)
                finish_button.clicked.emit(True)

        else:

            if event.key() == Qt.Key_Return:
                # move to the next page
                next_button = self.button(QWizard.NextButton)
                next_button.clicked.emit(True)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_piffPB_clicked(self):

        file_name = QFileDialog.getOpenFileName(self, "Choose PIFF file...")

        file_name = str(file_name)

        # normalizing path
        file_name = os.path.abspath(file_name)

        self.piffLE.setText(file_name)

    def hideConstraintFlexOption(self):

        self.volumeFlexCHB.setChecked(False)

        self.volumeFlexCHB.setHidden(True)

        self.surfaceFlexCHB.setChecked(False)

        self.surfaceFlexCHB.setHidden(True)

    def showConstraintFlexOption(self):

        if not self.growthCHB.isChecked() and not self.mitosisCHB.isChecked() and not self.deathCHB.isChecked():
            self.volumeFlexCHB.setHidden(False)

            self.surfaceFlexCHB.setHidden(False)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_extPotCHB_toggled(self, _flag):

        if _flag:
            self.extPotLocalFlexCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_extPotLocalFlexCHB_toggled(self, _flag):

        if _flag:
            self.extPotCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_volumeFlexCHB_toggled(self, _flag):

        if _flag:
            self.volumeLocalFlexCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_volumeLocalFlexCHB_toggled(self, _flag):

        if _flag:
            self.volumeFlexCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_surfaceFlexCHB_toggled(self, _flag):

        if _flag:
            self.surfaceLocalFlexCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_surfaceLocalFlexCHB_toggled(self, _flag):

        if _flag:
            self.surfaceFlexCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_connectGlobalCHB_toggled(self, _flag):

        if _flag:
            self.connect2DCHB.setChecked(not _flag)

            self.connectGlobalByIdCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_connect2DCHB_toggled(self, _flag):

        if _flag:
            self.connectGlobalCHB.setChecked(not _flag)

            self.connectGlobalByIdCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_connectGlobalByIdCHB_toggled(self, _flag):

        if _flag:
            self.connect2DCHB.setChecked(not _flag)

            self.connectGlobalCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_lengthConstraintCHB_toggled(self, _flag):

        if _flag:
            self.lengthConstraintLocalFlexCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_lengthConstraintLocalFlexCHB_toggled(self, _flag):

        if _flag:
            self.lengthConstraintCHB.setChecked(not _flag)

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_growthCHB_toggled(self, _flag):

        if _flag:

            self.hideConstraintFlexOption()

        else:

            self.showConstraintFlexOption()

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_mitosisCHB_toggled(self, _flag):

        if _flag:

            self.hideConstraintFlexOption()

        else:

            self.showConstraintFlexOption()

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_deathCHB_toggled(self, _flag):

        if _flag:

            self.hideConstraintFlexOption()

        else:

            self.showConstraintFlexOption()

    @pyqtSlot()  # signature of the signal emited by the button
    def on_cellTypeAddPB_clicked(self):

        cell_type = str(self.cellTypeLE.text()).strip()
        try:
            validate_cc3d_entity_identifier(cell_type, entity_type_label='cell type')
        except AttributeError as e:
            self.display_invalid_entity_label_message(error_message=str(e))
            return

        rows = self.cellTypeTable.rowCount()

        if cell_type == "":
            return

        # check if cell type with this name already exist

        cell_type_already_exists = False

        for rowId in range(rows):
            name = str(self.cellTypeTable.item(rowId, 0).text()).strip()
            print("CHECKING name=", name + "1", " type=", cell_type + "1")

            print("name==cellType ", name == cell_type)

            if name == cell_type:
                cell_type_already_exists = True

                break

        print("cellTypeAlreadyExists=", cell_type_already_exists)

        if cell_type_already_exists:
            print("WARNING")

            QMessageBox.warning(self, "Cell type name already exists",

                                "Cell type name already exist. Please choose different name", QMessageBox.Ok)

            return

        self.cellTypeTable.insertRow(rows)

        cell_type_item = QTableWidgetItem(cell_type)

        self.cellTypeTable.setItem(rows, 0, cell_type_item)

        cell_type_freeze_item = QTableWidgetItem()
        cell_type_freeze_item.data(Qt.CheckStateRole)

        if self.freezeCHB.isChecked():

            cell_type_freeze_item.setCheckState(Qt.Checked)

        else:

            cell_type_freeze_item.setCheckState(Qt.Unchecked)

        self.cellTypeTable.setItem(rows, 1, cell_type_freeze_item)

        # reset cell type entry line
        self.cellTypeLE.setText("")

    @pyqtSlot()  # signature of the signal emited by the button
    def on_clearCellTypeTablePB_clicked(self):

        rows = self.cellTypeTable.rowCount()

        for i in range(rows - 1, -1, -1):
            self.cellTypeTable.removeRow(i)

        # insert Medium
        self.cellTypeTable.insertRow(0)

        medium_item = QTableWidgetItem("Medium")

        self.cellTypeTable.setItem(0, 0, medium_item)

        medium_freeze_item = QTableWidgetItem()
        medium_freeze_item.data(Qt.CheckStateRole)
        medium_freeze_item.setCheckState(Qt.Unchecked)

        self.cellTypeTable.setItem(0, 1, medium_freeze_item)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_fieldAddPB_clicked(self):

        field_name = str(self.fieldNameLE.text()).strip()

        try:
            validate_cc3d_entity_identifier(field_name, entity_type_label='field label')
        except AttributeError as e:
            self.display_invalid_entity_label_message(error_message=str(e))
            return

        rows = self.fieldTable.rowCount()

        if field_name == "":
            return

        # check if cell type with this name already exist

        field_already_exists = False

        for row_id in range(rows):
            name = str(self.fieldTable.item(row_id, 0).text()).strip()
            print("CHECKING name=", name + "1", " type=", field_name + "1")
            print("name==cellType ", name == field_name)

            if name == field_name:
                field_already_exists = True

                break

        print("fieldAlreadyExists=", field_already_exists)
        if field_already_exists:
            print("WARNING")

            QMessageBox.warning(self, "Field name name already exists",
                                "Field name name already exist. Please choose different name", QMessageBox.Ok)

            return

        self.fieldTable.insertRow(rows)

        field_name_item = QTableWidgetItem(field_name)
        self.fieldTable.setItem(rows, 0, field_name_item)

        # picking solver name
        solver_name = str(self.solverCB.currentText()).strip()

        solver_name_item = QTableWidgetItem(solver_name)

        self.fieldTable.setItem(rows, 1, solver_name_item)

        # reset cell type entry line
        self.fieldNameLE.setText("")

    @pyqtSlot()  # signature of the signal emited by the button
    def on_clearFieldTablePB_clicked(self):

        rows = self.fieldTable.rowCount()

        for i in range(rows - 1, -1, -1):
            self.fieldTable.removeRow(i)

    # SECRETION
    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_secrConstConcRB_toggled(self, _flag):

        if _flag:
            self.secrRateLB.setText("Const. Concentration")
        else:

            self.secrRateLB.setText("Secretion Rate")

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_secrOnContactRB_toggled(self, _flag):
        if _flag:

            self.secrAddOnContactPB.setHidden(False)
            self.secrOnContactCellTypeCB.setHidden(False)
            self.secrOnContactLE.setHidden(False)

        else:

            self.secrAddOnContactPB.setHidden(True)
            self.secrOnContactCellTypeCB.setHidden(True)
            self.secrOnContactLE.setHidden(True)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_secrAddOnContactPB_clicked(self):

        cell_type = str(self.secrOnContactCellTypeCB.currentText())

        current_text = str(self.secrOnContactLE.text())

        current_types = current_text.split(',')

        if current_text != "":
            if cell_type not in current_types:
                self.secrOnContactLE.setText(current_text + "," + cell_type)
        else:
            self.secrOnContactLE.setText(cell_type)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_secrAddRowPB_clicked(self):

        field = str(self.secrFieldCB.currentText()).strip()
        cell_type = str(self.secrCellTypeCB.currentText()).strip()

        try:
            secr_rate = float(str(self.secrRateLE.text()))
        except Exception:
            secr_rate = 0.0

        secr_on_contact = str(self.secrOnContactLE.text())

        secr_type = "uniform"
        if self.secrOnContactRB.isChecked():
            secr_type = "on contact"

        elif self.secrConstConcRB.isChecked():
            secr_type = "constant concentration"

        rows = self.secretionTable.rowCount()

        self.secretionTable.insertRow(rows)

        self.secretionTable.setItem(rows, 0, QTableWidgetItem(field))
        self.secretionTable.setItem(rows, 1, QTableWidgetItem(cell_type))
        self.secretionTable.setItem(rows, 2, QTableWidgetItem(str(secr_rate)))
        self.secretionTable.setItem(rows, 3, QTableWidgetItem(secr_on_contact))
        self.secretionTable.setItem(rows, 4, QTableWidgetItem(str(secr_type)))

        # reset entry lines
        self.secrOnContactLE.setText('')

    @pyqtSlot()  # signature of the signal emited by the button
    def on_secrRemoveRowsPB_clicked(self):

        selected_items = self.secretionTable.selectedItems()

        row_dict = {}
        for item in selected_items:
            row_dict[item.row()] = 0

        rows = list(row_dict.keys())

        rows.sort()

        rows_size = len(rows)
        for idx in range(rows_size - 1, -1, -1):
            row = rows[idx]
            self.secretionTable.removeRow(row)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_secrClearTablePB_clicked(self):

        rows = self.secretionTable.rowCount()

        for idx in range(rows - 1, -1, -1):
            self.secretionTable.removeRow(idx)

    # DiffusionFE Secretion, remove if separate page not needed
    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_secrConstConcRB_2_toggled(self, _flag):
        if _flag:
            self.secrRateLB_2.setText("Const. Concentration")
        else:
            self.secrRateLB_2.setText("Secretion Rate")

    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_secrOnContactRB_2_toggled(self, _flag):
        if _flag:
            self.secrAddOnContactPB_2.setHidden(False)
            self.secrOnContactCellTypeCB_2.setHidden(False)
            self.secrOnContactLE_2.setHidden(False)

        else:
            self.secrAddOnContactPB_2.setHidden(True)
            self.secrOnContactCellTypeCB_2.setHidden(True)
            self.secrOnContactLE_2.setHidden(True)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_secrAddOnContactPB_2_clicked(self):

        cell_type = str(self.secrOnContactCellTypeCB_2.currentText())
        current_text = str(self.secrOnContactLE_2.text())
        current_types = current_text.split(',')

        if current_text != "":
            if cell_type not in current_types:
                self.secrOnContactLE_2.setText(current_text + "," + cell_type)
        else:
            self.secrOnContactLE_2.setText(cell_type)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_secrAddRowPB_2_clicked(self):  # Remove, secretion does not have its own table
        field = str(self.secrFieldCB_2.currentText()).strip()
        cell_type = str(self.secrCellTypeCB_2.currentText()).strip()

        try:
            secr_rate = float(str(self.secrRateLE_2.text()))
        except Exception:
            secr_rate = 0.0

        secr_on_contact = str(self.secrOnContactLE_2.text())

        secr_type = "uniform"
        if self.secrOnContactRB_2.isChecked():
            secr_type = "on contact"

        elif self.secrConstConcRB_2.isChecked():
            secr_type = "constant concentration"

        rows = self.secretion_DiffusionFE_Table.rowCount()
        self.secretion_DiffusionFE_Table.insertRow(rows)
        self.secretion_DiffusionFE_Table.setItem(rows, 0, QTableWidgetItem(field))
        self.secretion_DiffusionFE_Table.setItem(rows, 1, QTableWidgetItem(cell_type))
        self.secretion_DiffusionFE_Table.setItem(rows, 2, QTableWidgetItem(str(secr_rate)))
        self.secretion_DiffusionFE_Table.setItem(rows, 3, QTableWidgetItem(secr_on_contact))
        self.secretion_DiffusionFE_Table.setItem(rows, 4, QTableWidgetItem(str(secr_type)))

        # reset entry lines
        self.secrOnContactLE_2.setText('')

    @pyqtSlot()  # signature of the signal emited by the button
    def on_secrRemoveRowsPB_2_clicked(self):
        selected_items = self.secretion_DiffusionFE_Table.selectedItems()
        row_dict = {}
        for item in selected_items:
            row_dict[item.row()] = 0

        rows = list(row_dict.keys())
        rows.sort()
        rows_size = len(rows)
        for idx in range(rows_size - 1, -1, -1):
            row = rows[idx]
            self.secretion_DiffusionFE_Table.removeRow(row)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_secrClearTablePB_2_clicked(self):
        rows = self.secretion_DiffusionFE_Table.rowCount()

        for idx in range(rows - 1, -1, -1):
            self.secretion_DiffusionFE_Table.removeRow(idx)




    # CHEMOTAXIS
    @pyqtSlot(bool)  # signature of the signal emited by the button
    def on_chemSatRB_toggled(self, _flag):

        if _flag:

            self.satCoefLB.setText("Saturation Coef.")
            self.satCoefLB.setHidden(False)
            self.satChemLE.setHidden(False)

        else:

            self.satCoefLB.setHidden(True)
            self.satChemLE.setHidden(True)
            self.satChemLE.setText('')

    @pyqtSlot(bool)  # signature of the signal emited by the radio button
    def on_chemSatLinRB_toggled(self, _flag):

        if _flag:
            self.satCoefLB.setText("Saturation Coef. Linear")
            self.satCoefLB.setHidden(False)
            self.satChemLE.setHidden(False)

        else:

            self.satCoefLB.setHidden(True)
            self.satChemLE.setHidden(True)
            self.satChemLE.setText('')

    @pyqtSlot()  # signature of the signal emited by the button
    def on_chemotaxTowardsPB_clicked(self):

        cell_type = str(self.chemTowardsCellTypeCB.currentText())

        current_text = str(self.chemotaxTowardsLE.text())

        current_types = current_text.split(',')

        if current_text != "":
            if cell_type not in current_types:
                self.chemotaxTowardsLE.setText(current_text + "," + cell_type)
        else:
            self.chemotaxTowardsLE.setText(cell_type)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_chemotaxisAddRowPB_clicked(self):

        field = str(self.chemFieldCB.currentText()).strip()

        cell_type = str(self.chemCellTypeCB.currentText()).strip()

        try:
            lambda_ = float(str(self.lambdaChemLE.text()))
        except Exception:
            lambda_ = 0.0

        saturation_coef = 0.0

        if not self.chemRegRB.isChecked():

            try:
                saturation_coef = float(str(self.satChemLE.text()))
            except Exception:
                saturation_coef = 0.0

        chemotax_towards_types = str(self.chemotaxTowardsLE.text())

        chemotaxis_type = "regular"

        if self.chemSatRB.isChecked():
            chemotaxis_type = "saturation"

        elif self.chemSatLinRB.isChecked():

            chemotaxis_type = "saturation linear"

        rows = self.chamotaxisTable.rowCount()

        self.chamotaxisTable.insertRow(rows)

        self.chamotaxisTable.setItem(rows, 0, QTableWidgetItem(field))
        self.chamotaxisTable.setItem(rows, 1, QTableWidgetItem(cell_type))
        self.chamotaxisTable.setItem(rows, 2, QTableWidgetItem(str(lambda_)))
        self.chamotaxisTable.setItem(rows, 3, QTableWidgetItem(chemotax_towards_types))
        self.chamotaxisTable.setItem(rows, 4, QTableWidgetItem(str(saturation_coef)))
        self.chamotaxisTable.setItem(rows, 5, QTableWidgetItem(chemotaxis_type))

        # reset entry lines

        self.chemotaxTowardsLE.setText('')

    @pyqtSlot()  # signature of the signal emited by the button
    def on_chemotaxisRemoveRowsPB_clicked(self):

        selected_items = self.chamotaxisTable.selectedItems()

        row_dict = {}
        for item in selected_items:
            row_dict[item.row()] = 0

        rows = list(row_dict.keys())

        rows.sort()

        rows_size = len(rows)

        for idx in range(rows_size - 1, -1, -1):
            row = rows[idx]
            self.chamotaxisTable.removeRow(row)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_chemotaxisClearTablePB_clicked(self):

        rows = self.chamotaxisTable.rowCount()

        for idx in range(rows - 1, -1, -1):
            self.chamotaxisTable.removeRow(idx)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_afMoleculeAddPB_clicked(self):

        molecule = str(self.afMoleculeLE.text()).strip()

        rows = self.afTable.rowCount()

        if molecule == "":
            return

        # check if molecule with this name already exist

        molecule_already_exists = False
        for rowId in range(rows):
            name = str(self.afTable.item(rowId, 0).text()).strip()

            if name == molecule:
                molecule_already_exists = True
                break

        if molecule_already_exists:
            QMessageBox.warning(self, "Molecule Name Already Exists",

                                "Molecule name already exist. Please choose different name", QMessageBox.Ok)

            return

        self.afTable.insertRow(rows)

        molecule_item = QTableWidgetItem(molecule)

        self.afTable.setItem(rows, 0, molecule_item)

        # reset molecule entry line
        self.afMoleculeLE.setText("")

        return

    @pyqtSlot()  # signature of the signal emited by the button
    def on_clearAFTablePB_clicked(self):

        rows = self.afTable.rowCount()

        for i in range(rows - 1, -1, -1):
            self.afTable.removeRow(i)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_cmcMoleculeAddPB_clicked(self):

        cadherin = str(self.cmcMoleculeLE.text()).strip()

        rows = self.cmcTable.rowCount()

        if cadherin == "":
            return

        # check if cadherin with this name already exist

        cadherin_already_exists = False

        for rowId in range(rows):
            name = str(self.cmcTable.item(rowId, 0).text()).strip()

            if name == cadherin:
                cadherin_already_exists = True
                break

        if cadherin_already_exists:
            QMessageBox.warning(self, "Cadherin Name Already Exists",
                                "Cadherin name already exist. Please choose different name", QMessageBox.Ok)

            return

        self.cmcTable.insertRow(rows)

        cadherin_item = QTableWidgetItem(cadherin)

        self.cmcTable.setItem(rows, 0, cadherin_item)

        # reset cadherin entry line
        self.cmcMoleculeLE.setText("")

    @pyqtSlot()  # signature of the signal emited by the button
    def on_clearCMCTablePB_clicked(self):

        rows = self.cmcTable.rowCount()

        for i in range(rows - 1, -1, -1):
            self.cmcTable.removeRow(i)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_dirPB_clicked(self):

        name = str(self.nameLE.text()).strip()

        proj_dir = self.plugin.configuration.setting("RecentNewProjectDir")
        if name != "":
            directory = QFileDialog.getExistingDirectory(self, "Specify Location for your project", proj_dir)
            self.plugin.configuration.setSetting("RecentNewProjectDir", directory)
            self.dirLE.setText(directory)

    @pyqtSlot()  # signature of the signal emitted by the button
    def on_reactionDiff_FE_PB_clicked(self):
        popup = RxnDiffusionPropsPopupForm(self)
        if len(self.rxn_diffusionFE_add_data) > 1:  # Load existing user data, if exists
            popup.set_data(self.rxn_diffusionFE_add_data)
        if popup.exec_() == QDialog.Accepted:
            extra_settings: dict = popup.get_data()
            for key in extra_settings:
                print(f"{key}: {extra_settings[key]}")
                self.rxn_diffusionFE_add_data[key] = extra_settings[key]
        else:
            print("Popup cancelled")
            #self.result_label.setText("Popup canceled.")

    # setting up validators for the entry fields
    def setUpValidators(self):

        self.membraneFluctuationsLE.setValidator(QDoubleValidator())
        self.secrRateLE.setValidator(QDoubleValidator())
        self.lambdaChemLE.setValidator(QDoubleValidator())
        self.satChemLE.setValidator(QDoubleValidator())

    def get_page_id_by_name(self, page_name: str):
        return self.pageDict[page_name][1]

    def get_page_by_name(self, page_name: str):
        return self.pageDict[page_name][0]

    # initialize properties dialog

    def updateUi(self):

        self.setUpValidators()

        # Multi cad plugin is being deprecated
        self.contactMultiCadCHB.setEnabled(False)

        # have to set base size in QDesigner and then read it to rescale columns.
        # For some reason reading size of the widget does not work properly

        page_ids = self.pageIds()

        #  just iterate through ids in order to set pages, use nextId() to set order:
        for index in range(len(page_ids)):
            self.pageDict[self.page(index).title()] = [self.page(index), index]
        # remove pages not always needed:
        self.removePage(self.get_page_id_by_name(SECRETION_PAGE_NAME))  # deprecated
        self.removePage(self.get_page_id_by_name(CHEMOTAXIS_PAGE_NAME))
        self.removePage(self.get_page_id_by_name(ADHESION_FLEX_PAGE_NAME))
        self.removePage(self.get_page_id_by_name(CONTACT_MULTICAD_PAGE_NAME))
        self.removePage(self.get_page_id_by_name(DIFFUSION_WIZARD_PAGE_NAME))
        self.removePage(self.get_page_id_by_name(SECRETION_DIFFUSION_FE_PAGE_NAME))  # Do not use.

        self.nameLE.selectAll()

        proj_dir = self.plugin.configuration.setting("RecentNewProjectDir")

        print("projDir=", str(proj_dir))

        if str(proj_dir) == "":
            proj_dir = cc3d.cc3d_install_prefix

        self.dirLE.setText(proj_dir)

        # self.cellTypeLE.setFocus(True)

        self.cellTypeTable.insertRow(0)

        medium_item = QTableWidgetItem("Medium")

        self.cellTypeTable.setItem(0, 0, medium_item)

        medium_freeze_item = QTableWidgetItem()
        medium_freeze_item.data(Qt.CheckStateRole)
        medium_freeze_item.setCheckState(Qt.Unchecked)

        self.cellTypeTable.setItem(0, 1, medium_freeze_item)

        base_size = self.cellTypeTable.baseSize()
        self.cellTypeTable.setColumnWidth(0, int(base_size.width() / 2))
        self.cellTypeTable.setColumnWidth(1, int(base_size.width() / 2))
        self.cellTypeTable.horizontalHeader().setStretchLastSection(True)

        # general properties page

        self.piffPB.setHidden(True)
        self.piffLE.setHidden(True)

        # chemotaxis page

        base_size = self.fieldTable.baseSize()

        self.fieldTable.setColumnWidth(0, int(base_size.width() / 2))
        self.fieldTable.setColumnWidth(1, int(base_size.width() / 2))
        self.fieldTable.horizontalHeader().setStretchLastSection(True)

        self.satCoefLB.setHidden(True)
        self.satChemLE.setHidden(True)

        # secretion page - REMOVE at some point, not used

        base_size = self.secretionTable.baseSize()

        self.secretionTable.setColumnWidth(0, int(base_size.width() / 5))
        self.secretionTable.setColumnWidth(1, int(base_size.width() / 5))
        self.secretionTable.setColumnWidth(2, int(base_size.width() / 5))
        self.secretionTable.setColumnWidth(3, int(base_size.width() / 5))
        self.secretionTable.setColumnWidth(4, int(base_size.width() / 5))
        self.secretionTable.horizontalHeader().setStretchLastSection(True)
        self.secrAddOnContactPB.setHidden(True)
        self.secrOnContactCellTypeCB.setHidden(True)
        self.secrOnContactLE.setHidden(True)

        # Diffusion Secretion table:
        base_size = self.secretion_DiffusionFE_Table.baseSize()
        self.secretion_DiffusionFE_Table.setColumnWidth(0, int(base_size.width() / 5))
        self.secretion_DiffusionFE_Table.setColumnWidth(1, int(base_size.width() / 5))
        self.secretion_DiffusionFE_Table.setColumnWidth(2, int(base_size.width() / 5))
        self.secretion_DiffusionFE_Table.setColumnWidth(3, int(base_size.width() / 5))
        self.secretion_DiffusionFE_Table.setColumnWidth(4, int(base_size.width() / 5))
        self.secretion_DiffusionFE_Table.horizontalHeader().setStretchLastSection(True)
        self.secrAddOnContactPB_2.setHidden(True)
        self.secrOnContactCellTypeCB_2.setHidden(True)
        self.secrOnContactLE_2.setHidden(True)

        # AF molecule table
        self.afTable.horizontalHeader().setStretchLastSection(True)

        # CMC cadherin table
        self.cmcTable.horizontalHeader().setStretchLastSection(True)

        width = self.cellTypeTable.horizontalHeader().width()

        print("column 0 width=", self.cellTypeTable.horizontalHeader().sectionSize(0))
        print("column 1 width=", self.cellTypeTable.horizontalHeader().sectionSize(1))
        print("size=", self.cellTypeTable.size())
        print("baseSize=", self.cellTypeTable.baseSize())
        print("width=", width)
        print("column width=", self.cellTypeTable.columnWidth(0))

    def insertModulePage(self, _page):

        # get FinalPage id
        final_id = -1

        page_ids = self.pageIds()

        for page_id in page_ids:

            if self.page(page_id) == self.get_page_by_name[CONFIG_COMPLETE_PAGE_NAME]:
                final_id = page_id

                break

        if final_id == -1:
            print("COULD NOT INSERT PAGE  COULD NOT FIND LAST PAGE ")

            return

        print("FinalId=", final_id)

        self.setPage(final_id - 1, _page)

    def removeModulePage(self, _page):

        page_ids = self.pageIds()

        for page_id in page_ids:

            if self.page(page_id) == _page:
                self.removePage(page_id)
                break

    def checkIfNumber(self, value):
        if value == ".":
            return True
        if value.isdecimal():
            return True
        try:
            float(value)
            return True
        except ValueError:
            QMessageBox.warning(self, "Not a number",
                                    "Please specify a number for the value",
                                    QMessageBox.Ok)
            return False

    def x_bcTypeChanged(self, index):
        tab_idx = self.bcs_tab.currentIndex()
        xc = "x_combo" + str(tab_idx)
        xmin_le = "x_min" + str(tab_idx)
        xmax_le = "x_max" + str(tab_idx)
        current_combo = self.bcs_tab.findChild(QComboBox, xc)
        cur_text = current_combo.itemText(index)
        if index == 0:  # periodic boundary
            xMin = self.bcs_tab.findChild(QLineEdit, xmin_le)
            xMin.setDisabled(True)
            xMax = self.bcs_tab.findChild(QLineEdit, xmax_le)
            xMax.setDisabled(True)
        else:
            if index == 1:  # Constant value
                xMin = self.bcs_tab.findChild(QLineEdit, xmin_le)
                xMin.setDisabled(False)
                xMax = self.bcs_tab.findChild(QLineEdit, xmax_le)
                xMax.setDisabled(False)
            else:       # constant derivative
                xMin = self.bcs_tab.findChild(QLineEdit, xmin_le)
                xMin.setDisabled(False)
                xMax = self.bcs_tab.findChild(QLineEdit, xmax_le)
                xMax.setDisabled(False)


    def y_bcTypeChanged(self, index):
        tab_idx = self.bcs_tab.currentIndex()
        ymin_le = "y_min" + str(tab_idx)
        ymax_le = "y_max" + str(tab_idx)
        if index == 0:  # periodic boundary
            yMin = self.bcs_tab.findChild(QLineEdit, ymin_le)
            yMin.setDisabled(True)
            yMax = self.bcs_tab.findChild(QLineEdit, ymax_le)
            yMax.setDisabled(True)
        else:
            if index == 1:  # Constant value
                yMin = self.bcs_tab.findChild(QLineEdit, ymin_le)
                yMin.setDisabled(False)
                yMax = self.bcs_tab.findChild(QLineEdit, ymax_le)
                yMax.setDisabled(False)
            else:  # constant derivative
                yMin = self.bcs_tab.findChild(QLineEdit, ymin_le)
                yMin.setDisabled(False)
                yMax = self.bcs_tab.findChild(QLineEdit, ymax_le)
                yMax.setDisabled(False)

    def z_bcTypeChanged(self, index):
        tab_idx = self.bcs_tab.currentIndex()
        zmin_le = "z_min" + str(tab_idx)
        zmax_le = "z_max" + str(tab_idx)
       # zc = "z_combo" + str(tab_idx)
       # current_combo = self.bcs_tab.findChild(QComboBox, zc)

       # cur_text = current_combo.itemText(index)
        if index == 0:  # periodic boundary
            zMin = self.bcs_tab.findChild(QLineEdit, zmin_le)
            zMin.setDisabled(True)
            zMax = self.bcs_tab.findChild(QLineEdit, zmax_le)
            zMax.setDisabled(True)
        else:
            if index == 1:  # Constant value
                zMin = self.bcs_tab.findChild(QLineEdit, zmin_le)
                zMin.setDisabled(False)
                zMax = self.bcs_tab.findChild(QLineEdit, zmax_le)
                zMax.setDisabled(False)
            else:  # constant derivative
                zMin = self.bcs_tab.findChild(QLineEdit, zmin_le)
                zMin.setDisabled(False)
                zMax = self.bcs_tab.findChild(QLineEdit, zmax_le)
                zMax.setDisabled(False)

    def field_tab_changed(self, index):
        if self.bcs_tab.currentIndex() != index:
            self.bcs_tab.setCurrentIndex(index)
        if self.ics_tab.currentIndex() != index:
            self.ics_tab.setCurrentIndex(index)
        if self.field_tab.currentIndex() != index:
            self.field_tab.setCurrentIndex(index)

    def ics_file_path_changed(self):
        tab_idx = self.ics_tab.currentIndex()
        field = self.ics_tab.tabText(tab_idx)
        icfe = "ic_file_edt_" + str(tab_idx)
        current_fe = self.ics_tab.findChild(QLineEdit, icfe)
        ic_file = current_fe.text()  # contains full (absolute) file path
        print(ic_file)
        #  check if valid file location:
        if self.is_path_exists_or_creatable(ic_file):
            self.field_ic_fileDict[field] = ic_file
        else:
            # put prev file path back:
            current_fe.setText(self.field_ic_fileDict[field])


    def use_ics_file(self, index):
        tab_idx = self.ics_tab.currentIndex()
        icr = "ic_radio_btn_" + str(tab_idx)
        current_rb = self.ics_tab.findChild(QRadioButton, icr)
        icf = "ic_file_edt_" + str(tab_idx)
        current_fi = self.ics_tab.findChild(QLineEdit, icf)
        icle = "ic_val_" + str(tab_idx)
        current_le = self.ics_tab.findChild(QLineEdit, icle)
        if current_rb.isChecked():
            current_fi.setDisabled(False)
            current_le.setDisabled(True)
        else:
            current_fi.setDisabled(True)
            current_le.setDisabled(False)

    def getIC_Dialog(self, idx):
        ic_group = QGroupBox("")
        ic_group.setObjectName("ic_group_" + str(idx))
        ic_layout = QBoxLayout(QBoxLayout.LeftToRight)
        # Initial Val:
        ic_val_group = QGroupBox("Initial value")
        ic_val_layout = QBoxLayout(QBoxLayout.TopToBottom, ic_val_group)
        ic_val_label = QLabel("Diffusant initial concentration or expression:")
        ic_val_edit = QLineEdit("0.0")
        icv = "ic_val_" + str(idx)
        ic_val_edit.setObjectName(icv)
        ic_val_edit.textChanged.connect(self.checkIfNumber)
        ic_val_layout.addWidget(ic_val_label)
        ic_val_layout.addWidget(ic_val_edit)
        ic_val_group.setLayout(ic_val_layout)
        ic_layout.addWidget(ic_val_group)
        # inital conc file:
        ic_file_group = QGroupBox("Initial values file")
        ic_file_layout = QBoxLayout(QBoxLayout.TopToBottom)
        icfr = "ic_radio_btn_" + str(idx)
        ic_file_radio_btn = QRadioButton("Use Initial Concentrations file")
        ic_file_radio_btn.setObjectName(icfr)
        ic_file_radio_btn.toggled.connect(self.use_ics_file)
        field_name = self.bcs_tab.tabText(idx)  # ics and bcs use same field names
        default_file = str(self.dirLE.text()).strip() + str(self.nameLE.text()).strip() + "/"
      #  if sys.platform.startswith("win"): Python takes care of this?
      #      default_file = default_file + "\\"
        default_file = default_file + "init_conditions_" + field_name + ".txt"
        self.field_ic_fileDict[field_name] = default_file
        ic_file_edit = QLineEdit(default_file)
        ic_file_edit.setObjectName("ic_file_edt_" + str(idx))
        ic_file_edit.setDisabled(True)
        ic_file_edit.editingFinished.connect(self.ics_file_path_changed)
        ic_file_info_label = QLabel("Format of file is rows of numbers corresponding to position of each pixel and concentration: x y z c")
        ic_file_layout.addWidget(ic_file_radio_btn)
        ic_file_layout.addWidget(ic_file_edit)
        ic_file_layout.addWidget(ic_file_info_label)
        ic_file_group.setLayout(ic_file_layout)

        ic_layout.addWidget(ic_file_group)
        ic_group.setLayout(ic_layout)
        return ic_group
    def getBC_Dialog(self, idx):
        bc_group = QGroupBox("")
        bc_layout = QBoxLayout(QBoxLayout.LeftToRight)
        # X axis:
        x_group = QGroupBox("Along X axis", bc_group)
        x_group.setObjectName("x_group_" + str(idx))
        x_layout = QBoxLayout(QBoxLayout.TopToBottom, x_group)
        x_new_combo_bx = QComboBox(x_group)
        xc = "x_combo" + str(idx)
        x_new_combo_bx.setObjectName(xc)
        x_new_combo_bx.addItem(PERIODIC_BC)
        x_new_combo_bx.addItem(CONSTANT_BC)
        x_new_combo_bx.addItem(CONSTANT_DERIVATIVE_BC)
        x_new_combo_bx.setCurrentIndex(2) # set to Constant derivative
        x_new_combo_bx.currentIndexChanged.connect(self.x_bcTypeChanged)
        x_layout.addWidget(x_new_combo_bx, 0)
        xmin_label = QLabel("Value at x = x.min")
        xmin_line_edit = QLineEdit("0.0")
        xmin_le = "x_min" + str(idx)
        xmin_line_edit.setObjectName(xmin_le)
        xmin_line_edit.textChanged.connect(self.checkIfNumber)
        xmax_label = QLabel("Value at x = x.max")
        xmax_line_edit = QLineEdit("0.0")
        xmax_le = "x_max" + str(idx)
        xmax_line_edit.setObjectName(xmax_le)
        xmax_line_edit.textChanged.connect(self.checkIfNumber)
        xmin_group = QGroupBox("")
        xmin_layout = QBoxLayout(QBoxLayout.LeftToRight)
        xmin_layout.addWidget(xmin_label)
        xmin_layout.addWidget(xmin_line_edit)
        xmin_group.setLayout(xmin_layout)
        xmax_group = QGroupBox("")
        xmax_layout = QBoxLayout(QBoxLayout.LeftToRight)
        xmax_layout.addWidget(xmax_label)
        xmax_layout.addWidget(xmax_line_edit)
        xmax_group.setLayout(xmax_layout)
        x_layout.addWidget(xmin_group, 0)
        x_layout.addWidget(xmax_group, 0)
        x_group.setLayout(x_layout)

        # Y axis:
        y_group = QGroupBox("Along Y axis")
        y_group.setObjectName("y_group_" + str(idx))
        y_layout = QBoxLayout(QBoxLayout.TopToBottom)
        y_new_combo_by = QComboBox()
        yc = "y_combo" + str(idx)
        y_new_combo_by.setObjectName(yc)
        y_new_combo_by.addItem(PERIODIC_BC)
        y_new_combo_by.addItem(CONSTANT_BC)
        y_new_combo_by.addItem(CONSTANT_DERIVATIVE_BC)
        y_new_combo_by.setCurrentIndex(2)  # set to Constant derivative
        y_new_combo_by.currentIndexChanged.connect(self.y_bcTypeChanged)
        y_layout.addWidget(y_new_combo_by, 0)
        ymin_label = QLabel("Value at y = y.min")
        ymin_line_edit = QLineEdit("0.0")
        ymin_le = "y_min" + str(idx)
        ymin_line_edit.setObjectName(ymin_le)
        ymin_line_edit.textChanged.connect(self.checkIfNumber)
        ymax_label = QLabel("Value at y = y.max")
        ymax_line_edit = QLineEdit("0.0")
        ymax_line_edit.textChanged.connect(self.checkIfNumber)
        ymax_le = "y_max" + str(idx)

        if self.yDimSB.value() > 1:  # Check if lattice has y dir
            y_new_combo_by.setDisabled(False)
            ymin_line_edit.setDisabled(False)
            ymax_line_edit.setDisabled(False)
        else:
            y_new_combo_by.setDisabled(True)
            ymin_line_edit.setDisabled(True)
            ymax_line_edit.setDisabled(True)

        ymax_line_edit.setObjectName(ymax_le)
        ymin_group = QGroupBox("")
        ymin_layout = QBoxLayout(QBoxLayout.LeftToRight)
        ymin_layout.addWidget(ymin_label)
        ymin_layout.addWidget(ymin_line_edit)
        ymin_group.setLayout(ymin_layout)
        ymax_group = QGroupBox("")
        ymax_layout = QBoxLayout(QBoxLayout.LeftToRight)
        ymax_layout.addWidget(ymax_label)
        ymax_layout.addWidget(ymax_line_edit)
        ymax_group.setLayout(ymax_layout)
        y_layout.addWidget(ymin_group, 0)
        y_layout.addWidget(ymax_group, 0)
        y_group.setLayout(y_layout)

        # Z axis:
        z_group = QGroupBox("Along Z axis")
        z_group.setObjectName("z_group_" + str(idx))
        z_layout = QBoxLayout(QBoxLayout.TopToBottom)
        z_new_combo_bz = QComboBox()
        zc = "z_combo" + str(idx)
        z_new_combo_bz.setObjectName(zc)
        z_new_combo_bz.addItem(PERIODIC_BC)
        z_new_combo_bz.addItem(CONSTANT_BC)
        z_new_combo_bz.addItem(CONSTANT_DERIVATIVE_BC)
        z_new_combo_bz.setCurrentIndex(2)  # set to Constant derivative
        z_new_combo_bz.currentIndexChanged.connect(self.z_bcTypeChanged)
        z_layout.addWidget(z_new_combo_bz, 0)
        zmin_label = QLabel("Value at z = z.min")
        zmin_line_edit = QLineEdit("0.0")
        zmin_le = "z_min" + str(idx)
        zmin_line_edit.setObjectName(zmin_le)
        zmin_line_edit.textChanged.connect(self.checkIfNumber)
        zmax_label = QLabel("Value at z = z.max")
        zmax_line_edit = QLineEdit("0.0")
        zmax_line_edit.textChanged.connect(self.checkIfNumber)
        xmax_le = "z_max" + str(idx)
        z_val = self.zDimSB.value()  # Check if lattice has z dir
        if z_val > 1:
            z_new_combo_bz.setDisabled(False)
            zmin_line_edit.setDisabled(False)
            zmax_line_edit.setDisabled(False)
        else:
            z_new_combo_bz.setDisabled(True)
            zmin_line_edit.setDisabled(True)
            zmax_line_edit.setDisabled(True)

        zmax_line_edit.setObjectName(xmax_le)
        zmin_group = QGroupBox("")
        zmin_layout = QBoxLayout(QBoxLayout.LeftToRight)
        zmin_layout.addWidget(zmin_label)
        zmin_layout.addWidget(zmin_line_edit)
        zmin_group.setLayout(zmin_layout)
        zmax_group = QGroupBox("")
        zmax_layout = QBoxLayout(QBoxLayout.LeftToRight)
        zmax_layout.addWidget(zmax_label)
        zmax_layout.addWidget(zmax_line_edit)
        zmax_group.setLayout(zmax_layout)
        z_layout.addWidget(zmin_group, 0)
        z_layout.addWidget(zmax_group, 0)
        z_group.setLayout(z_layout)

        bc_layout.addWidget(x_group, 0)
        bc_layout.addWidget(y_group, 0)
        bc_layout.addWidget(z_group, 0)
        bc_group.setLayout(bc_layout)
        return bc_group

    def populate_pde_solver_entries(self):
        self.field_tab.clear() # clear the stuff
        self.cellTypeData = {}

        self.bcs_tab.clear()
        self.ics_tab.clear()

        for row in range(self.cellTypeTable.rowCount()):
            cell_type = str(self.cellTypeTable.item(row, 0).text())
           # print(cell_type, "hello")
            freeze = False
            if self.cellTypeTable.item(row, 1).checkState() == Qt.Checked:
                print("self.cellTypeTable.item(row,1).checkState()=", self.cellTypeTable.item(row, 1).checkState())
                freeze = True

            self.cellTypeData[cell_type] = [row, freeze]

        for solver_name, fields in self.diffusantDict.items():
            for idx, field in enumerate(fields):
                steadyState_solv: bool = False
                diff_secrete_table_cols: int = 8
                if (solver_name == SS_DIFF_SOLVER) or (solver_name == SS_DIFF_SOLVER_2D):
                    steadyState_solv = True
                    diff_secrete_table_cols = 6  # No Constant conc or Secrete on contact columns
                #if solver_name == REACT_DIFF_SOLVER_FE: # NOT implemented yet
                #    auto_scale: QCheckBox = QCheckBox("Autoscale diffusion")
                #    auto_scale.setToolTip("Optional auto time sub-stepping. Safe, but conservative")
                #    current: QLayout = self.diffusion_options_GBox.layout()
                #    current.addWidget(auto_scale, 0)
                new_bc_dialog: QGroupBox = self.getBC_Dialog(idx)  # Set BCs
                self.bcs_tab.insertTab(idx, new_bc_dialog, field)
                self.bcs_tab.currentChanged.connect(self.field_tab_changed)
                new_ic_dialog: QGroupBox = self.getIC_Dialog(idx)  # Set ICs:
                self.ics_tab.insertTab(idx, new_ic_dialog, field)
                self.ics_tab.currentChanged.connect(self.field_tab_changed)
                diff_secrete_table_widget = QTableWidget()
                vh = QHeaderView(Qt.Vertical)
                vh.hide()
                diff_secrete_table_widget.setVerticalHeader(vh)  # Hide row numbers
                diff_secrete_table_widget.setColumnCount(diff_secrete_table_cols)  # was 3

                cell_type_header = QTableWidgetItem("Cell or\n Area/Volume")
                cell_type_header.setToolTip("Chemical field behavior in Cell type or volume.")
                diff_secrete_table_widget.setHorizontalHeaderItem(0, cell_type_header)
                diff_coeff_header = QTableWidgetItem("Diffusion coeff\n (pixels^2 /mcs)")
                diff_decay_header = QTableWidgetItem("Decay coefficient\n (1/mcs)")
                const_sec_header = QTableWidgetItem("Secretion rate\n (amt/mcs/voxel)")
                if steadyState_solv:
                    diff_coeff_header.setToolTip("Steady-state solver uses only one global diffusion coef.")
                    diff_decay_header.setToolTip("Steady-state solver uses only one global decay coef.")
                    const_sec_header.setToolTip("Constant Secretion rate .")
                else:
                    const_sec_header.setToolTip(
                        "Constant Secretion rate or rate of secretion on contact with another cell.")
                diff_secrete_table_widget.setHorizontalHeaderItem(1, diff_coeff_header)
                diff_secrete_table_widget.setHorizontalHeaderItem(2, diff_decay_header)
                diff_secrete_table_widget.setHorizontalHeaderItem(3, const_sec_header)
                if steadyState_solv:
                    max_up_header = QTableWidgetItem("Max uptake by cell\n (amt/mcs/voxel)")
                    max_up_header.setToolTip("Maximum uptake of the field chemical by cell or volume")
                    diff_secrete_table_widget.setHorizontalHeaderItem(4, max_up_header)
                    rel_up_header = QTableWidgetItem("Relative uptake\n by cell/vol")
                    rel_up_header.setToolTip(
                        "Value between 0.0 and 1.0. Relative to actual field chemical concentration.")
                    diff_secrete_table_widget.setHorizontalHeaderItem(5, rel_up_header)
                else:
                    const_conc_sec_header = QTableWidgetItem("Constant conc\n field (amt/voxel)")
                    const_conc_sec_header.setToolTip("Chemical field kept at constant concentration.")
                    sec_on_contact_header = QTableWidgetItem("Secrete on contact\n with cell/vol")
                    sec_on_contact_header.setToolTip(
                        "Secrete on contact with another cell or volume: 'cell_type1, cell_type2' ")
                    diff_secrete_table_widget.setHorizontalHeaderItem(4, const_conc_sec_header)
                    diff_secrete_table_widget.setHorizontalHeaderItem(5, sec_on_contact_header)
                    max_up_header = QTableWidgetItem("Max uptake by cell\n (amt/mcs/voxel)")
                    max_up_header.setToolTip("Maximum uptake of the field chemical by cell or volume")
                    diff_secrete_table_widget.setHorizontalHeaderItem(6, max_up_header)
                    rel_up_header = QTableWidgetItem("Relative uptake\n by cell/vol")
                    rel_up_header.setToolTip(
                        "Value between 0.0 and 1.0. Relative to actual field chemical concentration.")
                    diff_secrete_table_widget.setHorizontalHeaderItem(7, rel_up_header)

              #  table_widget.horizontalHeader().setStretchLastSection(True)
                diff_secrete_table_widget.horizontalHeader().setSectionResizeMode(
                    QHeaderView.Stretch)
                # Global diffusion settings in first row:
                diff_secrete_table_widget.insertRow(diff_secrete_table_widget.rowCount())
                global_name = GLOBAL_DIFFUSION_LABEL
                global_val_decay_coefficient = '0.00001'
                item = QTableWidgetItem(global_name)
                item.setTextAlignment(Qt.AlignCenter)
                diff_secrete_table_widget.setItem(0, 0, item)
                default_value_diffusion_coefficient = '0.01'
                diff_item = QTableWidgetItem(default_value_diffusion_coefficient)
                diff_item.setTextAlignment(Qt.AlignCenter)
                diff_secrete_table_widget.setItem(0, 1, diff_item)
                decay_item = QTableWidgetItem(global_val_decay_coefficient)
                decay_item.setTextAlignment(Qt.AlignCenter)
                diff_secrete_table_widget.setItem(0, 2, decay_item)
                const_sec_item = QTableWidgetItem("n/a")
                const_sec_item.setTextAlignment(Qt.AlignCenter)
                diff_secrete_table_widget.setItem(0, 3, const_sec_item)
                if steadyState_solv:
                    const_item3 = QTableWidgetItem("n/a")
                    const_item3.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(0, 4, const_item3)
                    const_item4 = QTableWidgetItem("n/a")
                    # const_item4.setFlags(not Qt.ItemIsEnabled)
                    const_item4.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(0, 5, const_item4)
                else:
                    const_item = QTableWidgetItem("n/a")
                    const_item.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(0, 4, const_item)
                    const_item2 = QTableWidgetItem("n/a")
                    const_item2.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(0, 5, const_item2)
                    const_item3 = QTableWidgetItem("n/a")
                    const_item3.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(0, 6, const_item3)
                    const_item4 = QTableWidgetItem("n/a")
                    const_item4.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(0, 7, const_item4)

                # now list all cell types:
                for row, (type_name, type_data) in enumerate(self.cellTypeData.items()):
                    diff_secrete_table_widget.insertRow(diff_secrete_table_widget.rowCount())
                    if steadyState_solv:
                        default_value_diffusion_coefficient = 'n/a'
                        default_value_decay_coefficient = 'n/a'
                    else:
                        default_value_decay_coefficient = '0.001'
                    default_value_const_secretion = '-'
                    default_value_const_conc_secretion = '-'
                    default_value_sec_on_contact = '-'
                    default_value_max_uptake = '-'
                    default_value_rel_uptake = '-'

                    item = QTableWidgetItem(type_name)
                    item.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(row + 1, 0, item)
                    diff_item = QTableWidgetItem(default_value_diffusion_coefficient)
                    diff_item.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(row + 1, 1, diff_item)
                    decay_item = QTableWidgetItem(default_value_decay_coefficient)
                    decay_item.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(row + 1, 2, decay_item)
                    const_sec_item = QTableWidgetItem(default_value_const_secretion)
                    const_sec_item.setTextAlignment(Qt.AlignCenter)
                    diff_secrete_table_widget.setItem(row + 1, 3, const_sec_item)
                    const_conc_sec_item = QTableWidgetItem(default_value_const_conc_secretion)
                    const_conc_sec_item.setTextAlignment(Qt.AlignCenter)
                    if steadyState_solv:
                        max_uptake_item = QTableWidgetItem(default_value_max_uptake)
                        max_uptake_item.setTextAlignment(Qt.AlignCenter)
                        diff_secrete_table_widget.setItem(row + 1, 4, max_uptake_item)
                        rel_uptake_item = QTableWidgetItem(default_value_rel_uptake)
                        rel_uptake_item.setTextAlignment(Qt.AlignCenter)
                        diff_secrete_table_widget.setItem(row + 1, 5, rel_uptake_item)
                    else:
                        diff_secrete_table_widget.setItem(row + 1, 4, const_conc_sec_item)
                        sec_on_contact_item = QTableWidgetItem(default_value_sec_on_contact)
                        sec_on_contact_item.setTextAlignment(Qt.AlignCenter)
                        diff_secrete_table_widget.setItem(row + 1, 5, sec_on_contact_item)
                        max_uptake_item = QTableWidgetItem(default_value_max_uptake)
                        max_uptake_item.setTextAlignment(Qt.AlignCenter)
                        diff_secrete_table_widget.setItem(row + 1, 6, max_uptake_item)
                        rel_uptake_item = QTableWidgetItem(default_value_rel_uptake)
                        rel_uptake_item.setTextAlignment(Qt.AlignCenter)
                        diff_secrete_table_widget.setItem(row + 1, 7, rel_uptake_item)
                tab_title: str = field + ": " + solver_name
                self.field_tab.insertTab(idx, diff_secrete_table_widget, tab_title)
                self.field_tab.currentChanged.connect(self.field_tab_changed)
                self.field_table_dict[field] = diff_secrete_table_widget

    # Secretion on contact: Expect a comma separated string of cell types to check: 'cell1, cell2, cell3'
    def checkIfValidCellType(self, cell_types_str) -> bool:
        type_list = cell_types_str.split(",")
        for new_type in type_list:
            found = False
            for row in range(self.cellTypeTable.rowCount()):
                valid_cell_type = str(self.cellTypeTable.item(row, 0).text())
                if new_type.strip().lower() == valid_cell_type.strip().lower():
                    found = True
            if not found:
                print("Cell type not found: " + str(new_type))
                return False
        return True

        #  Returns dictionary of chemical field secretion values, returns False if data bad
    def getDiffusionSecretion_Values(self, field_table: QTableWidget, field_str, solver: str) -> dict[str, list]:
        secretion_diffusion_data: dict[str, list] = {}  # format {field:[secrDict1,secrDict2,...]}
        ss_solver = False
        if (solver == SS_DIFF_SOLVER) or (solver == SS_DIFF_SOLVER_2D):
            ss_solver = True

        for row in range(field_table.rowCount()):
            secretion_type = "-"
            rate = 0.0  # holds value of secretion rate for all three types of field secretion
            cell_type = str(field_table.item(row, 0).text())
            if not row == 0 and not cell_type == GLOBAL_DIFFUSION_LABEL:  # first row contains default diffusion values
                if not ss_solver:
                    const_conc_sec = str(field_table.item(row, 4).text())
                    on_contact_with = str(field_table.item(row, 5).text())
                    try:
                        if not const_conc_sec == "-":
                            rate = float(
                                const_conc_sec)  # value stored in rate var even though it is a constant conc.
                            secretion_type = "constant concentration"
                    except Exception:
                        rate = 0.0
                try:
                    uniform_rate = str(field_table.item(row, 3).text())
                    if not uniform_rate == "-":
                        rate = float(str(field_table.item(row, 3).text()))
                        secretion_type = "uniform"
                except Exception:
                    rate = 0.0
                try:
                    if not ss_solver:
                        max_uptake = float(str(field_table.item(row, 6).text()))
                    else:
                        max_uptake = float(str(field_table.item(row, 4).text()))
                    if max_uptake < 0.0:
                        max_uptake = 0.0
                except Exception:
                    max_uptake = 0.0
                try:
                    if not ss_solver:
                        rel_uptake = float(str(field_table.item(row, 7).text()))
                    else:
                        rel_uptake = float(str(field_table.item(row, 5).text()))
                    if rel_uptake < 0.0:
                        rel_uptake = 0.0
                    elif rel_uptake > 1.0:
                        rel_uptake = 1.0
                except Exception:
                    rel_uptake = 0.0

                diff_fe_secr_dict = {}
                diff_fe_secr_dict["CellType"] = cell_type
                diff_fe_secr_dict["MaxUptake"] = max_uptake
                diff_fe_secr_dict["RelativeUptakeRate"] = rel_uptake
                diff_fe_secr_dict["Rate"] = rate
                if not ss_solver:
                    if not on_contact_with == "-":
                        if self.checkIfValidCellType(on_contact_with):
                            diff_fe_secr_dict["OnContactWith"] = on_contact_with
                            secretion_type = "on contact"
                        else:
                            msg = '''
                            For 'Secrete on contact': one of the cell types listed is invalid. 
                            Make sure cell type list is comma separated.
                            '''
                            QMessageBox.warning(self, "Invalid Cell type", msg, QMessageBox.Ok)
                            print("msg")
                            return {"Invalid Cell type": [-1]}
                        if uniform_rate == "-":
                            msg = '''
                            For 'Secrete on contact': Please add a value to 
                            the 'Secretion rate' column.
                            '''
                            QMessageBox.warning(self, "Invalid Secretion rate", msg, QMessageBox.Ok)
                            return {"Invalid Secretion rate": [-1]}
                diff_fe_secr_dict["SecretionType"] = secretion_type
                try:
                    secretion_diffusion_data[field_str].append(diff_fe_secr_dict)
                except LookupError:
                    secretion_diffusion_data[field_str] = [diff_fe_secr_dict]
        return secretion_diffusion_data


    #  Returns diffusion values dict
    def getCurrentDiffusionFE_Values(self):
        diffusion_vals_dict = {}
        for solver_name, fields in self.diffusantDict.items():
            for idx, field in enumerate(fields):
                diff_table = self.field_table_dict[field]
                diffusant_data = {}
                vol_coeffs = {}
                for row in range(diff_table.rowCount()):
                    cell_type_vol = diff_table.item(row, 0).text()
                    coef = diff_table.item(row, 1).text()
                    decay = diff_table.item(row, 2).text()
                    if row == 0:
                        vol_coeffs.update({cell_type_vol: {"GlobalDiffusionCoefficient": coef, "GlobalDecayCoefficient": decay}})
                    else:
                        vol_coeffs.update({cell_type_vol: {"DiffusionCoefficient": coef, "DecayCoefficient": decay}})
                diffusant_data["Coefficients"] = vol_coeffs
                for widget in self.bcs_tab.children():  # Get BCs
                    group_boxes = widget.findChildren(QGroupBox)
                    all_bcs = {}
                    for child in group_boxes:
                        group_bx_name = ""
                        if isinstance(child, QGroupBox):
                            combo_boxes = child.findChildren(QComboBox)
                            group_bx_name = child.objectName()
                            if group_bx_name.endswith("_" + str(idx)):
                                for c_box in combo_boxes:
                                    bcs = {}
                                    boundary_type = ''
                                    axis_dir = ""
                                    if "x" in c_box.objectName():
                                        axis_dir = "x_"
                                    else:
                                        if "y" in c_box.objectName():
                                            axis_dir = "y_"
                                        else:
                                            axis_dir = "z_"
                                    if c_box.currentIndex() == 0:  # periodic boundary
                                        boundary_type = "Periodic"
                                    else:
                                        if c_box.currentIndex() == 1:  # constant value boundary
                                            boundary_type = "ConstantValue"  # (Dirichlet)
                                        else:                          # Constant derivative boundary
                                            boundary_type = "ConstantDerivative"  # (von Neumann)
                                    lines = child.findChildren(QLineEdit)
                                    axis_vals = {}
                                    for new_line in lines:
                                        if axis_dir in new_line.objectName():
                                            axis_vals.update({new_line.objectName(): new_line.text()})
                                    bcs[boundary_type] = axis_vals
                                    axial_bc = {group_bx_name: bcs}
                                    all_bcs.update(axial_bc)

                        diffusant_bcs = {"BoundaryConditions": all_bcs}
                    diffusant_data.update(diffusant_bcs)

                for widget in self.ics_tab.children():  # Get ICs
                    group_boxes = widget.findChildren(QGroupBox)
                    all_ics = {}
                    for group in group_boxes:
                        ic_file = False
                        diffusant_ic = {}
                        group_bx_name = group.objectName()
                        if group_bx_name.endswith("_" + str(idx)):
                            radio_buttons = group.findChildren(QRadioButton)
                            for rb in radio_buttons:
                                if rb.isChecked():
                                    ic_file = True
                            lines = group.findChildren(QLineEdit)
                            for line in lines:
                                if ic_file:
                                    if "ic_file" in line.objectName():
                                        diffusant_ic = {"ConcentrationFileName": line.text()}
                                else:
                                    if "ic_val" in line.objectName():
                                        diffusant_ic = {"InitialConcentrationExpression": line.text()}
                                all_ics.update(diffusant_ic)
                        diffusant_ic = {"InitialConditions": all_ics}
                    diffusant_data.update(diffusant_ic)
                diffusion_vals_dict[field] = diffusant_data

            print(diffusion_vals_dict)
        return diffusion_vals_dict


    def is_path_creatable(self, pathname: str) -> bool:
        '''
        `True` if the current user has sufficient permissions to create the passed
        pathname; `False` otherwise.
        '''
        # Parent directory of the passed path. If empty, we substitute the current
        # working directory (CWD) instead.
        dirname = os.path.dirname(pathname) or os.getcwd()
        return os.access(dirname, os.W_OK)

    def is_path_exists_or_creatable(self, pathname: str) -> bool:
        '''
        `True` if the passed pathname is a valid pathname for the current OS _and_
        either currently exists or is hypothetically creatable; `False` otherwise.
        '''
        try:
            path = os.path.dirname(pathname)  # confirm there is no filename appended to the end of dir path
            return (os.path.exists(path) or self.is_path_creatable(path))
        # Report failure on non-fatal filesystem complaints (e.g., connection
        # timeouts, permissions issues) implying this path to be inaccessible. All
        # other exceptions are unrelated fatal issues and should not be caught here.
        except OSError:
            return False

    def validateCurrentPage(self) -> bool:

        print("THIS IS VALIDATE FOR PAGE ", self.currentId)

        if self.currentId() == self.get_page_id_by_name("CompuCell3D Simulation Wizard"):
            directory = str(self.dirLE.text()).strip()
            name = str(self.nameLE.text()).strip()

#            self.setPage(self.get_page_id_by_name("PythonScript"), self.get_page_by_name("PythonScript"))  # TODO ???
            self.setPage(self.pageDict["Configuration Complete!"][1], self.pageDict["Configuration Complete!"][0])

            if directory == "" or name == "":
                QMessageBox.warning(self, "Missing information",
                                    "Please specify name of the simulation and directory where it should be written to",
                                    QMessageBox.Ok)
                return False

            elif not name.isidentifier():
                msg = """
                Please specifying a name that meets with following criteria
                
                1. Consists only of letters, numbers and/or `_`. 
                2. Starts with either a letter or '_'
                """
                QMessageBox.warning(self, "Invalid simulation name", msg, QMessageBox.Ok)
                return False

            else:
                if directory != "":
                    self.plugin.configuration.setSetting("RecentNewProjectDir", directory)
                    print("CHECKING DIRECTORY ")

                    # checking if directory is writeable
                    project_dir = os.path.abspath(directory)

                    if not os.path.exists(project_dir):
                        try:
                            os.makedirs(project_dir)
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise OSError(f'Could not create directory {project_dir}')

                    if not os.access(project_dir, os.W_OK):
                        print("CHECKING DIRECTORY ")
                        QMessageBox.warning(self, "Write permission Error",
                                            "You do not have write permissions to %s directory. "
                                            "This error also appears when creating project that has non-ascii "
                                            "characters (either in project name or in project directory). " % (
                                                os.path.abspath(directory)), QMessageBox.Ok)

                        return False

                return True

        # general properties
        if self.currentId() == self.get_page_id_by_name(SIMULATION_PROPERTIES_PAGE_NAME):

            if self.piffRB.isChecked() and str(self.piffLE.text()).strip() == '':
                QMessageBox.warning(self, "Missing information", "Please specify name of the PIFF file", QMessageBox.Ok)

                return False

            sim_3d_flag = False

            if self.xDimSB.value() > 1 and self.yDimSB.value() > 1 and self.zDimSB.value() > 1:
                sim_3d_flag = True

            if sim_3d_flag:

                self.lengthConstraintLocalFlexCHB.setChecked(False)
                self.lengthConstraintLocalFlexCHB.hide()

            else:
                self.lengthConstraintLocalFlexCHB.show()

            if str(self.latticeTypeCB.currentText()) == "Square" and not sim_3d_flag:
                self.connect2DCHB.show()

            else:
                self.connect2DCHB.hide()
                self.connect2DCHB.setChecked(False)

            return True
        if self.currentId() == self.get_page_id_by_name(CELL_TYPE_SPEC_PAGE_NAME):
            # we only extract types from table here - it is not a validation strictly speaking
            # extract cell type information form the table

            self.typeTable = []

            for row in range(self.cellTypeTable.rowCount()):
                cell_type = str(self.cellTypeTable.item(row, 0).text())
                freeze = False

                if self.cellTypeTable.item(row, 1).checkState() == Qt.Checked:
                    print("self.cellTypeTable.item(row,1).checkState()=", self.cellTypeTable.item(row, 1).checkState())
                    freeze = True

                self.typeTable.append([cell_type, freeze])

            # at this point we can fill all the cell types and fields widgets on subsequent pages

            self.chemCellTypeCB.clear()
            self.chemTowardsCellTypeCB.clear()
            self.chemFieldCB.clear()

            print("Clearing Combo boxes")
            for cell_type_tuple in self.typeTable:

                if str(cell_type_tuple[0]) != "Medium":
                    self.chemCellTypeCB.addItem(cell_type_tuple[0])

                self.chemTowardsCellTypeCB.addItem(cell_type_tuple[0])

            # secretion plugin
            self.secrFieldCB.clear()
            self.secrCellTypeCB.clear()
            self.secrOnContactCellTypeCB.clear()

            for cell_type_tuple in self.typeTable:
                self.secrCellTypeCB.addItem(cell_type_tuple[0])
                self.secrOnContactCellTypeCB.addItem(cell_type_tuple[0])

            return True

        if self.currentId() == self.get_page_id_by_name(CELL_PROP_BEHAVIORS_PAGE_NAME):
            print(self.get_page_by_name)

         #   if self.secretionCHB.isChecked():  # Remove if no longer needed
         #       self.setPage(self.get_page_id_by_name("Secretion Plugin"), self.get_page_by_name("Secretion Plugin"))

         #   else:
            self.removePage(self.get_page_id_by_name(SECRETION_PAGE_NAME))

            if self.chemotaxisCHB.isChecked():
                self.setPage(self.get_page_id_by_name(CHEMOTAXIS_PAGE_NAME), self.get_page_by_name(CHEMOTAXIS_PAGE_NAME))

            else:
                self.removePage(self.get_page_id_by_name(CHEMOTAXIS_PAGE_NAME))

            if self.contactMultiCadCHB.isChecked():
                self.setPage(self.get_page_id_by_name(CONTACT_MULTICAD_PAGE_NAME), self.get_page_by_name(CONTACT_MULTICAD_PAGE_NAME))

            else:
                self.removePage(self.get_page_id_by_name(CONTACT_MULTICAD_PAGE_NAME))

            if self.adhesionFlexCHB.isChecked():
                self.setPage(self.get_page_id_by_name(ADHESION_FLEX_PAGE_NAME), self.get_page_by_name(ADHESION_FLEX_PAGE_NAME))
            else:
                self.removePage(self.get_page_id_by_name(ADHESION_FLEX_PAGE_NAME))
            return True

    #    chem_field_id = self.get_page_id_by_name(CHEMICAL_FIELDS_DIFFUSANTS_PAGE_NAME)
        if self.currentId() == self.get_page_id_by_name(CHEMICAL_FIELDS_DIFFUSANTS_PAGE_NAME):
            # we only extract diffusants from table here - it is not a validation strictly speaking
            self.diffusantDict = {}
            for row in range(self.fieldTable.rowCount()):
                field = str(self.fieldTable.item(row, 0).text())
                solver = str(self.fieldTable.item(row, 1).text())

                try:
                    self.diffusantDict[solver].append(field)
                except LookupError:
                    self.diffusantDict[solver] = [field]

            for solver_name, fields in self.diffusantDict.items():
                for field_name in fields:
                    self.chemFieldCB.addItem(field_name)

            for solver_name, fields in self.diffusantDict.items():
                for field_name in fields:
                    self.secrFieldCB.addItem(field_name)

             # DiffusionFE secretion plugin ( _2 )
            self.secrFieldCB_2.clear()
            self.secrCellTypeCB_2.clear()
            self.secrOnContactCellTypeCB_2.clear()

            for cell_type_tuple in self.typeTable:
                self.secrCellTypeCB_2.addItem(cell_type_tuple[0])
                self.secrOnContactCellTypeCB_2.addItem(cell_type_tuple[0])
        #    for solver_name, fields in self.diffusantDict.items():  # remove if do not need anymore
        #        for field_name in fields:
        #            self.secrFieldCB_2.addItem(field_name)

            if len(self.diffusantDict.items()) > 0:  # VALIDATE ICs and BCs,
                solver_found = False
                for solver_name, fields in self.diffusantDict.items():  # Check for use of DiffusionSolverFE
                    if solver_name in (DIFFUSION_SOLVER_FE, SS_DIFF_SOLVER, SS_DIFF_SOLVER_2D) and not solver_found:
                    #if (solver_name == DIFFUSION_SOLVER_FE or REACT_DIFF_SOLVER_FE or REACT_DIFF_SOLVER_FVM) and not solver_found:
                        solver_found = True
                        self.setPage(self.get_page_id_by_name(DIFFUSION_WIZARD_PAGE_NAME), self.get_page_by_name(DIFFUSION_WIZARD_PAGE_NAME))
                       # self.setPage(self.get_page_id_by_name(SECRETION_DIFFUSION_FE_PAGE_NAME), self.get_page_by_name(SECRETION_DIFFUSION_FE_PAGE_NAME))
                self.populate_pde_solver_entries()
            else:
                self.removePage(self.get_page_id_by_name(DIFFUSION_WIZARD_PAGE_NAME))
              #  self.removePage(self.get_page_id_by_name(SECRETION_DIFFUSION_FE_PAGE_NAME)) # remove if do not need anymore
            return True

        if self.currentId() == self.get_page_by_name(CONTACT_MULTICAD_PAGE_NAME):
            if not self.cmcTable.rowCount():

                QMessageBox.warning(self, "Missing information",
                                    "Please specify at least one cadherin name to be used in ContactMultiCad plugin",
                                    QMessageBox.Ok)

                return False

            else:
                return True

        if self.currentId() == self.get_page_id_by_name(DIFFUSION_WIZARD_PAGE_NAME):
            # we only extract data from page here - it is not a validation strictly speaking
            self.diffusion_vals_dict = self.getCurrentDiffusionFE_Values()
            # Get secretion values and uptake values
            for solver_name, fields in self.diffusantDict.items():
                for field_name in fields:
                    results = self.getDiffusionSecretion_Values(self.field_table_dict[field_name], field_name, solver_name)
                    for key in results:
                        if "Invalid" in key and -1 in results[key]:
                            return False  # secretion values bad

                    self.diffusion_vals_dict[field_name]["Secretion"] = results
                    #self.diffusion_vals_dict[field_name]["Secretion"] = \
                    #    self.getDiffusionSecretion_Values(self.field_table_dict[field_name], field_name)

        if self.currentId() == self.get_page_by_name("AdhesionFlex Plugin"):

            if not self.afTable.rowCount():

                QMessageBox.warning(self, "Missing information",
                                    "Please specify at least one adhesion molecule name "
                                    "to be used in AdhesionFlex plugin",
                                    QMessageBox.Ok)

                return False

            else:

                return True

        return True

    def makeProjectDirectories(self, dir, name):

        try:

            self.mainProjDir = os.path.join(dir, name)

            self.plugin.makeDirectory(self.mainProjDir)

            self.simulationFilesDir = os.path.join(self.mainProjDir, "Simulation")

            self.plugin.makeDirectory(self.simulationFilesDir)



        except IOError as e:

            raise IOError

        return

    def generateNewProject(self):

        directory = str(self.dirLE.text()).strip()

        directory = os.path.abspath(directory)

        name = str(self.nameLE.text()).strip()

        self.makeProjectDirectories(directory, name)

        self.generalPropertiesDict = {}

        self.generalPropertiesDict["Dim"] = [self.xDimSB.value(), self.yDimSB.value(), self.zDimSB.value()]
        self.generalPropertiesDict["MembraneFluctuations"] = float(str(self.membraneFluctuationsLE.text()))
        self.generalPropertiesDict["NeighborOrder"] = self.neighborOrderSB.value()
        self.generalPropertiesDict["MCS"] = self.mcsSB.value()
        self.generalPropertiesDict["LatticeType"] = str(self.latticeTypeCB.currentText())
        self.generalPropertiesDict["SimulationName"] = name
        self.generalPropertiesDict["BoundaryConditions"] = OrderedDict()
        self.generalPropertiesDict["BoundaryConditions"]['x'] = self.xbcCB.currentText()
        self.generalPropertiesDict["BoundaryConditions"]['y'] = self.ybcCB.currentText()
        self.generalPropertiesDict["BoundaryConditions"]['z'] = self.zbcCB.currentText()
        self.generalPropertiesDict["Initializer"] = ["uniform", None]

        if self.blobRB.isChecked():

            self.generalPropertiesDict["Initializer"] = ["blob", None]

        elif self.piffRB.isChecked():

            piff_path = str(self.piffLE.text()).strip()
            self.generalPropertiesDict["Initializer"] = ["piff", piff_path]

            # trying to copy piff file into simulation dir of the project directory
            try:

                shutil.copy(piff_path, self.simulationFilesDir)

                base_piff_path = os.path.basename(piff_path)
                relative_piff_path = os.path.join(self.simulationFilesDir, base_piff_path)
                self.generalPropertiesDict["Initializer"][1] = self.getRelativePathWRTProjectDir(relative_piff_path)

                print("relativePathOF PIFF=", self.generalPropertiesDict["Initializer"][1])

            except shutil.Error:
                QMessageBox.warning(self, "Cannot copy PIFF file",
                                    "Cannot copy PIFF file into project directory. "
                                    "Please check if the file exists and that you have necessary write permissions",
                                    QMessageBox.Ok)

            except IOError as e:
                QMessageBox.warning(self, "IO Error", e.__str__(), QMessageBox.Ok)

        self.cellTypeData = {}

        # extract cell type information form the table
        for row in range(self.cellTypeTable.rowCount()):

            cell_type = str(self.cellTypeTable.item(row, 0).text())
            freeze = False

            if self.cellTypeTable.item(row, 1).checkState() == Qt.Checked:
                print("self.cellTypeTable.item(row,1).checkState()=", self.cellTypeTable.item(row, 1).checkState())
                freeze = True

            self.cellTypeData[cell_type] = [row, freeze]

        self.af_data = {}

        for row in range(self.afTable.rowCount()):
            molecule = str(self.afTable.item(row, 0).text())

            self.af_data[row] = molecule

        self.af_formula = str(self.bindingFormulaLE.text()).strip()

        cmc_table = []

        for row in range(self.cmcTable.rowCount()):
            cadherin = str(self.cmcTable.item(row, 0).text())

            cmc_table.append(cadherin)

        self.pde_field_data = {}  # Need to add all the new settings/values to this
        #  Work through table then get ICs and BCs, finally secretion table
        for row in range(self.fieldTable.rowCount()):
            chem_field_name = str(self.fieldTable.item(row, 0).text())

            solver_name = str(self.fieldTable.item(row, 1).text())

            self.pde_field_data[chem_field_name] = solver_name

        try:
            solver_name
        except NameError:
            solver_name = None
    #    if solver_name == DIFFUSION_SOLVER_FE:  # Remove this section if do not need anymore
            #  DiffusionFE Secretion:

     #       secretion_diffusion_data = {}  # format {field:[secrDict1,secrDict2,...]}
     #       for row in range(self.secretion_DiffusionFE_Table.rowCount()):

     #           secr_field_name = str(self.secretion_DiffusionFE_Table.item(row, 0).text())
     #           cell_type = str(self.secretion_DiffusionFE_Table.item(row, 1).text())

     #           try:
     #               rate = float(str(self.secretion_DiffusionFE_Table.item(row, 2).text()))
     #           except Exception:
     #               rate = 0.0

     #           on_contact_with = str(self.secretion_DiffusionFE_Table.item(row, 3).text())
     #           secretion_type = str(self.secretion_DiffusionFE_Table.item(row, 4).text())

      #          diff_fe_secr_dict = {}
      #          diff_fe_secr_dict["CellType"] = cell_type
      #          diff_fe_secr_dict["Rate"] = rate
      #          diff_fe_secr_dict["OnContactWith"] = on_contact_with
      #          diff_fe_secr_dict["SecretionType"] = secretion_type

      #          try:
      #              secretion_diffusion_data[secr_field_name].append(diff_fe_secr_dict)
      #          except LookupError:
      #              secretion_diffusion_data[secr_field_name] = [diff_fe_secr_dict]
      #      for field in secretion_diffusion_data:
      #          self.diffusion_vals_dict[field]["Secretion"] = secretion_diffusion_data[field]

        self.secretion_data = {}  # format {field:[secrDict1,secrDict2,...]}

        for row in range(self.secretionTable.rowCount()):

            secr_field_name = str(self.secretionTable.item(row, 0).text())
            cell_type = str(self.secretionTable.item(row, 1).text())

            try:
                rate = float(str(self.secretionTable.item(row, 2).text()))
            except Exception:
                rate = 0.0

            on_contact_with = str(self.secretionTable.item(row, 3).text())
            secretion_type = str(self.secretionTable.item(row, 4).text())

            secr_dict = {}
            secr_dict["CellType"] = cell_type
            secr_dict["Rate"] = rate
            secr_dict["OnContactWith"] = on_contact_with
            secr_dict["SecretionType"] = secretion_type

            try:
                self.secretion_data[secr_field_name].append(secr_dict)
            except LookupError:
                self.secretion_data[secr_field_name] = [secr_dict]

        self.chemotaxisData = {}  # format {field:[chemDict1,chemDict2,...]}

        for row in range(self.chamotaxisTable.rowCount()):
            chem_field_name = str(self.chamotaxisTable.item(row, 0).text())

            cell_type = str(self.chamotaxisTable.item(row, 1).text())

            try:
                lambda_ = float(str(self.chamotaxisTable.item(row, 2).text()))
            except Exception:
                lambda_ = 0.0

            chemotax_towards = str(self.chamotaxisTable.item(row, 3).text())

            try:
                sat_coef = float(str(self.chamotaxisTable.item(row, 4).text()))
            except Exception:
                sat_coef = 0.0

            chemotaxis_type = str(self.chamotaxisTable.item(row, 5).text())
            chem_dict = {}
            chem_dict["CellType"] = cell_type
            chem_dict["Lambda"] = lambda_
            chem_dict["ChemotaxTowards"] = chemotax_towards
            chem_dict["SatCoef"] = sat_coef
            chem_dict["ChemotaxisType"] = chemotaxis_type

            try:
                self.chemotaxisData[chem_field_name].append(chem_dict)
            except LookupError:
                self.chemotaxisData[chem_field_name] = [chem_dict]

        # constructing Project XMl Element
        simulation_element = ElementCC3D("Simulation", {"version": cc3d.__version__})
        xml_generator = CC3DMLGeneratorBase(self.simulationFilesDir, name)

        self.generateXML(xml_generator)

        # end of generate XML ------------------------------------------------------------------------------------

        if self.pythonXMLRB.isChecked():
            xml_file_name = os.path.join(self.simulationFilesDir, name + ".xml")
            xml_generator.saveCC3DXML(xml_file_name)
            simulation_element.ElementCC3D("XMLScript", {"Type": "XMLScript"},

                                          self.getRelativePathWRTProjectDir(xml_file_name))

            # end of generate XML ------------------------------------------------------------------------------------

        if self.pythonXMLRB.isChecked() or self.pythonOnlyRB.isChecked():
            # generate Python ------------------------------------------------------------------------------------

            python_generator = CC3DPythonGenerator(xml_generator)
            python_generator.set_python_only_flag(self.pythonOnlyRB.isChecked())

            self.generateSteppablesCode(python_generator)

            # before calling generateMainPythonScript we have to call generateSteppablesCode
            # that generates also steppable registration lines
            python_generator.generate_main_python_script()
            simulation_element.ElementCC3D("PythonScript", {"Type": "PythonScript"},
                                           self.getRelativePathWRTProjectDir(python_generator.mainPythonFileName))

            simulation_element.ElementCC3D("Resource", {"Type": "Python"},
                                           self.getRelativePathWRTProjectDir(python_generator.steppablesPythonFileName))

            # end of generate Python ---------------------------------------------------------------------------------
        # including PIFFile in the .cc3d project description
        if self.generalPropertiesDict["Initializer"][0] == "piff":
            simulation_element.ElementCC3D("PIFFile", {}, self.generalPropertiesDict["Initializer"][1])

        # save Project file
        proj_file_name = os.path.join(self.mainProjDir, name + ".cc3d")

        # simulationElement.CC3DXMLElement.saveXML(projFileName)
        proj_file = open(proj_file_name, 'w')
        proj_file.write('%s' % simulation_element.CC3DXMLElement.getCC3DXMLElementString())
        proj_file.close()

        # open newly created project in the ProjectEditor
        self.plugin.openCC3Dproject(proj_file_name)

    def generateSteppablesCode(self, pythonGenerator):

        if self.growthCHB.isChecked():
            pythonGenerator.generate_growth_steppable()

        if self.mitosisCHB.isChecked():
            pythonGenerator.generate_mitosis_steppable()

        if self.deathCHB.isChecked():
            pythonGenerator.generate_death_steppable()

        pythonGenerator.generate_vis_plot_steppables()

        pythonGenerator.generate_steppable_python_script()

        pythonGenerator.generate_steppable_registration_lines()

    def generateXML(self, generator):
        cell_type_dict = self.cellTypeData
        args = []

        kwds = {}

        kwds['insert_root_element'] = generator.cc3d
        kwds['data'] = cell_type_dict
        kwds['generalPropertiesData'] = self.generalPropertiesDict
        kwds['afData'] = self.af_data
        kwds['formula'] = self.af_formula
        kwds['chemotaxisData'] = self.chemotaxisData
        kwds['pdeFieldData'] = self.pde_field_data
        kwds['secretionData'] = self.secretion_data
        kwds['diffusantData'] = self.diffusion_vals_dict

        generator.generateMetadataSimulationProperties(*args, **kwds)

        generator.generatePottsSection(*args, **kwds)

        generator.generateCellTypePlugin(*args, **kwds)

        if self.volumeFlexCHB.isChecked():
            generator.generateVolumeFlexPlugin(*args, **kwds)

        if self.surfaceFlexCHB.isChecked():
            generator.generateSurfaceFlexPlugin(*args, **kwds)

        if self.volumeLocalFlexCHB.isChecked():
            generator.generateVolumeLocalFlexPlugin(*args, **kwds)

        if self.surfaceLocalFlexCHB.isChecked():
            generator.generateSurfaceLocalFlexPlugin(*args, **kwds)

        if self.extPotCHB.isChecked():
            generator.generateExternalPotentialPlugin(*args, **kwds)

        if self.extPotLocalFlexCHB.isChecked():
            generator.generateExternalPotentialLocalFlexPlugin(*args, **kwds)

        if self.comCHB.isChecked():
            generator.generateCenterOfMassPlugin(*args, **kwds)

        if self.neighborCHB.isChecked():
            generator.generateNeighborTrackerPlugin(*args, **kwds)

        if self.momentOfInertiaCHB.isChecked():
            generator.generateMomentOfInertiaPlugin(*args, **kwds)

        if self.pixelTrackerCHB.isChecked():
            generator.generatePixelTrackerPlugin(*args, **kwds)

        if self.boundaryPixelTrackerCHB.isChecked():
            generator.generateBoundaryPixelTrackerPlugin(*args, **kwds)

        if self.contactCHB.isChecked():
            generator.generateContactPlugin(*args, **kwds)

        if self.compartmentCHB.isChecked():
            generator.generateCompartmentPlugin(*args, **kwds)

        if self.internalContactCB.isChecked():
            generator.generateContactInternalPlugin(*args, **kwds)

        if self.contactLocalProductCHB.isChecked():
            generator.generateContactLocalProductPlugin(*args, **kwds)

        if self.fppCHB.isChecked():
            generator.generateFocalPointPlasticityPlugin(*args, **kwds)

        if self.elasticityCHB.isChecked():
            generator.generateElasticityTrackerPlugin(*args, **kwds)

            generator.generateElasticityPlugin(*args, **kwds)

        if self.adhesionFlexCHB.isChecked():
            generator.generateAdhesionFlexPlugin(*args, **kwds)

        if self.chemotaxisCHB.isChecked():
            generator.generateChemotaxisPlugin(*args, **kwds)

        if self.lengthConstraintCHB.isChecked():
            generator.generateLengthConstraintPlugin(*args, **kwds)

        if self.lengthConstraintLocalFlexCHB.isChecked():
            generator.generateLengthConstraintLocalFlexPlugin(*args, **kwds)

        if self.connectGlobalCHB.isChecked():
            generator.generateConnectivityGlobalPlugin(*args, **kwds)

        if self.connectGlobalByIdCHB.isChecked():
            generator.generateConnectivityGlobalByIdPlugin(*args, **kwds)

        if self.connect2DCHB.isChecked():
            generator.generateConnectivityPlugin(*args, **kwds)

     #   if self.secretionCHB.isChecked():  # remove if not needed anymore (was in Cell Properties and Behaviors page
     #       generator.generateSecretionPlugin(*args, **kwds)

        if self.pythonControlSecretionCHB.isChecked():
            args.append("pythonControl")
            generator.generateSecretionPlugin(*args, **kwds)

            # if self.pdeSolverCallerCHB.isChecked():

            # xmlGenerator.generatePDESolverCaller()

        # PDE solvers

        # getting a list of solvers to be generated

        list_of_solvers = list(self.diffusantDict.keys())

        for solver in list_of_solvers:
            solver_generator_fcn = getattr(generator, 'generate' + solver)

            solver_generator_fcn(*args, **kwds)

            # if self.fieldTable.rowCount():

            # generator.generateDiffusionSolverFE(*args,**kwds)            

            # generator.generateFlexibleDiffusionSolverFE(*args,**kwds)

            # generator.generateFastDiffusionSolver2DFE(*args,**kwds)            

            # generator.generateKernelDiffusionSolver(*args,**kwds)            

            # generator.generateSteadyStateDiffusionSolver(*args,**kwds)            

        if self.boxWatcherCHB.isChecked():
            generator.generateBoxWatcherSteppable(*args, **kwds)

        # cell layout initializer

        if self.uniformRB.isChecked():
            generator.generateUniformInitializerSteppable(*args, **kwds)

        elif self.blobRB.isChecked():
            generator.generateBlobInitializerSteppable(*args, **kwds)

        elif self.piffRB.isChecked():
            generator.generatePIFInitializerSteppable(*args, **kwds)

        if self.pifDumperCHB.isChecked():
            generator.generatePIFDumperSteppable(*args, **kwds)

    def findRelativePathSegments(self, basePath, p, rest=[]):

        """

            This function finds relative path segments of path p with respect to base path    

            It returns list of relative path segments and flag whether operation succeeded or not    

        """

        h, t = os.path.split(p)

        pathMatch = False

        if h == basePath:
            pathMatch = True

            return [t] + rest, pathMatch

        print("(h,t,pathMatch)=", (h, t, pathMatch))

        if len(h) < 1: return [t] + rest, pathMatch

        if len(t) < 1: return [h] + rest, pathMatch

        return self.findRelativePathSegments(basePath, h, [t] + rest)

    def findRelativePath(self, basePath, p):

        relativePathSegments, pathMatch = self.findRelativePathSegments(basePath, p)

        if pathMatch:

            relative_path = ""

            for i in range(len(relativePathSegments)):

                segment = relativePathSegments[i]

                relative_path += segment

                if i != len(relativePathSegments) - 1:
                    relative_path += "/"  # we use unix style separators - they work on all (3) platforms

            return relative_path

        else:

            return p

    def getRelativePathWRTProjectDir(self, path):

        return self.findRelativePath(self.mainProjDir, path)
