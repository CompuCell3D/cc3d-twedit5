from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from cc3d.twedit5.Plugins.CC3DProject.ui_contactpluginwidget import Ui_contactPluginWidget

CONTACT_TABLE_HEADER_FONT_SIZE = 10
CONTACT_SMALL_FONT_SIZE = 8
DEFAULT_CONTACT_ENERGY = '10.0'
DEFAULT_MIX_ENERGY = '2.0'
DEFAULT_SORT_ENERGY = '20'
DEFAULT_CONTACT_NEIGHBOR_ORDER = 2
NEIGHBOR_ORDER_TOOLTIP_1 = "How many nearby pixels the Contact(Internal) plugin algorithm will check " \
                           "each time it needs to do an energy calculation."
NEIGHBOR_ORDER_TOOLTIP_2 = "Integer > 0, typically between 2 and 4. Higher is more computationally intensive."
RESET_MATRIX_TABLES_PB_TEXT = "Reset to default"
RESET_MATRIX_TABLES_PB_TOOLTIP = "Reset contact energies and neighbor order to default values."

class ContactPluginWidget(QWidget):
    def __init__(self, parent=None, contact_internal_call_back=None):
        super().__init__(parent)
        self.ui = Ui_contactPluginWidget()
        self.ui.setupUi(self)
        self.cell_types = []
        self.contact_cell_cell_energy: list[tuple[str, str, str]] = []  # list[ tuple[ mol1, mol2, binding param]]
        self.internal_contact_cell_cell_energy: list[tuple[str, str, str]] = []  # list[ tuple[ mol1, mol2, binding param]]
        self.contact_internal_callBack = contact_internal_call_back
        self.ui.contact_reset_tablesPB.setText(RESET_MATRIX_TABLES_PB_TEXT)
        self.ui.contact_reset_tablesPB.setToolTip(RESET_MATRIX_TABLES_PB_TOOLTIP)
        self.ui.contact_neighborSB.setToolTip(NEIGHBOR_ORDER_TOOLTIP_2)
        self.ui.contact_neighborSB.setValue(DEFAULT_CONTACT_NEIGHBOR_ORDER)
        self.ui.contact_neighborLB.setToolTip(NEIGHBOR_ORDER_TOOLTIP_1)
        self.ui.contact_internal_neighborSB.setToolTip(NEIGHBOR_ORDER_TOOLTIP_2)
        self.ui.contact_internal_neighborSB.setValue(DEFAULT_CONTACT_NEIGHBOR_ORDER)
        self.ui.internal_neighborLB.setToolTip(NEIGHBOR_ORDER_TOOLTIP_1)

    @pyqtSlot(bool)
    def on_contact_internalCB_toggled(self, is_checked):
        if is_checked:
            #self.ui.internal_contact_matrixGB.setEnabled(True)
            self.initInternalContactMatrix(self.cell_types)
        else:
            self.ui.internal_contact_matrixGB.setEnabled(False)
        if self.contact_internal_callBack is not None:
            self.contact_internal_callBack(is_checked)

    def clearTableWidget(self, table_widget_to_be_cleared: QTableWidget):
        rows = table_widget_to_be_cleared.rowCount()
        for i in range(rows - 1, -1, -1):
            table_widget_to_be_cleared.removeRow(i)

    def clearMatrixTable(self, table_widget_to_be_cleared: QTableWidget):
        try:
            self.clearTableWidget(table_widget_to_be_cleared)
            table_widget_to_be_cleared.clear()  # clear headers
        except NameError:
            print(f" -> ContactPluginWidget: clearMatrixTable() {table_widget_to_be_cleared}"
                  " does not exist.")

    """ Sets up the initial Contact matrix with default values."""
    def initContactMatrix(self, cell_types: list[str]):
        header_font = QFont()
        header_font.setPointSize(CONTACT_TABLE_HEADER_FONT_SIZE)
        cell_type_count = len(cell_types)

        self.cell_types.clear()
        # clear out existing matrix
        if self.ui.contact_matrix_table.rowCount() > 0:
            self.clearMatrixTable(self.ui.contact_matrix_table)

        column_names = []
        for i in range(cell_type_count):
            column_names.append(cell_types[i])
            self.cell_types.append(cell_types[i])

        self.ui.contact_matrix_table.setColumnCount(len(column_names))
        self.ui.contact_matrix_table.setHorizontalHeaderLabels(column_names)
        for i in range(0, self.ui.contact_matrix_table.columnCount()):
            self.ui.contact_matrix_table.horizontalHeaderItem(i).setFont(header_font)

        for row in range(0, cell_type_count):
            self.ui.contact_matrix_table.insertRow(row)
            for column in range(0, cell_type_count):
                if row <= column:
                    binding_par_item = QTableWidgetItem(str(DEFAULT_CONTACT_ENERGY))
                    binding_par_item.setFont(header_font)
                    binding_par_item.setTextAlignment(Qt.AlignCenter)
                    tool_tip = "Contact energy per unit area between the two cells, used to calculate total binding energy."
                    binding_par_item.setToolTip(tool_tip)
                    self.ui.contact_matrix_table.setItem(row, column, binding_par_item)
                else:  # bottom of matrix assumed the same as top half:
                    redundant_val = QTableWidgetItem("-")
                    redundant_val.setTextAlignment(Qt.AlignCenter)
                    redundant_val.setFlags(redundant_val.flags() & ~Qt.ItemIsEditable)  # not editable
                    self.ui.contact_matrix_table.setItem(row, column, redundant_val)

        self.ui.contact_matrix_table.setVerticalHeaderLabels(column_names)  # matrix, so col - row headers same.
        if self.ui.contact_matrix_table.rowCount() > 0:
            for i in range(0, self.ui.contact_matrix_table.rowCount()):
                self.ui.contact_matrix_table.verticalHeaderItem(i).setFont(header_font)
        self.ui.contact_matrix_table.verticalHeader().setVisible(True)
        self.ui.contact_matrix_table.resizeRowsToContents()
        self.ui.contact_matrix_table.resizeColumnsToContents()

    """ Sets up the initial Internal Contact matrix with default values."""
    def initInternalContactMatrix(self, cell_types: list[str]):
        self.ui.contact_internalCB.setChecked(True)
        self.ui.internal_contact_matrixGB.setEnabled(True)

       # clear out existing matrix:
        if self.ui.internal_contact_matrix_table.rowCount() > 0:
            self.clearMatrixTable(self.ui.internal_contact_matrix_table)

        header_font = QFont()
        header_font.setPointSize(CONTACT_TABLE_HEADER_FONT_SIZE)
        cell_type_count = len(cell_types)
        column_names = []
        for i in range(cell_type_count):
            column_names.append(cell_types[i])

        self.ui.internal_contact_matrix_table.setColumnCount(len(column_names))
        self.ui.internal_contact_matrix_table.setHorizontalHeaderLabels(column_names)
        for i in range(0, self.ui.contact_matrix_table.columnCount()):
            self.ui.internal_contact_matrix_table.horizontalHeaderItem(i).setFont(header_font)

        for row in range(0, cell_type_count):
            self.ui.internal_contact_matrix_table.insertRow(row)
            for column in range(0, cell_type_count):
                if row <= column:
                    binding_par_item = QTableWidgetItem(str(DEFAULT_CONTACT_ENERGY))
                    binding_par_item.setFont(header_font)
                    binding_par_item.setTextAlignment(Qt.AlignCenter)
                    tool_tip = "Contact energy per unit area between the two cells, used to calculate total binding energy."
                    binding_par_item.setToolTip(tool_tip)
                    self.ui.internal_contact_matrix_table.setItem(row, column, binding_par_item)
                else:  # bottom of matrix assumed the same as top half:
                    redundant_val = QTableWidgetItem("-")
                    redundant_val.setTextAlignment(Qt.AlignCenter)
                    redundant_val.setFlags(redundant_val.flags() & ~Qt.ItemIsEditable)  # not editable
                    self.ui.internal_contact_matrix_table.setItem(row, column, redundant_val)

        self.ui.internal_contact_matrix_table.setVerticalHeaderLabels(column_names)  # matrix, so col - row headers same.
        if self.ui.internal_contact_matrix_table.rowCount() > 0:
            for i in range(0, self.ui.internal_contact_matrix_table.rowCount()):
                self.ui.internal_contact_matrix_table.verticalHeaderItem(i).setFont(header_font)
        self.ui.internal_contact_matrix_table.verticalHeader().setVisible(True)
        self.ui.internal_contact_matrix_table.resizeRowsToContents()
        self.ui.internal_contact_matrix_table.resizeColumnsToContents()

    def getContactNeighborOrder(self) -> int:
        return int(self.ui.contact_neighborSB.value())

    def setContactNeighborOrder(self, val: int) -> bool:
        if isinstance(val, int):
            if 0 >= int(val) >= 10:
                self.ui.contact_neighborSB.setValue(val)
                return True
            else:
                return False
        else:
            print("setContactNeighborOrder(): val is not an int.")
            return False

    def getInternalContactNeighborOrder(self) -> int:
        return int(self.ui.contact_internal_neighborSB.value())

    def setInternalContactNeighborOrder(self, val: int) -> bool:
        if isinstance(val, int):
            if 0 >= int(val) >= 10:
                self.ui.contact_internal_neighborSB.setValue(val)
                return True
            else:
                return False
        else:
            print("setInternalContactNeighborOrder(): val is not an int.")
            return False

    def setContactEnergyMatrix(self, cell_cell_energies: list[tuple[str, str, str]]):
        # TODO
        pass

    def getContactEnergyMatrix(self) -> list[tuple[str, str, str]]:

        # generate cell-cell contact energy list here:
        for row in range(self.ui.contract_matrix_table.rowCount()):
            for col in range(self.ui.contract_matrix_table.columnCount()):
                if str(self.ui.contract_matrix_table.item(row, col).text()).strip() != "-":
                    cell1 = str(self.ui.contract_matrix_table.verticalHeaderItem(row).text())
                    cell2 = str(self.ui.contract_matrix_table.horizontalHeaderItem(col).text())
                    contact_energy = str(self.ui.contract_matrix_table.item(row, col).text()).strip()
                    try:
                        contact_energy_float = float(contact_energy)
                        new_cell_cell_bind = (cell1, cell2, contact_energy)
                    except ValueError:
                        new_cell_cell_bind = (cell1, cell2, DEFAULT_CONTACT_ENERGY)
                    self.contact_cell_cell_energy.append(new_cell_cell_bind)
        return self.contact_cell_cell_energy

    def getInternalContactEnergyMatrix(self) -> list[tuple[str, str, str]]:
        # generate cell-cell internal contact energy list here:
        for row in range(self.ui.internal_contract_matrix_table.rowCount()):
            for col in range(self.ui.internal_contract_matrix_table.columnCount()):
                if str(self.ui.internal_contract_matrix_table.item(row, col).text()).strip() != "-":
                    cell1 = str(self.ui.internal_contract_matrix_table.verticalHeaderItem(row).text())
                    cell2 = str(self.ui.internal_contract_matrix_table.horizontalHeaderItem(col).text())
                    contact_energy = str(self.ui.internal_contract_matrix_table.item(row, col).text()).strip()
                    try:
                        contact_energy_float = float(contact_energy)
                        new_cell_cell_bind = (cell1, cell2, contact_energy)
                    except ValueError:
                        contact_energy = DEFAULT_CONTACT_ENERGY
                        new_cell_cell_bind = (cell1, cell2, contact_energy)
                    self.internal_contact_cell_cell_energy.append(new_cell_cell_bind)
        return self.internal_contact_cell_cell_energy

    def setInternalContactEnergyMatrix(self, cell_cell_energies: list[tuple[str, str, str]]):
        # TODO
        pass


