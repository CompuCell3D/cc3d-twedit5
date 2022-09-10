from dataclasses import dataclass, field
from typing import Optional
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.module_data import ModuleData, TableType
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.xml_parse_data import XMLParseData, ParseMode
from cc3d.core.XMLUtils import dictionaryToMapStrStr as d2mss
from cc3d.core.XMLUtils import ElementCC3D, CC3DXMLListPy

import numpy as np


@dataclass
class ContactPluginData(XMLParseData):
    global_params: ModuleData = None
    neighbor_order: int = 1

    def get_default_params(self):

        return ModuleData(
            arr=np.zeros(shape=[1, 1], dtype=float),
            arr_columns=["Medium"],
            arr_element_type=float,
            table_type=TableType.MATRIX | TableType.IS_SYMMETRIC,
        )

    def parse_xml(self, root_element):
        sim_dicts = {}
        plugin_element = root_element.getFirstElement("Plugin", d2mss({"Name": "Contact"}))
        if plugin_element is None:
            return sim_dicts

        # sorting by type is handled in update_from_dependent_modules.
        # here we are doing verbatim parsing of current xml
        neighbor_order_elem = plugin_element.getFirstElement("NeighborOrder")
        if neighbor_order_elem:
            self.neighbor_order = int(abs(neighbor_order_elem.getInt()))

        energy_dict = {}
        plugin_elements = CC3DXMLListPy(plugin_element.getElements("Energy"))
        cell_type_set = set()
        for plugin_element in plugin_elements:
            type_1 = plugin_element.getAttribute("Type1")
            type_2 = plugin_element.getAttribute("Type2")
            cell_type_set.add(type_1)
            cell_type_set.add(type_2)
            energy = plugin_element.getDouble()
            energy_dict[f"{type_1}|{type_2}"] = energy
            energy_dict[f"{type_2}|{type_1}"] = energy

        arr = np.zeros(shape=[len(cell_type_set), len(cell_type_set)], dtype=float)
        # sorting according to type id is handled in update_from_dependent_modules
        cell_type_list = list(cell_type_set)
        for i in range(0, len(cell_type_list)):
            for j in range(i, len(cell_type_list)):
                type_i = cell_type_list[i]
                type_j = cell_type_list[j]

                try:
                    energy = energy_dict[f"{type_i}|{type_j}"]
                except KeyError:
                    continue
                arr[i, j] = energy
                arr[j, i] = energy

        self.mode = ParseMode.GLOBAL

        self.global_params = ModuleData(
            arr=arr,
            arr_columns=cell_type_list,
            arr_element_type=float,
            table_type=TableType.MATRIX | TableType.IS_SYMMETRIC,
        )

    def generate_xml_element(self) -> Optional[ElementCC3D]:
        """
        Abstract fcn - reimplement XML Element in derived class
        """
        element = self.get_tool_element()

        gp = self.global_params

        cell_types = gp.arr_columns
        energy_arr = gp.arr

        for i in range(len(cell_types)):
            for j in range(i, len(cell_types)):
                attrs = {'Type1': cell_types[i], 'Type2': cell_types[j]}
                element.ElementCC3D("Energy", attrs, energy_arr[i, j])

        element.ElementCC3D("NeighborOrder", {}, self.neighbor_order)
        return element

    def get_tool_element(self):
        """
        Returns base tool CC3D element
        :return:
        """
        return ElementCC3D("Plugin", {"Name": "Contact"})

    def update_from_dependent_modules(self, dependent_module_data_dict):
        cell_type_plugin_data = dependent_module_data_dict.get('CellType', None)
        if cell_type_plugin_data is None:
            return

        updated_cell_types = cell_type_plugin_data.get_cell_types()

        # creating handy dictionary that  summarizes contact plugin types and energy entries and is convenient to
        # work with when building new array based on new cell types, also convenient during reordering columns ets

        # current energy matrix storage
        energy_dict = {}
        current_cell_types = self.global_params.arr_columns
        for i in range(len(current_cell_types)):
            for j in range(i, len(current_cell_types)):
                energy_dict[f"{current_cell_types[i]}|{current_cell_types[j]}"] = self.global_params.arr[i, j]
                energy_dict[f"{current_cell_types[j]}|{current_cell_types[i]}"] = self.global_params.arr[j, i]

        size_updated_types = len(updated_cell_types)
        new_arr = np.zeros(shape=[size_updated_types, size_updated_types], dtype=float)

        # updating step
        for i in range(size_updated_types):
            for j in range(i, size_updated_types):
                energy = energy_dict.get(f"{updated_cell_types[i]}|{updated_cell_types[j]}", None)
                if energy is None:
                    continue
                new_arr[i, j] = energy
                new_arr[j, i] = energy
        self.global_params.arr = new_arr
        self.global_params.arr_columns = updated_cell_types
