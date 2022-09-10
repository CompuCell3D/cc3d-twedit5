# Start-Of-Header

name = "CellType"

author = "T.J. Sego"

version = "0.0.0"

class_name = "CellTypeTool"

module_type = "Plugin"

short_description = "CellType plugin tool"

long_description = """This tool provides model design support for the CellType plugin, including a graphical user 
interface and CC3DML parser and generator"""

tool_tip = """This tool provides model design support for the CellType plugin"""

# End-Of-Header

from collections import OrderedDict
from copy import deepcopy
from itertools import product
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from cc3d.cpp.CC3DXML import *
from cc3d.core.XMLUtils import ElementCC3D, CC3DXMLListPy
from cc3d.core.XMLUtils import dictionaryToMapStrStr as d2mss

from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CC3DModelToolBase import CC3DModelToolBase
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CellType.celltypedlg import CellTypeGUI
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CellType.CellTypePluginData import CellTypePluginData
from cc3d.twedit5.Plugins.PluginCCDGUIDesign import CC3DGUIDesign


class CellTypeTool(CC3DModelToolBase):
    def __init__(
        self, sim_dicts=None, root_element=None, parent_ui: QObject = None, design_gui_plugin: CC3DGUIDesign = None
    ):
        self._dict_keys_to = ["data"]
        self._dict_keys_from = []
        self._requisite_modules = ["Potts"]

        self.cell_type_names = None
        self.cell_type_ids = None
        self.cell_types_frozen = None
        self.cell_type_plugin_data = None

        super(CellTypeTool, self).__init__(
            dict_keys_to=self._dict_keys_to,
            dict_keys_from=self._dict_keys_from,
            requisite_modules=self._requisite_modules,
            sim_dicts=sim_dicts,
            root_element=root_element,
            parent_ui=parent_ui,
            design_gui_plugin=design_gui_plugin
        )

        self._user_decision = True

    @staticmethod
    def get_module_data_class():
        """returns CellTypePluginData"""
        return CellTypePluginData

    def load_xml(self, root_element: CC3DXMLElement) -> None:
        """
        Loads plugin data from root XML element
        :param root_element: root simulation CC3D XML element
        :return: None
        """
        self.parse_dependent_modules(root_element=root_element)
        self.cell_type_plugin_data = CellTypePluginData()
        self.cell_type_plugin_data.parse_xml(root_element=root_element)

    def get_tool_element(self):
        """
        Returns base tool CC3D element
        :return:
        """
        return ElementCC3D("Plugin", {"Name": "CellType"})

    def generate(self):
        """
        Generates plugin element from current sim dictionary states
        :return: plugin element from current sim dictionary states
        """
        return self.cell_type_plugin_data.generate_xml_element()

    def _process_imports(self) -> None:
        """
        Performs internal UI processing of dictionary/XML inputs during initialization
        This is where UI internal attributes are initialized, potential disagreements between multiple
        information inputs are reconciled, and default data is set
        :return: None
        """
        if self._sim_dicts is None or not self._sim_dicts:
            return

        self.cell_type_ids = []
        self.cell_type_names = []
        self.cell_types_frozen = []

        cell_type_data = self._sim_dicts["data"]
        if cell_type_data is None:
            return
        type_ids = list(cell_type_data.keys())
        type_ids.sort()

        type_id = 0
        for tid in type_ids:
            self.cell_type_ids.append(type_id)
            self.cell_type_names.append(cell_type_data[tid][0])
            self.cell_types_frozen.append(cell_type_data[tid][1])
            type_id += 1

    def validate_dicts(self, sim_dicts=None) -> bool:
        """
        Validates current sim dictionary states against changes
        :param sim_dicts: sim dictionaries with changes
        :return:{bool} valid flag is low when changes in sim_dicts affects UI data
        """
        if sim_dicts is None:
            return True

        new_data = sim_dicts["data"]
        current_data = self._sim_dicts["data"]

        if new_data is current_data:
            return True
        elif new_data is None and current_data is not None:
            return False
        elif new_data is not None and current_data is None:
            return False
        elif new_data and not current_data:
            return False
        elif not new_data and current_data:
            return False
        else:
            return new_data == current_data

    def _append_to_global_dict(self, global_sim_dict: dict = None, local_sim_dict: dict = None):
        """
        Public method to append internal sim dictionary; does not call internal update
        :param global_sim_dict: sim dictionary of entire simulation
        :param local_sim_dict: local sim dictionary; default internal dictionary
        :return:
        """

        if global_sim_dict is None:
            global_sim_dict = {}

        if local_sim_dict is not None:
            global_sim_dict["data"] = local_sim_dict["data"]
        else:
            if self._sim_dicts is None:
                self._sim_dicts = {}
                global_sim_dict["data"] = None

            global_sim_dict["data"] = deepcopy(self._sim_dicts["data"])

        return global_sim_dict

    def get_ui(self):
        """
        Returns UI widget
        :return:
        """
        return CellTypeGUI(cell_type_plugin_data=self.cell_type_plugin_data)

    def _process_ui_finish(self, gui: CellTypeGUI):
        """
        Protected method to process user feedback on GUI close
        :param gui: tool gui object
        :return: None
        """
        if not gui.user_decision:
            return
        self.cell_type_plugin_data = gui.cell_type_plugin_data

    def update_dicts(self):
        """
        Public method to update sim dictionaries from internal data
        :return: None
        """
        self._sim_dicts["data"] = {
            self.cell_type_ids[i]: (self.cell_type_names[i], self.cell_types_frozen[i])
            for i in range(self.cell_type_ids.__len__())
        }
        return None
