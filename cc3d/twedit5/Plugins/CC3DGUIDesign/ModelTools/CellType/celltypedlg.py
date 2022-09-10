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
    def __init__(self, parent=None, cell_type_plugin_data: CellTypePluginData = None):
        super(CellTypeGUI, self).__init__(parent)
        self.setupUi(self)

        self.cell_type_plugin_data = cell_type_plugin_data
        self.cell_type_params_table = None

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
        self.okPB.clicked.connect(self.handle_accept)
        self.cancelPB.clicked.connect(self.handle_reject)
        self.deleteCellTypePB.clicked.connect(self.handle_delete_cell_type)
        self.clearCellTypeTablePB.clicked.connect(self.handle_clear_table)

    def on_table_item_change(self, item: QTableWidgetItem):
        if item.row() == 0 and item.column() == 0:
            item.setText("Medium")
            return
        elif item.row() < 0:
            return
        if item.column() == 0 and item.text() != "Medium" and item.text().__len__() > 2:
            self.name_change(old_name=self.cell_types[item.row()], new_name=item.text())

    def handle_add_cell_type(self):

        cell_type_name = self.cellTypeLE.text().strip()
        if not cell_type_name:
            return

        freeze = self.freezeCHB.isChecked()

        view = self.cell_type_params_table.table_view
        model = view.model()
        insert_row_df = self.cell_type_plugin_data.get_cell_type_row(cell_type_name=cell_type_name, freeze=freeze)
        model.append_rows(append_df=insert_row_df)

        self.update_plugin_data_from_model_data()

        # resetting input widgets
        self.cellTypeLE.clear()
        self.freezeCHB.setChecked(False)

    def handle_delete_cell_type(self):
        view = self.cell_type_params_table.table_view
        current_index = view.currentIndex()
        if current_index.isValid():
            i = current_index.row()
            cell_type = self.cell_type_plugin_data.global_params.df["TypeName"].values[i]
            if cell_type == "Medium":
                return
            model = view.model()
            model.remove_row(index=current_index, num_rows=1)

            self.update_plugin_data_from_model_data()

    def handle_clear_table(self):
        view = self.cell_type_params_table.table_view
        model = view.model()
        mask = model.df["TypeName"] == "Medium"
        model.df = model.df[mask]
        model.layoutChanged.emit()

        self.update_plugin_data_from_model_data()

    def update_plugin_data_from_model_data(self):
        """
        updates self.cell_type_plugin_data based on model data (model is in model view controler)
        """
        view = self.cell_type_params_table.table_view
        model = view.model()
        self.cell_type_plugin_data.global_params.df = model.df

    def handle_accept(self):
        self.user_decision = True
        self.close()

    def handle_reject(self):
        self.user_decision = False
        self.close()

    def name_change(self, old_name: str, new_name: str):
        if self.validate_name(name=new_name):
            for i in range(self.cell_types.__len__()):
                if self.cell_types[i] == old_name:
                    self.cell_types[i] = new_name
                    return
