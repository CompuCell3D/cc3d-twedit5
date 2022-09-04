from copy import deepcopy
from itertools import product
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pandas as pd
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CC3DModelToolGUIBase import CC3DModelToolGUIBase
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CellType.ui_celltypedlg import Ui_CellTypePluginGUI
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.xml_parse_data import ParseMode
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.table_component import TableComponent
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CellType.CellTypePluginData import CellTypePluginData



class CellTypeGUI(CC3DModelToolGUIBase, Ui_CellTypePluginGUI):
    def __init__(self, parent=None, cell_type_plugin_data:CellTypePluginData = None):
        super(CellTypeGUI, self).__init__(parent)
        self.setupUi(self)

        # self.cell_types = deepcopy(cell_types)
        # self.is_frozen = deepcopy(is_frozen)

        self.cell_type_plugin_data = cell_type_plugin_data
        self.cell_type_params_table = None

        self.selected_row = None

        self.init_data()

        self.connect_all_signals()

        self.draw_ui()

        self.showNormal()

    def init_data(self):
        return

    def draw_ui(self):

        if self.cell_type_plugin_data is None:
            return

        self.cell_type_params_table = TableComponent(module_data=self.cell_type_plugin_data.global_params)

        self.cell_type_GB.layout().addWidget(self.cell_type_params_table.get_ui())

    def connect_all_signals(self):
        self.cellTypeAddPB.clicked.connect(self.handle_add_cell_type)
        self.okPB.clicked.connect(self.on_accept)
        self.cancelPB.clicked.connect(self.on_reject)

        return
        # self.cellTypeTable.itemChanged.connect(self.on_table_item_change)
        # self.cellTypeAddPB.clicked.connect(self.on_add_cell_type)
        # self.deleteCellTypePB.clicked.connect(self.on_del_cell_type)
        # self.clearCellTypeTablePB.clicked.connect(self.on_clear_table)
        # self.okPB.clicked.connect(self.on_accept)
        # self.cancelPB.clicked.connect(self.on_reject)

    def on_table_item_change(self, item: QTableWidgetItem):
        if item.row() == 0 and item.column() == 0:
            item.setText("Medium")
            return
        elif item.row() < 0:
            return
        if item.column() == 0 and item.text() != "Medium" and item.text().__len__() > 2:
            self.name_change(old_name=self.cell_types[item.row()], new_name=item.text())

    def handle_add_cell_type(self):
        cell_type_name = self.cellTypeLE.text()
        freeze = self.freezeCHB.isChecked()

        # insert_row_df = pd.DataFrame([{"CellType": "New", "TargetVolume": 22, "LambdaVolume": 2.1, "Freeze": False}])

        view = self.cell_type_params_table.table_view
        model = view.model()
        insert_row_df = self.cell_type_plugin_data.get_cell_type_row(cell_type_name=cell_type_name, freeze=freeze)
        model.append_rows(append_df=insert_row_df)
        self.cell_type_plugin_data.global_params.df = model.df

        # self.cell_type_plugin_data.add_cell_type(cell_type_name=cell_type_name, freeze=freeze)

        # if not self.validate_name(name=cell_type_name):
        #     return
        #
        # self.cell_types.append(cell_type_name)
        # self.is_frozen.append(freeze)
        #
        # self.draw_ui()

    def on_del_cell_type(self):
        row = self.cellTypeTable.currentRow()
        col = self.cellTypeTable.currentColumn()
        if row < 0 or col < 0:
            return

        cell_name = self.cellTypeTable.item(row, 0).text()
        if cell_name == "Medium":
            return
        else:
            self.cell_types.pop(row)
            self.is_frozen.pop(row)

            self.draw_ui()

    def on_clear_table(self):
        self.cell_types = []
        self.is_frozen = []
        self.init_data()
        self.draw_ui()

    def on_accept(self):
        self.user_decision = True
        self.close()

    def on_reject(self):
        self.user_decision = False
        self.close()

    def name_change(self, old_name: str, new_name: str):
        if self.validate_name(name=new_name):
            for i in range(self.cell_types.__len__()):
                if self.cell_types[i] == old_name:
                    self.cell_types[i] = new_name
                    return

    # def validate_name(self, name: str):
    #     return not (name in self.cell_types or name == "Medium" or name.__len__() < 2)


class TypeTableItem(QTableWidgetItem):
    def __init__(self, text: str):
        super(TypeTableItem, self).__init__()
        self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        self.setText(text)


class FreezeCB(QWidget):
    def __init__(self, parent: CellTypeGUI, check_state: bool = False, is_medium: bool = False):
        super(FreezeCB, self).__init__(parent)

        self.cb = QCheckBox()
        self.cb.setCheckable(not is_medium)
        self.cb.setChecked(check_state and not is_medium)

        self.h_layout = QHBoxLayout(self)
        self.h_layout.addWidget(self.cb)
        self.h_layout.setAlignment(Qt.AlignCenter)
