from dataclasses import dataclass
import pandas as pd
import numpy as np
from typing import List, Type
from enum import Enum


@dataclass
class TableType:
    ROW_LIST = 0b1
    MATRIX = 0b1 << 1
    IS_SYMMETRIC = 0b1 << 2


@dataclass
class ModuleData:
    df: pd.DataFrame = None
    arr: np.ndarray = None
    arr_columns: List = None
    arr_element_type: Type = None
    types: List = None
    editable_columns: List = None
    table_type: TableType = TableType.ROW_LIST


if __name__ == '__main__':

    print(TableType.ROW_LIST)
    print(TableType.MATRIX)
    print(TableType.IS_SYMMETRIC|TableType.MATRIX)
    print(6 & TableType.ROW_LIST)
