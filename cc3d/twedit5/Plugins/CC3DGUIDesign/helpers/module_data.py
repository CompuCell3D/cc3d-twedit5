from dataclasses import dataclass
import pandas as pd
from typing import List


@dataclass
class ModuleData:
    df: pd.DataFrame = None
    types: List = None
    editable_columns: List = None