from copy import deepcopy
from itertools import product
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets

from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CC3DModelToolGUIBase import CC3DModelToolGUIBase
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Volume.ui_volumedlg import Ui_VolumePluginGUI

from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.table_component import TableComponent


class VolumeGUI(CC3DModelToolGUIBase, Ui_VolumePluginGUI):
    def __init__(self, parent=None, volume_plugin_data=None, cell_types: List[str] = None):
        super(VolumeGUI, self).__init__(parent)
        self.setupUi(self)
        self.cell_types = ['Medium', 'Condensing', 'NonCondensing']
        self.volume_plugin_data = volume_plugin_data
        self.volume_params_table = None
        self.table_inserted = ''
        self.user_decision = None

        self.selected_row = None

        self.init_data()

        self.connect_all_signals()

        self.draw_ui()

        self.showNormal()

    def init_data(self):
        return

    def draw_ui(self):

        if self.volume_plugin_data is None:
            return

        if self.volume_plugin_data.global_params:
            if self.global_RB.isChecked():
                self.insert_global_params_table()
            else:

                self.global_RB.toggle()

        elif self.volume_plugin_data.by_type_params:
            if self.by_type_RB.isChecked():
                self.insert_by_type_params_table()
            else:
                self.by_type_RB.toggle()

    def insert_global_params_table(self):
        self.volume_params_table = TableComponent(module_data=self.volume_plugin_data.global_params)
        self.remove_table()
        self.by_type_GB.layout().addWidget(self.volume_params_table.get_ui())
        self.table_inserted = 'global'

    def insert_by_type_params_table(self):
        self.volume_params_table = TableComponent(module_data=self.volume_plugin_data.by_type_params)
        self.remove_table()
        self.by_type_GB.layout().addWidget(self.volume_params_table.get_ui())

        self.table_inserted = 'by_type'

    def remove_table(self):
        if self.by_type_GB.layout().count() > 0:
            self.by_type_GB.layout().takeAt(0)

    def connect_all_signals(self):
        print('connecting signals - to implement')
        self.global_RB.toggled.connect(self.on_global_RB_toggled)
        self.by_type_RB.toggled.connect(self.on_by_type_RB_toggled)
        self.ok_PB.clicked.connect(self.accept)
        self.cancel_PB.clicked.connect(self.reject)

    def on_global_RB_toggled(self, flag):

        if flag:
            if self.volume_plugin_data.global_params is None:
                self.volume_plugin_data.global_params = self.volume_plugin_data.get_default_global_params()

            if self.table_inserted != 'global':
                self.insert_global_params_table()
                self.volume_plugin_data.mode = 'global'


    def on_by_type_RB_toggled(self, flag):

        if flag:
            if self.volume_plugin_data.by_type_params is None:
                self.volume_plugin_data.by_type_params = self.volume_plugin_data.get_default_by_type_params(
                    cell_types=self.cell_types)

            if self.table_inserted != 'by_type':
                self.insert_by_type_params_table()
                self.volume_plugin_data.mode = 'by_type'

    # def on_table_item_change(self, item: QTableWidgetItem):
    #     if item.row() == 0 and item.column() == 0:
    #         item.setText("Medium")
    #         return
    #     elif item.row() < 0:
    #         return
    #     if item.column() == 0 and item.text() != "Medium" and item.text().__len__() > 2:
    #         self.name_change(old_name=self.cell_types[item.row()], new_name=item.text())

    # def on_add_cell_type(self):
    #     cell_name = self.cellTypeLE.text()
    #     is_freeze = self.freezeCHB.isChecked()
    #
    #     if not self.validate_name(name=cell_name):
    #         return
    #
    #     self.cell_types.append(cell_name)
    #     self.is_frozen.append(is_freeze)
    #
    #     self.draw_ui()
    #
    # def on_del_cell_type(self):
    #     row = self.cellTypeTable.currentRow()
    #     col = self.cellTypeTable.currentColumn()
    #     if row < 0 or col < 0:
    #         return
    #
    #     cell_name = self.cellTypeTable.item(row, 0).text()
    #     if cell_name == "Medium":
    #         return
    #     else:
    #         self.cell_types.pop(row)
    #         self.is_frozen.pop(row)
    #
    #         self.draw_ui()
    #
    # def on_clear_table(self):
    #     self.cell_types = []
    #     self.is_frozen = []
    #     self.init_data()
    #     self.draw_ui()

    def accept(self):
        self.user_decision = True
        self.close()

    def reject(self):
        self.user_decision = False
        self.close()

    # def on_reject(self):
    #     self.user_decision = False
    #     self.close()

    # def name_change(self, old_name: str, new_name: str):
    #     if self.validate_name(name=new_name):
    #         for i in range(self.cell_types.__len__()):
    #             if self.cell_types[i] == old_name:
    #                 self.cell_types[i] = new_name
    #                 return

    # def validate_name(self, name: str):
    #     return not (name in self.cell_types or name == "Medium" or name.__len__() < 2)

# class TypeTableItem(QTableWidgetItem):
#     def __init__(self, text: str):
#         super(TypeTableItem, self).__init__()
#         self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
#         self.setText(text)
#
#
# class FreezeCB(QWidget):
#     def __init__(self, parent: CellTypeGUI, check_state: bool = False, is_medium: bool = False):
#         super(FreezeCB, self).__init__(parent)
#
#         self.cb = QCheckBox()
#         self.cb.setCheckable(not is_medium)
#         self.cb.setChecked(check_state and not is_medium)
#
#         self.h_layout = QHBoxLayout(self)
#         self.h_layout.addWidget(self.cb)
#         self.h_layout.setAlignment(Qt.AlignCenter)
