from PyQt5.QtCore import Qt, pyqtSlot, QUrl
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMessageBox

from cc3d.twedit5.Plugins.CC3DProject.ui_contactpluginwidget import Ui_contactPluginWidget
from cc3d.twedit5.Plugins.CC3DProject.ContactPlugin_descr import get_contact_plugin_description_html
from cc3d.twedit5.Plugins.CC3DProject.InternalContactPlugin_descr import get_internal_contact_plugin_description_html

CONTACT_TABLE_HEADER_FONT_SIZE = 10
CONTACT_DESCR_FONT_SIZE = 11
CONTACT_SMALL_FONT_SIZE = 8
DEFAULT_CONTACT_ENERGY = '10.0'
DEFAULT_MIX_ENERGY = '2.0'
DEFAULT_SORT_ENERGY = '2.0'
DEFAULT_CONTACT_NEIGHBOR_ORDER = 2
MEDIUM_CELL_TYPE = "Medium"
NEIGHBOR_ORDER_TOOLTIP_1 = "How many nearby pixels the Contact(Internal) plugin algorithm will check " \
                           "each time it needs to do an energy calculation."
NEIGHBOR_ORDER_TOOLTIP_2 = "Integer > 0, typically between 2 and 4. Higher is more computationally intensive."
CONTACT_ENERGY_TABLE_CELL_TOOLTIP = "Contact energy per unit area between the two cells, used to calculate total contact energy."
RESET_MATRIX_TABLES_PB_TEXT = "Reset to default(s)"
RESET_MATRIX_TABLES_PB_TOOLTIP = "Reset contact energies and neighbor order to default values."

CONTACT_PLUGIN_DESCR = "Contact Plugin: computes the adhesion energy between neighboring cells. " \
                       "In essence, it describes how cells “stick” to each other. Contact energy is contrived. " \
                       "It is merely a way to replicate the properties of a cell’s membrane, " \
                       "the bindings of the nano-structures on its surface, and its environment (the Medium). " \
                       "For more realistic interactions use AdhesionFlex plugin instead."
CONTACT_PLUGIN_DESCR_2 = "Two cell types that have high contact energy will not “want to” adhere to each other. " \
                         "If possible, those cells may separate, effectively reducing the total energy to stay in " \
                         "that position. Conversely, low contact energy “encourages” cell types to bind. As contact " \
                         "energy is lowered, it also increases the surface of the contact. \n\nContact energy " \
                         "is constantly re-calculated each time a cell’s surface changes. Contact energy is defined " \
                         "as a matrix that compares each cell type against each other cell type. "

CONTACT_INTERNAL_PLUGIN_DESCR = "Internal Contact Plugin: controls how easily sub-cells within the same compartment " \
                                "adhere to each other. The Internal Contact Plugin can help control the shape and " \
                                "arrangement of a compartmentalized cell. The standard Contact Plugin is included to " \
                                "control how clusters interact with one another. The core idea here is to have different " \
                                "contact energies between subcells belonging to the same cluster and different energies " \
                                "for cells belonging to different clusters. Technically subcells of a cluster are “regular” " \
                                "CompuCell3D cells (cell types). "

CONTACT_URL = "https://compucell3dreferencemanual.readthedocs.io/en/latest/contact_plugin.html"
CONTACT_INTERNAL_URL = "https://compucell3dreferencemanual.readthedocs.io/en/latest/compartments.html"


class ContactPluginWidget(QWidget):
    """ Class that holds QT5 gui object for user entered values for Contact and Contact internal plugins. """

    def __init__(self, parent=None, contact_internal_call_back=None):
        super().__init__(parent)
        self.ui = Ui_contactPluginWidget()
        self.ui.setupUi(self)
        self.cell_types = []
        self.contact_cell_cell_energy: list[tuple[str, str, str]] = []  # list[ tuple[ mol1, mol2, binding param]]
        self.internal_contact_cell_cell_energy: list[tuple[str, str, str]] = []  # list[ tuple[ mol1, mol2, binding param]]
        self.contact_internal_callBack = contact_internal_call_back
        descr_font = QFont()
        descr_font.setPointSize(CONTACT_DESCR_FONT_SIZE)
        self.ui.contact_reset_tablesPB.setText(RESET_MATRIX_TABLES_PB_TEXT)
        self.ui.contact_reset_tablesPB.setToolTip(RESET_MATRIX_TABLES_PB_TOOLTIP)
        self.ui.contact_neighborSB.setToolTip(NEIGHBOR_ORDER_TOOLTIP_2)
        self.ui.contact_neighborSB.setValue(DEFAULT_CONTACT_NEIGHBOR_ORDER)
        self.ui.contact_neighborLB.setToolTip(NEIGHBOR_ORDER_TOOLTIP_1)
        self.ui.contact_internal_neighborSB.setToolTip(NEIGHBOR_ORDER_TOOLTIP_2)
        self.ui.contact_internal_neighborSB.setValue(DEFAULT_CONTACT_NEIGHBOR_ORDER)
        self.ui.internal_neighborLB.setToolTip(NEIGHBOR_ORDER_TOOLTIP_1)

        contact_descr_style = """
        table { font-size:11px; border: 0px light gray;}
        caption { font-size:12px; text-align: center; }
        td { text-align: center;}
        """
        self.ui.contact_plugin_textBrowser.clear()
        palette = self.ui.contact_plugin_textBrowser.palette()
        palette.setColor(QPalette.Base, QColor(230, 230, 230))  # background color
        self.ui.contact_plugin_textBrowser.setPalette(palette)
        self.ui.contact_plugin_textBrowser.setHtml(get_contact_plugin_description_html())

        self.ui.internal_contact_textBrowser.clear()
        palette = self.ui.internal_contact_textBrowser.palette()
        palette.setColor(QPalette.Base, QColor(230, 230, 230))
        self.ui.internal_contact_textBrowser.setPalette(palette)
        self.ui.internal_contact_textBrowser.document().setDefaultStyleSheet(contact_descr_style)
        self.ui.internal_contact_textBrowser.setHtml(get_internal_contact_plugin_description_html())

    @pyqtSlot(bool)
    def on_contact_reset_tablesPB_clicked(self):
        self.fillContactMatrixWithDefault()
        self.fillContactInternalMatrixWithDefault()
        self.ui.cells_mixCB.blockSignals(True)  # do not signal an event
        self.ui.cells_mixCB.setChecked(False)
        self.ui.cells_mixCB.blockSignals(False)
        self.ui.cells_sortCB.blockSignals(True)
        self.ui.cells_sortCB.setChecked(False)
        self.ui.cells_sortCB.blockSignals(False)
        self.ui.contact_neighborSB.setValue(DEFAULT_CONTACT_NEIGHBOR_ORDER)
        self.ui.contact_internal_neighborSB.setValue(DEFAULT_CONTACT_NEIGHBOR_ORDER)

    @pyqtSlot(bool)
    def on_cells_mixCB_toggled(self, is_checked):
        if is_checked:
            self.ui.cells_sortCB.setChecked(False)
            self.setUpCellMixingContactEnergiesMatrix()
        # else:  # let user decide through on_contact_reset_tablesPB_clicked()
            # self.fillContactMatrixWithDefault()

    @pyqtSlot(bool)
    def on_cells_sortCB_toggled(self, is_checked):
        if is_checked:
            self.ui.cells_mixCB.setChecked(False)
            self.setUpSortedCellsContactEnergiesMatrix()
        # else:
            # self.fillContactMatrixWithDefault()

    @pyqtSlot(bool)
    def on_contact_internalCB_toggled(self, is_checked):
        if is_checked:
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

    def fillContactMatrixWithDefault(self):
        """ Reset existing Contact energy matrix values with default values. """

        table_cell_font = QFont()
        table_cell_font.setPointSize(CONTACT_TABLE_HEADER_FONT_SIZE)
        for row in range(0, self.ui.contact_matrix_table.rowCount()):
            for column in range(0, self.ui.contact_matrix_table.columnCount()):
                if row <= column:
                    cell_to_update: QTableWidgetItem = self.ui.contact_matrix_table.item(row, column)
                    if cell_to_update:
                        cell_to_update.setText(str(DEFAULT_CONTACT_ENERGY))
                    else:  # create new table cell (QTableWidgetItem):
                        energy_par_item = QTableWidgetItem(str(DEFAULT_CONTACT_ENERGY))
                        energy_par_item.setFont(table_cell_font)
                        energy_par_item.setTextAlignment(Qt.AlignCenter)
                        tool_tip = CONTACT_ENERGY_TABLE_CELL_TOOLTIP
                        energy_par_item.setToolTip(tool_tip)
                        self.ui.contact_matrix_table.setItem(row, column, energy_par_item)
                #else:  # bottom of matrix assumed the same as top half, always filled with '-'

    def fillContactInternalMatrixWithDefault(self):
        """ Reset existing Contact Internal energy matrix values with default values. """

        table_cell_font = QFont()
        table_cell_font.setPointSize(CONTACT_TABLE_HEADER_FONT_SIZE)
        for row in range(0, self.ui.internal_contact_matrix_table.rowCount()):
            for column in range(0, self.ui.internal_contact_matrix_table.columnCount()):
                if row <= column:
                    cell_type_h = self.ui.internal_contact_matrix_table.horizontalHeaderItem(column).text()
                    cell_type_v = self.ui.internal_contact_matrix_table.verticalHeaderItem(row).text()
                    cell_to_update: QTableWidgetItem = self.ui.internal_contact_matrix_table.item(row, column)
                    if cell_to_update:
                        if cell_type_h == MEDIUM_CELL_TYPE or cell_type_v == MEDIUM_CELL_TYPE:
                            # Check if 'MEDIUM_CELL_TYPE' type, if so then default energy is '-',
                            # Internal cells do have contact with MEDIUM_CELL_TYPE outside of cell cluster.
                            cell_to_update.setText("-")
                        else:
                            cell_to_update.setText(str(DEFAULT_CONTACT_ENERGY))
                    else:  # create new table cell:
                        energy_par_item = QTableWidgetItem(str(DEFAULT_CONTACT_ENERGY))
                        energy_par_item.setFont(table_cell_font)
                        energy_par_item.setTextAlignment(Qt.AlignCenter)
                        tool_tip = CONTACT_ENERGY_TABLE_CELL_TOOLTIP
                        energy_par_item.setToolTip(tool_tip)
                        self.ui.internal_contact_matrix_table.setItem(row, column, energy_par_item)
                #else:  # bottom of matrix assumed the same as top half, always filled with '-'

    def checkIfNumber(self, value: str) -> bool:
        if value.isdecimal():
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def checkEnergyValue(self, val: str) -> bool:
        # can also be "-", need to check:
        if val.strip() == "-":
            return True
        if not self.checkIfNumber(val):
            return False
        else:
            return True

    def checkContactEnergyValue(self, item: QTableWidgetItem) -> bool:
        cell_1 = self.ui.contact_matrix_table.horizontalHeaderItem(item.column()).text()
        cell_2 = self.ui.contact_matrix_table.verticalHeaderItem(item.row()).text()
        val_str = item.text()
        if self.checkEnergyValue(val_str):
            return True
        else:
            item.setText(DEFAULT_CONTACT_ENERGY)
            QMessageBox.warning(self, "Not a number",
                                f"Please specify a number for the {cell_1} - {cell_2} contact energy value",
                                QMessageBox.Ok)
            return False

    def checkContactInternalEnergyValue(self, item: QTableWidgetItem) -> bool:
        cell_1 = self.ui.internal_contact_matrix_table.horizontalHeaderItem(item.column()).text()
        cell_2 = self.ui.internal_contact_matrix_table.verticalHeaderItem(item.row()).text()
        val_str = item.text()
        if self.checkEnergyValue(val_str):
            return True
        else:
            item.setText(DEFAULT_CONTACT_ENERGY)
            QMessageBox.warning(self, "Not a number",
                                f"Please specify a number for the {cell_1} - {cell_2} contact internal energy value",
                                QMessageBox.Ok)
            return False

    def validateContactPage(self) -> list[str]:
        issues = []
        # TODO: check if valid information. Needed??
        return issues

    def initContactMatrix(self, cell_types: list[str]):
        """ Sets up the initial Contact matrix then fills with default values."""

        header_font = QFont()
        header_font.setPointSize(CONTACT_TABLE_HEADER_FONT_SIZE)
        cell_type_count = len(cell_types)

        self.cell_types.clear()
        # clear out existing matrix
        if self.ui.contact_matrix_table.rowCount() > 0:
            self.clearMatrixTable(self.ui.contact_matrix_table)
        self.ui.contact_matrix_table.blockSignals(True)  # Do not trigger signal while adding default values.
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

                    tool_tip = CONTACT_ENERGY_TABLE_CELL_TOOLTIP
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
        self.ui.contact_matrix_table.itemChanged.connect(self.checkContactEnergyValue)
        self.ui.contact_matrix_table.blockSignals(False)

    def initInternalContactMatrix(self, cell_types: list[str]):
        """ Sets up the initial Internal Contact matrix with default values."""

        self.ui.contact_internalCB.setChecked(True)
        self.ui.internal_contact_matrixGB.setEnabled(True)

        # clear out existing matrix:
        if self.ui.internal_contact_matrix_table.rowCount() > 0:
            self.clearMatrixTable(self.ui.internal_contact_matrix_table)
        self.ui.internal_contact_matrix_table.blockSignals(True)

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
                cell_type_h = self.ui.internal_contact_matrix_table.horizontalHeaderItem(column).text()
                if cell_type_h == MEDIUM_CELL_TYPE:
                    medium_col = column
                if row <= column:
                    if cell_type_h == MEDIUM_CELL_TYPE or row == medium_col:
                        # Check if 'MEDIUM_CELL_TYPE' type, if so then default energy is '-',
                        # Internal cells do have contact with MEDIUM_CELL_TYPE outside of cell cluster.
                        binding_par_item = QTableWidgetItem("-")
                    else:
                        binding_par_item = QTableWidgetItem(str(DEFAULT_CONTACT_ENERGY))
                    binding_par_item.setFont(header_font)
                    binding_par_item.setTextAlignment(Qt.AlignCenter)
                    tool_tip = CONTACT_ENERGY_TABLE_CELL_TOOLTIP
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
        self.ui.internal_contact_matrix_table.itemChanged.connect(self.checkContactInternalEnergyValue)
        self.ui.internal_contact_matrix_table.blockSignals(False)

    def setUpSortedCellsContactEnergiesMatrix(self):
        table_cell_font = QFont()
        table_cell_font.setPointSize(CONTACT_TABLE_HEADER_FONT_SIZE)
        for row in range(0, self.ui.contact_matrix_table.rowCount()):
            for column in range(0, self.ui.contact_matrix_table.columnCount()):
                if row <= column:
                    cell_to_update: QTableWidgetItem = self.ui.contact_matrix_table.item(row, column)
                    if cell_to_update:
                        cell_1: str = self.ui.contact_matrix_table.horizontalHeaderItem(row).text()
                        cell_2: str = self.ui.contact_matrix_table.verticalHeaderItem(column).text()
                        if row < column:
                            if cell_1 == MEDIUM_CELL_TYPE or cell_2 == MEDIUM_CELL_TYPE:
                                cell_to_update.setText(str('16.0'))
                            else:
                                cell_to_update.setText(str(DEFAULT_CONTACT_ENERGY))
                        else:  # Same cell type contact:
                            if cell_1 == MEDIUM_CELL_TYPE and cell_2 == MEDIUM_CELL_TYPE:
                                cell_to_update.setText(str('0.0'))
                            else:
                                cell_to_update.setText(str(DEFAULT_SORT_ENERGY))
                    else:  # create new table cell:
                        energy_par_item = QTableWidgetItem(str(DEFAULT_CONTACT_ENERGY))
                        energy_par_item.setFont(table_cell_font)
                        energy_par_item.setTextAlignment(Qt.AlignCenter)
                        tool_tip = CONTACT_ENERGY_TABLE_CELL_TOOLTIP
                        energy_par_item.setToolTip(tool_tip)
                        self.ui.contact_matrix_table.setItem(row, column, energy_par_item)
                # else:  # bottom of matrix assumed the same as top half, always filled with '-'

    def setUpCellMixingContactEnergiesMatrix(self):
        table_cell_font = QFont()
        table_cell_font.setPointSize(CONTACT_TABLE_HEADER_FONT_SIZE)
        for row in range(0, self.ui.contact_matrix_table.rowCount()):
            for column in range(0, self.ui.contact_matrix_table.columnCount()):
                if row <= column:
                    cell_to_update: QTableWidgetItem = self.ui.contact_matrix_table.item(row, column)
                    if cell_to_update:
                        if row < column:
                            if self.ui.contact_matrix_table.horizontalHeaderItem(row).text() == MEDIUM_CELL_TYPE or \
                                    self.ui.contact_matrix_table.verticalHeaderItem(column).text() == MEDIUM_CELL_TYPE:
                                cell_to_update.setText(str(DEFAULT_CONTACT_ENERGY))  # Do not mix with Medium cell type
                            else:
                                cell_to_update.setText(str(DEFAULT_MIX_ENERGY))
                        else:  # Same cell type contact:
                            cell_to_update.setText(str(DEFAULT_CONTACT_ENERGY))
                    else:  # create new table cell if none there:
                        energy_par_item = QTableWidgetItem(str(DEFAULT_CONTACT_ENERGY))
                        energy_par_item.setFont(table_cell_font)
                        energy_par_item.setTextAlignment(Qt.AlignCenter)
                        tool_tip = CONTACT_ENERGY_TABLE_CELL_TOOLTIP
                        energy_par_item.setToolTip(tool_tip)
                        self.ui.contact_matrix_table.setItem(row, column, energy_par_item)
                # else:  # bottom of matrix assumed the same as top half, always filled with '-'

    def getContactNeighborOrder(self) -> int:
        return int(self.ui.contact_neighborSB.value())

    def setContactNeighborOrder(self, val: int) -> bool:
        if isinstance(val, int):
            if 0 >= int(val) <= 10:
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
            if 0 >= int(val) <= 10:
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
        for row in range(self.ui.contact_matrix_table.rowCount()):
            for col in range(self.ui.contact_matrix_table.columnCount()):
                if str(self.ui.contact_matrix_table.item(row, col).text()).strip() != "-":
                    cell1 = str(self.ui.contact_matrix_table.verticalHeaderItem(row).text())
                    cell2 = str(self.ui.contact_matrix_table.horizontalHeaderItem(col).text())
                    contact_energy = str(self.ui.contact_matrix_table.item(row, col).text()).strip()
                    if contact_energy == "-":  # Valid if no cell-cell contact
                        new_cell_cell_bind = (cell1, cell2, contact_energy)
                    else:
                        try:
                            contact_energy_float = float(contact_energy)
                            new_cell_cell_bind = (cell1, cell2, contact_energy)
                        except ValueError:
                            new_cell_cell_bind = (cell1, cell2, DEFAULT_CONTACT_ENERGY)
                    self.contact_cell_cell_energy.append(new_cell_cell_bind)
        return self.contact_cell_cell_energy

    def getInternalContactEnergyMatrix(self) -> list[tuple[str, str, str]]:
        # generate cell-cell internal contact energy list here:
        for row in range(self.ui.internal_contact_matrix_table.rowCount()):
            for col in range(self.ui.internal_contact_matrix_table.columnCount()):
                if str(self.ui.internal_contact_matrix_table.item(row, col).text()).strip() != "-":
                    cell1 = str(self.ui.internal_contact_matrix_table.verticalHeaderItem(row).text())
                    cell2 = str(self.ui.internal_contact_matrix_table.horizontalHeaderItem(col).text())
                    contact_energy = str(self.ui.internal_contact_matrix_table.item(row, col).text()).strip()
                    if contact_energy == "-":  # Valid if no cell-cell contact
                        new_cell_cell_bind = (cell1, cell2, contact_energy)
                    else:
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

    def validateContactAndContactInteralEnergies(self) -> list[str]:
        issues: list[str] = []
        # TODO
        return issues
