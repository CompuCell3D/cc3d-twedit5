# Start-Of-Header

name = 'Volume'

author = 'T.J. Sego, Maciek Swat'

version = '0.0.0'

class_name = 'VolumeTool'

module_type = 'Plugin'

short_description = 'Volume plugin tool'

long_description = """This tool provides model design support for the Volume plugin, including a graphical user 
interface and CC3DML parser and generator"""

tool_tip = """This tool provides model design support for the Volume plugin"""

# End-Of-Header

from collections import OrderedDict
from copy import deepcopy
from itertools import product
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from typing import Dict
from cc3d.cpp.CC3DXML import *
from cc3d.core.XMLUtils import ElementCC3D, CC3DXMLListPy
from cc3d.core.XMLUtils import dictionaryToMapStrStr as d2mss

from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CC3DModelToolBase import CC3DModelToolBase
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Volume.volumedlg import VolumeGUI
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Volume.VolumePluginData import VolumePluginData, VolumeByTypePluginData


class VolumeTool(CC3DModelToolBase):
    def __init__(self, sim_dicts=None, root_element=None, parent_ui: QObject = None):
        self._dict_keys_to = ['data']
        self._dict_keys_from = []
        self._requisite_modules = []


        self.volume_plugin_data = None
        self.updated_volume_plugin_data = None

        super(VolumeTool, self).__init__(dict_keys_to=self._dict_keys_to, dict_keys_from=self._dict_keys_from,
                                         requisite_modules=self._requisite_modules, sim_dicts=sim_dicts,
                                         root_element=root_element, parent_ui=parent_ui,
                                         modules_to_react_to=['CellType'])

        self._user_decision = True

    def load_xml(self, root_element: CC3DXMLElement) -> None:
        """
        Loads plugin data from root XML element
        :param root_element: root simulation CC3D XML element
        :return: None
        """
        self._sim_dicts = load_xml(root_element=root_element)

    def get_tool_element(self):
        """
        Returns base tool CC3D element
        :return:
        """
        return ElementCC3D('Plugin', {'Name': 'Volume'})

    def generate(self):
        """
        Generates plugin element from current sim dictionary states
        :return: plugin element from current sim dictionary states
        """
        element = self.get_tool_element()

        if self.updated_volume_plugin_data is not None:
            gp = self.updated_volume_plugin_data.global_params
            btp = self.updated_volume_plugin_data.by_type_params
            if gp is not None:
                element.ElementCC3D('TargetVolume', {}, gp.target_volume)
                element.ElementCC3D('LambdaVolume', {}, gp.lambda_volume)
            elif btp is not None:
                raise NotImplementedError('Volume By type not implemented')

        return element

    def _process_imports(self) -> None:
        """
        Performs internal UI processing of dictionary/XML inputs during initialization
        This is where UI internal attributes are initialized, potential disagreements between multiple
        information inputs are reconciled, and default data is set
        :return: None
        """
        if self._sim_dicts is None or not self._sim_dicts:
            return

        volume_plugin_data = self._sim_dicts['data']
        if volume_plugin_data is None:
            return
        self.volume_plugin_data = volume_plugin_data

    def validate_dicts(self, sim_dicts=None) -> bool:
        """
        Validates current sim dictionary states against changes
        :param sim_dicts: sim dictionaries with changes
        :return:{bool} valid flag is low when changes in sim_dicts affects UI data
        """
        if sim_dicts is None:
            return True

        new_data = sim_dicts['data']
        current_data = self._sim_dicts['data']

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
            global_sim_dict['data'] = local_sim_dict['data']
        else:
            if self._sim_dicts is None:
                self._sim_dicts = {}
                global_sim_dict['data'] = None

            global_sim_dict['data'] = deepcopy(self._sim_dicts['data'])

        return global_sim_dict

    def get_ui(self):
        """
        Returns UI widget
        :return:
        """
        return VolumeGUI(volume_plugin_data=self.volume_plugin_data)

    def _process_ui_finish(self, gui: VolumeGUI):
        """
        Protected method to process user feedback on GUI close
        :param gui: tool gui object
        :return: None
        """
        if not gui.user_decision:
            return
        new_volume_plugin_data = VolumePluginData()
        if gui.global_RB:
            new_volume_plugin_data.global_params = VolumeByTypePluginData(
                target_volume=gui.target_vol_LE.text(), lambda_volume=gui.lambda_vol_LE.text()
            )
            if new_volume_plugin_data != self.volume_plugin_data:
                self.updated_volume_plugin_data = new_volume_plugin_data

    def update_dicts(self):
        """
        Public method to update sim dictionaries from internal data
        :return: None
        """
        # self._sim_dicts['data'] = {self.cell_type_ids[i]: (self.cell_type_names[i], self.cell_types_frozen[i])
        #                            for i in range(self.cell_type_ids.__len__())}
        return None


def load_xml(root_element) -> {}:
    sim_dicts = {}
    for key in VolumeTool().dict_keys_from() + VolumeTool().dict_keys_to():
        sim_dicts[key] = None

    plugin_element = root_element.getFirstElement('Plugin', d2mss({'Name': 'Volume'}))

    if plugin_element is None:
        return sim_dicts

    global_settings = False
    by_type_settings = False
    by_cell_settings = False
    target_volume = None
    lambda_volume = None

    if plugin_element.findElement('TargetVolume'):
        target_volume = plugin_element.getFirstElement('TargetVolume').getDouble()
        # if sim_dicts['data'] is None:
        #     sim_dicts['data'] = {}
        #
        # sim_dicts['data']['TargetVolume'] = plugin_element.getFirstElement('TargetVolume').getDouble()
        # global_settings = True

    if plugin_element.findElement('LambdaVolume'):
        lambda_volume = plugin_element.getFirstElement('LambdaVolume').getDouble()
        # if sim_dicts['data'] is None:
        #     sim_dicts['data'] = {}
        #
        # sim_dicts['data']['LambdaVolume'] = plugin_element.getFirstElement('LambdaVolume').getDouble()
        # global_settings = True

    if lambda_volume is not None and target_volume is not None:
        sim_dicts['data'] = VolumePluginData(
            global_params=VolumeByTypePluginData(lambda_volume=lambda_volume, target_volume=target_volume))

    # sim_dicts['global_settings'] = global_settings
    # sim_dicts['by_type_settings'] = by_type_settings
    # sim_dicts['by_cell_settings'] = by_cell_settings
    # type_table = {}
    # plugin_elements = CC3DXMLListPy(plugin_element.getElements('CellType'))
    # for plugin_element in plugin_elements:
    #     type_id = int(plugin_element.getAttribute('TypeId'))
    #     type_name = plugin_element.getAttribute('TypeName')
    #     is_freeze = plugin_element.findAttribute('Freeze')
    #     type_table[type_id] = (type_name, is_freeze)
    #
    # sim_dicts['data'] = type_table

    return sim_dicts
