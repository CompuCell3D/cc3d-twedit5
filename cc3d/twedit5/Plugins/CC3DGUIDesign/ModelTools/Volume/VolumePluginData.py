from dataclasses import dataclass
from typing import Dict


@dataclass
class VolumeByTypePluginData:
    target_volume: str = None
    lambda_volume: str = None

    def __ne__(self, other):
        return self.lambda_volume != other.lambda_volume or self.target_volume != other.target_volume


@dataclass
class VolumePluginData:
    global_params: VolumeByTypePluginData = None
    by_type_params: Dict[str, VolumeByTypePluginData] = None
