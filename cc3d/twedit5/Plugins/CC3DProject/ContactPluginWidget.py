from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from cc3d.twedit5.Plugins.CC3DProject.ui_contactpluginwidget import Ui_contactPluginWidget

CONTACT_TABLE_HEADER_FONT_SIZE = 10
CONTACT_SMALL_FONT_SIZE = 8
DEFAULT_CONTACT_ENERGY = '10.0'
DEFAULT_MIX_ENERGY = '2.0'
DEFAULT_SORT_ENERGY = '20'

class ContactPluginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_contactPluginWidget()
        self.ui.setupUi(self)
        #uic.loadUi("Plugins/CC3DProject/ContactPlugin_widget.ui", self)  # Alternative approach
        #self.ui.contact_value_LE.setText("100,000")

    """ Sets up the initial Contact matrix with default values."""
    def initContactMatrix(self, cell_types: list[str]):
        header_font = QFont()
        header_font.setPointSize(CONTACT_TABLE_HEADER_FONT_SIZE)
        cell_type_count = len(cell_types)
        column_names = []
        for i in range(cell_type_count):
            column_names.append(cell_types[i])

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
    def getContactNeighborOrder(self) -> int:
        pass

    def setContactNeighborOrder(self, val: int):
        pass

    def getInternalContactNeighborOrder(self) -> int:
        pass

    def setInternalContactNeighborOrder(self, val: int):
        pass

    def getContactEnergyMatrix(self):
        pass

    def setContactEnergyMatrix(self):
        pass
    def getInternalContactEnergyMatrix(self):
        pass

    def setInternalContactEnergyMatrix(self):
        pass


