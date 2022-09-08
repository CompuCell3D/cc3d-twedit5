from dataclasses import dataclass
import pandas as pd
import numpy as np
from typing import List, Type
from enum import Enum


class TableType(Enum):
    ROW_LIST = 1
    MATRIX = 2


@dataclass
class ModuleData:
    df: pd.DataFrame = None
    arr: np.ndarray = None
    arr_columns: List = None
    arr_element_type: Type = None
    types: List = None
    editable_columns: List = None
    table_type: TableType = TableType.ROW_LIST
