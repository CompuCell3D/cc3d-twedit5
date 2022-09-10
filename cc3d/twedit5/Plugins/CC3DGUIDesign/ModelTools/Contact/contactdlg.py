from copy import deepcopy
from itertools import product
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CC3DModelToolGUIBase import CC3DModelToolGUIBase
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Contact.ui_contactdlg import Ui_ContactPluginGUI
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Contact.ContactPluginData import ContactPluginData
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.table_component import TableComponent
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.xml_parse_data import XMLParseData
from typing import Dict


class ContactGUI(CC3DModelToolGUIBase, Ui_ContactPluginGUI):
    def __init__(self, parent=None, contact_plugin_data: ContactPluginData = None,
                 modules_to_react_to_data_dict: Dict[str, XMLParseData] = None):
        super(ContactGUI, self).__init__(parent, modules_to_react_to_data_dict=modules_to_react_to_data_dict)
        self.setupUi(self)
        self.contact_plugin_data = contact_plugin_data
        self.contact_plugin_table = None

        self.neighbor_order_list = range(1, 5)
        self.cell_types = None

        self.user_decision = None

        self.valid_color = QColor("black")
        self.invalid_color = QColor("red")

        self.init_data()

        self.draw_ui()

        self.connect_all_signals()

        self.showNormal()

    def init_data(self):
        return

    def draw_ui(self):
        if self.contact_plugin_data is None:
            return
        # cell_type_plugin_data = self.get_parsed_module_data(module_name="CellType")
        # taking into account information about current cell types before displaying data to the user
        self.contact_plugin_data.update_from_dependent_modules(
            dependent_module_data_dict=self.modules_to_react_to_data_dict)

        self.contact_plugin_table = TableComponent(module_data=self.contact_plugin_data.global_params)

        self.energy_GB.layout().addWidget(self.contact_plugin_table.get_ui())
        self.spinBox.setValue(self.contact_plugin_data.neighbor_order)

    def connect_all_signals(self):
        self.ok_PB.clicked.connect(self.handle_accept)
        self.cancel_PB.clicked.connect(self.handle_reject)

    def handle_accept(self):
        self.user_decision = True
        self.close()

    def handle_reject(self):
        self.user_decision = False
        self.close()
