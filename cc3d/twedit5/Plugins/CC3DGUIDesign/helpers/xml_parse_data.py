from dataclasses import dataclass
from cc3d.core.XMLUtils import ElementCC3D
from typing import Optional
from enum import Enum


class ParseMode(Enum):
    GLOBAL = 1
    BY_TYPE = 2
    BY_CELL = 3


@dataclass
class XMLParseData:
    mode: ParseMode = ParseMode.GLOBAL

    def parse_xml(self, root_element: ElementCC3D):
        """Abstract fcn - reimplement XML parsing in derived class
        """
        pass

    def generate_xml_element(self) -> Optional[ElementCC3D]:
        """
        Abstract fcn - reimplement XML Element in derived class
        """
        return None

    def get_tool_element(self):
        """
        Returns base tool CC3D element
        :return:
        """
        return ElementCC3D('Module')