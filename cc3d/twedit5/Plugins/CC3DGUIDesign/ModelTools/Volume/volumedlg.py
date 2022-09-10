from copy import deepcopy
from itertools import product
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from typing import Dict
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CC3DModelToolGUIBase import CC3DModelToolGUIBase
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Volume.ui_volumedlg import Ui_VolumePluginGUI
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.xml_parse_data import ParseMode
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.table_component import TableComponent
import pandas as pd
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.xml_parse_data import XMLParseData


class VolumeGUI(CC3DModelToolGUIBase, Ui_VolumePluginGUI):
    def __init__(
        self, parent=None, volume_plugin_data=None, modules_to_react_to_data_dict: Dict[str, XMLParseData] = None
    ):
        super(VolumeGUI, self).__init__(parent, modules_to_react_to_data_dict=modules_to_react_to_data_dict)
        self.setupUi(self)
        self.volume_plugin_data = volume_plugin_data
        self.volume_params_table = None
        self.table_inserted = ParseMode.BY_CELL

        self.selected_row = None

        self.connect_all_signals()

        self.draw_ui()

        self.showNormal()

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
        self.table_inserted = ParseMode.GLOBAL

    def insert_by_type_params_table(self):
        self.volume_params_table = TableComponent(module_data=self.volume_plugin_data.by_type_params)
        self.remove_table()
        self.by_type_GB.layout().addWidget(self.volume_params_table.get_ui())

        self.table_inserted = ParseMode.BY_TYPE

    def remove_table(self):
        if self.by_type_GB.layout().count() > 0:
            self.by_type_GB.layout().takeAt(0)

    def connect_all_signals(self):
        print("connecting signals - to implement")
        self.global_RB.toggled.connect(self.handle_global_RB_toggled)
        self.by_type_RB.toggled.connect(self.handle_by_type_RB_toggled)
        self.ok_PB.clicked.connect(self.accept)
        self.cancel_PB.clicked.connect(self.reject)


    def handle_global_RB_toggled(self, flag):

        if flag:
            self.by_type_GB.show()
            if self.volume_plugin_data.global_params is None:
                self.volume_plugin_data.global_params = self.volume_plugin_data.get_default_global_params()

            if self.table_inserted != ParseMode.GLOBAL:
                self.insert_global_params_table()
                self.volume_plugin_data.mode = ParseMode.GLOBAL

    def handle_by_type_RB_toggled(self, flag):

        if flag:
            self.by_type_GB.show()
            if self.volume_plugin_data.by_type_params is None:
                cell_type_plugin_data = self.get_parsed_module_data(module_name="CellType")
                cell_types = cell_type_plugin_data.get_cell_types()
                self.volume_plugin_data.by_type_params = self.volume_plugin_data.get_default_by_type_params(
                    cell_types=cell_types
                )
            else:
                self.volume_plugin_data.update_from_dependent_modules(
                    dependent_module_data_dict=self.modules_to_react_to_data_dict
                )

            if self.table_inserted != ParseMode.BY_TYPE:
                self.insert_by_type_params_table()
                self.volume_plugin_data.mode = ParseMode.BY_TYPE

    def handle_by_cell_RB_toggled(self, flag):
        if flag:
            self.volume_plugin_data.mode = ParseMode.BY_CELL
            self.by_type_GB.hide()

    def accept(self):
        self.user_decision = True
        self.close()

    def reject(self):
        self.user_decision = False
        self.close()
