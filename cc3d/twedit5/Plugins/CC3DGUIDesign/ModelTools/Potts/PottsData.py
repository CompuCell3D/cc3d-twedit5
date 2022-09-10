from dataclasses import dataclass, field
from typing import Optional, List, Dict
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.module_data import ModuleData, TableType
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.xml_parse_data import XMLParseData, ParseMode
from cc3d.core.XMLUtils import dictionaryToMapStrStr as d2mss
from cc3d.core.XMLUtils import ElementCC3D, CC3DXMLListPy
import numpy as np


@dataclass
class PottsData(XMLParseData):
    neighbor_order: int = 1
    dim: List[int] = field(default_factory=lambda: [256, 256, 1])
    membrane_fluctuations: float = 10.
    mcs: int = 10000
    lattice_type: str = "Square"
    boundary_conditions: Dict[str, str] = field(default=lambda: {"x": "NoFlux", "y": "NoFlux", "z": "NoFlux"})
    offset: float = 0.
    k_boltzman: float = 1.0
    anneal: int = 0
    flip_2_dim_ratio: float = 1.0
    debug_output_frequency: int = None
    random_seed: int = None
    energy_function_calculator: object = None

    def get_default_params(self):
        return None
        # return ModuleData(
        #     arr=np.zeros(shape=[1, 1], dtype=float),
        #     arr_columns=["Medium"],
        #     arr_element_type=float,
        #     table_type=TableType.MATRIX | TableType.IS_SYMMETRIC,
        # )

    def parse_xml(self, root_element):
        # todo - parse boundary conditions

        potts_element = root_element.getFirstElement("Potts")

        element = potts_element.getFirstElement("Dimensions")
        if element:

            if element.findAttribute("x"):
                self.dim[0] = element.getAttributeAsUInt("x")

            if element.findAttribute("y"):
                self.dim[1] = element.getAttributeAsUInt("y")

            if element.findAttribute("z"):
                self.dim[2] = element.getAttributeAsUInt("z")

        element = potts_element.getFirstElement("FluctuationAmplitude")
        if element:

            p_elements = CC3DXMLListPy(element.getElements("FluctuationAmplitudeParameters"))
            if p_elements:
                # todo - implement it
                print('IMPLEMENT ME!')
            #     gpd["MembraneFluctuations"] = {"Parameters": {}, "FunctionName": "Min"}
            #     p_element: CC3DXMLElement
            #     for p_element in p_elements:
            #         cell_type = p_element.getAttribute("CellType")
            #         amp = float(p_element.getAttribute("FluctuationAmplitude"))
            #         gpd["MembraneFluctuations"]["Parameters"][cell_type] = amp
            #
            #     f_element: CC3DXMLElement = potts_element.getFirstElement("FluctuationAmplitudeFunctionName")
            #     if f_element:
            #         gpd["MembraneFluctuations"]["FunctionName"] = f_element.getText()
            #     else:
            #         gpd["MembraneFluctuations"] = float(element.getText())

            else:
                self.membrane_fluctuations = float(element.getText())

        # parsing boundary conditions
        boundary_conditions_dict = {"x": "NoFlux", "y": "NoFlux", "z": "NoFlux"}
        valid_boundary_conditions = ["NoFlux", "Periodic"]
        axes = ["x", "y", "z"]
        for axis in axes:
            bc_element = potts_element.getFirstElement(f"Boundary_{axis}")
            if bc_element:
                bc_type = bc_element.getText()
                if bc_type in valid_boundary_conditions:
                    boundary_conditions_dict[axis] = bc_type

        self.boundary_conditions = boundary_conditions_dict

        element = potts_element.getFirstElement("Temperature")
        if element:
            self.membrane_fluctuations = float(element.getText())

        n_element = potts_element.getFirstElement("NeighborOrder")

        if n_element:
            self.neighbor_order = int(n_element.getText())

        s_element = potts_element.getFirstElement("Steps")

        if s_element:
            self.mcs = int(s_element.getText())

        offset_element = potts_element.getFirstElement("Offset")
        if offset_element:
            self.offset = float(offset_element.getText())

        coefficient_element = potts_element.getFirstElement("KBoltzman")
        if coefficient_element:
            self.k_boltzman = float(coefficient_element.getText())

        anneal_element = potts_element.getFirstElement("Anneal")
        if anneal_element:
            self.anneal = int(anneal_element.getText())

        flip_to_dim_ratio_element = potts_element.getFirstElement("Flip2DimRatio")
        if flip_to_dim_ratio_element:
            self.flip_2_dim_ratio = float(flip_to_dim_ratio_element.getText())

        debug_output_freq_element = potts_element.getFirstElement("DebugOutputFrequency")
        if debug_output_freq_element:
            self.debug_output_frequency = int(debug_output_freq_element.getText())

        random_seed_element = potts_element.getFirstElement("RandomSeed")
        if random_seed_element:
            self.random_seed = int(random_seed_element.getText())

        # # implement it
        # energy_func_calc_element = potts_element.getFirstElement("EnergyFunctionCalculator")
        # if energy_func_calc_element:
        #     func_type = energy_func_calc_element.getAttribute("Type")
        #
        #     file_name_element = energy_func_calc_element.getFirstElement("OutputFileName")
        #     file_name = file_name_element.getText()
        #     file_freq = float(file_name_element.getAttribute("Frequency"))
        #
        #     spin_element = energy_func_calc_element.getFirstElement("OutputCoreFileNameSpinFlips")
        #     spin_name = spin_element.getText()
        #     spin_freq = float(spin_element.getAttribute("Frequency"))
        #     gather_results = spin_element.findAttribute("GatherResults")
        #     output_accepted = spin_element.findAttribute("OutputAccepted")
        #     output_rejected = spin_element.findAttribute("OutputRejected")
        #     output_total = spin_element.findAttribute("OutputTotal")
        #
        #     gpd["EnergyFunctionCalculator"] = {
        #         "Type": func_type,
        #         "OutputFileName": {"OutputFileName": file_name, "Frequency": file_freq},
        #         "OutputCoreFileNameSpinFlips": {
        #             "OutputCoreFileNameSpinFlips": spin_name,
        #             "Frequency": spin_freq,
        #             "GatherResults": gather_results,
        #             "OutputAccepted": output_accepted,
        #             "OutputRejected": output_rejected,
        #             "OutputTotal": output_total,
        #         },
        #     }



    def generate_xml_element(self) -> Optional[ElementCC3D]:
        """
        Abstract fcn - reimplement XML Element in derived class
        """
        element = self.get_tool_element()

        element.ElementCC3D("Dimensions", {"x": self.dim[0], "y": self.dim[1], "z": self.dim[2]})
        element.ElementCC3D("Steps", {}, self.mcs)

        # todo - implement proper handling of more complex definitions of membrane fluctuations
        # if isinstance(gpd["MembraneFluctuations"], dict):
        #     mf_element = element.ElementCC3D("FluctuationAmplitude", {})
        #     for cell_type, param in gpd["MembraneFluctuations"]["Parameters"].items():
        #         mf_element.ElementCC3D(
        #             "FluctuationAmplitudeParameters", {"CellType": cell_type, "FluctuationAmplitude": str(param)}
        #         )
        #
        #     element.ElementCC3D("FluctuationAmplitudeFunctionName", {}, gpd["MembraneFluctuations"]["FunctionName"])
        # else:
        element.ElementCC3D("FluctuationAmplitude", {}, self.membrane_fluctuations)
        element.ElementCC3D("NeighborOrder", {}, self.neighbor_order)

        element.ElementCC3D("LatticeType", {}, self.lattice_type)

        if self.dim[2] > 1:
            dim_list = ["x", "y", "z"]
        else:
            dim_list = ["x", "y"]
        [
            element.ElementCC3D("Boundary_" + dim_name, {}, self.boundary_conditions[dim_name])
            for dim_name in dim_list
        ]
        if self.offset != 0.:
            element.ElementCC3D("Offset", {}, self.offset)

        if self.k_boltzman != 1.:
            element.ElementCC3D("KBoltzman", {}, self.k_boltzman)

        if self.anneal != 0:
            element.ElementCC3D("Anneal", {}, self.anneal)

        if self.flip_2_dim_ratio != 1.0:
            element.ElementCC3D("Flip2DimRatio", {}, self.flip_2_dim_ratio)

        if self.debug_output_frequency is not None:
            element.ElementCC3D("DebugOutputFrequency", {}, self.debug_output_frequency)

        if self.random_seed is not None:
            element.ElementCC3D("RandomSeed", {}, int(self.random_seed))

        # todo implement energy function calculator
        # if gpd["EnergyFunctionCalculator"] != default_gpd()["EnergyFunctionCalculator"]:
        #     energy_func_calc_element: ElementCC3D = element.ElementCC3D(
        #         "EnergyFunctionCalculator", {"Type": gpd["EnergyFunctionCalculator"]["Type"]}
        #     )
        #     energy_func_calc_element.ElementCC3D(
        #         "OutputFileName",
        #         {"Frequency": gpd["EnergyFunctionCalculator"]["OutputFileName"]["Frequency"]},
        #         gpd["EnergyFunctionCalculator"]["OutputFileName"]["OutputFileName"],
        #     )
        #     ef_dict = {"Frequency": gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["Frequency"]}
        #     if gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["GatherResults"]:
        #         ef_dict["GatherResults"] = ""
        #     if gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputAccepted"]:
        #         ef_dict["OutputAccepted"] = ""
        #     if gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputRejected"]:
        #         ef_dict["OutputRejected"] = ""
        #     if gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputTotal"]:
        #         ef_dict["OutputTotal"] = ""
        #     energy_func_calc_element.ElementCC3D(
        #         "OutputCoreFileNameSpinFlips",
        #         ef_dict,
        #         gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputCoreFileNameSpinFlips"],
        #     )

        return element

    def get_tool_element(self):
        """
        Returns base tool CC3D element
        :return:
        """
        return ElementCC3D("Potts", {})

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
