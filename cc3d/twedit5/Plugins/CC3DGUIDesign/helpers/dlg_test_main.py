import sip

sip.setapi('QString', 1)
sip.setapi('QVariant', 1)

import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.module_data import ModuleData
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.table_component import TableComponent
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Volume.volumedlg import VolumeGUI
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Volume.VolumePluginData import VolumePluginData


if __name__ == '__main__':
    app = QApplication(sys.argv)  # needs to be defined first
    module_data = ModuleData(
        df=pd.DataFrame(data=[['Condensing', 25.0, 2.0, True],
                              ['NonCondensing', 26.0, 2.1, False]],
                        columns=['CellType', 'TargetVolume', 'LambdaVolume', 'Freeze']),
        types=[str, float, float, bool],
        editable_columns=['TargetVolume', 'LambdaVolume', 'Freeze']

    )
    table_component = TableComponent(module_data=module_data)
    vpd = VolumePluginData  (by_type_params=module_data)

    v_gui = VolumeGUI(volume_plugin_data=vpd)
    v_gui.draw_ui()
    v_gui.show()
    sys.exit(app.exec_())


