from dataclasses import dataclass, field
from typing import Optional
import pandas as pd
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.module_data import ModuleData
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.xml_parse_data import XMLParseData, ParseMode
from cc3d.core.XMLUtils import dictionaryToMapStrStr as d2mss
from cc3d.core.XMLUtils import ElementCC3D, CC3DXMLListPy
from collections import OrderedDict
from typing import List
import numpy as np


@dataclass
class CellTypePluginData(XMLParseData):
    global_params: ModuleData = None
    types: List = field(default_factory=lambda: [str, int, bool])
    cols: List[str] = field(default_factory=lambda: ["TypeId", "TypeName", "Freeze"])
    editable_cols: List[str] = field(default_factory=lambda: ["TypeName", "Freeze"])

    def get_default_params(self):

        return ModuleData(
            df=pd.DataFrame([[0, "Medium", False]], columns=self.cols),
            types=self.types,
            editable_columns=self.editable_cols,
        )

    def get_cell_types(self) -> List[str]:
        """returns list of cell types ordered by cell type
        """
        # ordering types by cell type id
        cell_types = self.global_params.df['TypeName'].values
        cell_type_ids = self.global_params.df['TypeId'].values
        cell_type_ids_argsort = np.argsort(cell_type_ids)
        # actual ordering
        cell_types = cell_types[cell_type_ids_argsort]

        return cell_types

    def parse_xml(self, root_element):
        sim_dicts = {}
        plugin_element = root_element.getFirstElement("Plugin", d2mss({"Name": "CellType"}))
        if plugin_element is None:
            return sim_dicts

        data = []
        plugin_elements = CC3DXMLListPy(plugin_element.getElements("CellType"))
        for plugin_element in plugin_elements:
            type_id = int(plugin_element.getAttribute("TypeId"))
            type_name = plugin_element.getAttribute("TypeName")
            freeze = plugin_element.findAttribute("Freeze")
            data.append([type_id, type_name, freeze])

        self.mode = ParseMode.GLOBAL
        self.global_params = ModuleData(
            df=pd.DataFrame(data=data, columns=self.cols), types=self.types, editable_columns=self.editable_cols
        )

    def generate_xml_element(self) -> Optional[ElementCC3D]:
        """
        Abstract fcn - reimplement XML Element in derived class
        """
        element = self.get_tool_element()

        gp = self.global_params

        for i, row in gp.df.iterrows():
            attrs = OrderedDict()
            attrs["TypeName"] = row.TypeName
            attrs["TypeId"] = row.TypeId
            if row.Freeze:
                attrs["Freeze"] = ""

            element.ElementCC3D("CellType", attrs)

        return element

    def get_tool_element(self):
        """
        Returns base tool CC3D element
        :return:
        """
        return ElementCC3D("Plugin", {"Name": "CellType"})

    def get_cell_type_row(self, cell_type_name: str, freeze: bool = False):
        if not self.validate_type_name(cell_type_name=cell_type_name):
            return
        next_type_id = np.max(self.global_params.df["TypeId"]) + 1
        insert_row = {
            "TypeName": cell_type_name,
            "TypeId": next_type_id,
            "Freeze": freeze,
        }
        return pd.DataFrame([insert_row])

    def clear(self):
        self.global_params.df = self.get_default_params()

    def delete_cell_type(self, cell_type_name):

        mask = ~(self.global_params.df["TypeName"] == cell_type_name)
        self.global_params.df = self.global_params.df[mask]

    def validate_type_name(self, cell_type_name: str):
        cell_type_name = cell_type_name.strip()
        name_has_spaces = " " in cell_type_name

        return not (
            cell_type_name in self.global_params.df["TypeName"]
            or cell_type_name == "Medium"
            or cell_type_name.__len__() < 1
            or name_has_spaces
        )
