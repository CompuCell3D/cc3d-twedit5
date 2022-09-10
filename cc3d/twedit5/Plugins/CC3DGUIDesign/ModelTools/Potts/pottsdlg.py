from collections import OrderedDict
from copy import deepcopy
from itertools import product
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.CC3DModelToolGUIBase import CC3DModelToolGUIBase
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Potts.ui_pottsdlg import Ui_PottsGUI
from cc3d.twedit5.Plugins.CC3DGUIDesign.ModelTools.Potts.PottsData import PottsData


class PottsGUI(CC3DModelToolGUIBase, Ui_PottsGUI):
    def __init__(self, parent=None, potts_data: PottsData = None):
        super(PottsGUI, self).__init__(parent)
        self.setupUi(self)
        self.potts_data = potts_data

        self.__default_ef_file_name = 'statData.txt'
        self.default_function = 'Default'

        # self.gpd = deepcopy(gpd)
        # self.valid_functions = valid_functions
        # self.default_function = 'Default'
        # if self.default_function not in self.valid_functions:
        #     self.valid_functions.append(self.default_function)

        self.user_decision = None

        # self.cell_types = [cell_type for cell_type in cell_types if cell_type != "Medium"]

        # if isinstance(self.gpd["MembraneFluctuations"], dict):
        #     self.show_cell_types = True
        #     self.type_params = {cell_type: self.gpd["MembraneFluctuations"]['Parameters'][cell_type]
        #                         for cell_type in self.cell_types}
        # else:
        #     self.show_cell_types = False
        #     self.type_params = {cell_type: 0.0 for cell_type in self.cell_types}

        # self.init_ui()
        self.draw_ui()

        self.connect_all_signals()

        self.showNormal()
    # def init_ui(self):
    #     self.xDimSB.setValue(self.gpd["Dim"][0])
    #     self.yDimSB.setValue(self.gpd["Dim"][1])
    #     self.zDimSB.setValue(self.gpd["Dim"][2])
    #
    #     self.fluctuation_FcnCB.addItems(self.valid_functions)
    #     if self.cell_types:
    #         self.cell_TypeCB.addItems(self.cell_types)
    #         self.cell_TypeCB.setCurrentText(self.cell_types[0])
    #         self.type_ParamLE.setText(str(self.type_params[self.cell_TypeCB.currentText()]))
    #     else:
    #         self.type_ParamLE.setEnabled(False)
    #
    #     if self.show_cell_types:
    #         self.membraneFluctuationsLE.setText(str(10))
    #         self.fluctuation_FcnCB.setCurrentText(self.gpd['MembraneFluctuations']['FunctionName'])
    #     else:
    #         self.membraneFluctuationsLE.setText(str(self.gpd["MembraneFluctuations"]))
    #         self.fluctuation_FcnCB.setCurrentText(self.default_function)
    #     self.membraneFluctuationsLE.setValidator(QDoubleValidator())
    #     self.type_ParamLE.setValidator(QDoubleValidator())
    #
    #     self.neighborOrderSB.setValue(self.gpd["NeighborOrder"])
    #
    #     self.mcsSB.setValue(self.gpd["MCS"])
    #
    #     self.latticeTypeCB.setCurrentText(self.gpd["LatticeType"])
    #
    #     self.xbcCB.setCurrentText(self.gpd["BoundaryConditions"]['x'])
    #     self.ybcCB.setCurrentText(self.gpd["BoundaryConditions"]['y'])
    #     self.zbcCB.setCurrentText(self.gpd["BoundaryConditions"]['z'])
    #
    #     self.update_fluctuation_fields()
    #
    #     self.offset_SB.setValue(self.gpd["Offset"])
    #     self.coefficient_SB.setValue(self.gpd["KBoltzman"])
    #
    #     self.anneal_SB.setValue(self.gpd["Anneal"])
    #     self.flip_to_dim_SB.setValue(self.gpd["Flip2DimRatio"])
    #
    #     self.debug_CB.setChecked(self.gpd["DebugOutputFrequency"] is not None)
    #     self.debug_enable(self.debug_CB.isChecked())
    #     if self.debug_CB.isChecked():
    #         self.debug_SB.setValue(self.gpd["DebugOutputFrequency"])
    #
    #     self.random_seed_CB.setChecked(self.gpd["RandomSeed"] is not None)
    #     self.random_enable(self.random_seed_CB.isChecked())
    #     if self.random_seed_SB.isEnabled():
    #         self.random_seed_SB.setValue(self.gpd["RandomSeed"])
    #
    #     if isinstance(self.gpd["EnergyFunctionCalculator"], dict):
    #         self.ef_spin_freq_SB.setValue(
    #             self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["Frequency"])
    #         self.ef_results_CB.setChecked(
    #             self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["GatherResults"])
    #         self.ef_accepted_CB.setChecked(
    #             self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputAccepted"])
    #         self.ef_rejected_CB.setChecked(
    #             self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputRejected"])
    #         self.ef_total_CB.setChecked(
    #             self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputTotal"])
    #         self.ef_file_freq_SB.setValue(self.gpd["EnergyFunctionCalculator"]["OutputFileName"]["Frequency"])
    #         self.ef_file_name_LE.setText(
    #             self.gpd["EnergyFunctionCalculator"]["OutputFileName"]["OutputFileName"])
    #     else:
    #         self.ef_file_name_LE.setText(self.__default_ef_file_name)
    #
    #     self.ef_enable_CB.setChecked(isinstance(self.gpd["EnergyFunctionCalculator"], dict))
    #     self.ef_enable_widgets(self.ef_enable_CB.isChecked())
    #
    #     self.tabWidget.setCurrentIndex(0)

    def draw_ui(self):
        if self.potts_data is None:
            return

        # ok_PB = self.buttonBox.button(QDialogButtonBox.Ok)
        self.ok_PB.setAutoDefault(False)
        self.ok_PB.setDefault(False)
        #
        # cancel_PB = self.buttonBox.button(QDialogButtonBox.Cancel)
        self.cancel_PB.setAutoDefault(False)
        self.cancel_PB.setDefault(False)

        pd = self.potts_data
        self.xDimSB.setValue(pd.dim[0])
        self.yDimSB.setValue(pd.dim[1])
        self.zDimSB.setValue(pd.dim[2])

        self.neighborOrderSB.setValue(pd.neighbor_order)
        # todo add handling for more advanced options with membrane fluctuations
        # self.fluctuation_FcnCB.addItems(self.valid_functions)
        # if self.cell_types:
        #     self.cell_TypeCB.addItems(self.cell_types)
        #     self.cell_TypeCB.setCurrentText(self.cell_types[0])
        #     self.type_ParamLE.setText(str(self.type_params[self.cell_TypeCB.currentText()]))
        # else:
        #     self.type_ParamLE.setEnabled(False)
        #
        # if self.show_cell_types:
        #     self.membraneFluctuationsLE.setText(str(10))
        #     self.fluctuation_FcnCB.setCurrentText(self.gpd['MembraneFluctuations']['FunctionName'])
        # else:
        #     self.membraneFluctuationsLE.setText(str(self.gpd["MembraneFluctuations"]))
        #     self.fluctuation_FcnCB.setCurrentText(self.default_function)
        # self.membraneFluctuationsLE.setValidator(QDoubleValidator())
        # self.type_ParamLE.setValidator(QDoubleValidator())

        self.membraneFluctuationsLE.setText(str(pd.membrane_fluctuations))
        self.fluctuation_FcnCB.setCurrentText(self.default_function)
        self.membraneFluctuationsLE.setValidator(QDoubleValidator())

        self.mcsSB.setValue(pd.mcs)

        self.latticeTypeCB.setCurrentText(pd.lattice_type)

        self.xbcCB.setCurrentText(pd.boundary_conditions['x'])
        self.ybcCB.setCurrentText(pd.boundary_conditions['y'])
        self.zbcCB.setCurrentText(pd.boundary_conditions['z'])

        self.offset_LE.setValidator(QDoubleValidator())
        self.offset_LE.setText(str(pd.offset))

        self.coefficient_LE.setValidator(QDoubleValidator())
        self.coefficient_LE.setText(str(pd.k_boltzman))

        self.anneal_SB.setValue(pd.anneal)

        self.flip_to_dim_LE.setValidator(QDoubleValidator())
        self.flip_to_dim_LE.setText(str(pd.flip_2_dim_ratio))

        self.debug_CB.setChecked(pd.debug_output_frequency is not None)
        self.debug_enable(self.debug_CB.isChecked())
        if self.debug_CB.isChecked():
            self.debug_SB.setValue(pd.debug_output_frequency)

        self.random_seed_CB.setChecked(pd.random_seed is not None)
        self.random_enable(self.random_seed_CB.isChecked())
        if self.random_seed_SB.isEnabled():
            self.random_seed_SB.setValue(pd.random_seed)

        # todo handle more advanced options
        # if isinstance(self.gpd["EnergyFunctionCalculator"], dict):
        #     self.ef_spin_freq_SB.setValue(
        #         self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["Frequency"])
        #     self.ef_results_CB.setChecked(
        #         self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["GatherResults"])
        #     self.ef_accepted_CB.setChecked(
        #         self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputAccepted"])
        #     self.ef_rejected_CB.setChecked(
        #         self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputRejected"])
        #     self.ef_total_CB.setChecked(
        #         self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"]["OutputTotal"])
        #     self.ef_file_freq_SB.setValue(self.gpd["EnergyFunctionCalculator"]["OutputFileName"]["Frequency"])
        #     self.ef_file_name_LE.setText(
        #         self.gpd["EnergyFunctionCalculator"]["OutputFileName"]["OutputFileName"])
        # else:
        #     self.ef_file_name_LE.setText(self.__default_ef_file_name)
        #
        # self.ef_enable_CB.setChecked(isinstance(self.gpd["EnergyFunctionCalculator"], dict))
        # self.ef_enable_widgets(self.ef_enable_CB.isChecked())


        self.tabWidget.setCurrentIndex(0)



        # # cell_type_plugin_data = self.get_parsed_module_data(module_name="CellType")
        # # taking into account information about current cell types before displaying data to the user
        # self.contact_plugin_data.update_from_dependent_modules(
        #     dependent_module_data_dict=self.modules_to_react_to_data_dict)
        #
        # self.contact_plugin_table = TableComponent(module_data=self.contact_plugin_data.global_params)
        #
        # self.energy_GB.layout().addWidget(self.contact_plugin_table.get_ui())
        # self.spinBox.setValue(self.contact_plugin_data.neighbor_order)


    def update_fluctuation_fields(self):
        if self.show_cell_types:
            self.cell_TypeCB.show()
            self.type_ParamLE.show()
            self.label_31.hide()
            self.membraneFluctuationsLE.hide()
        else:
            self.cell_TypeCB.hide()
            self.type_ParamLE.hide()
            self.label_31.show()
            self.membraneFluctuationsLE.show()

    def debug_enable(self, _enable: bool):
        self.debug_SB.setEnabled(_enable)

    def random_enable(self, _enable: bool):
        self.random_seed_SB.setEnabled(_enable)

    def ef_enable_widgets(self, _enable: bool):
        self.ef_spin_freq_SB.setEnabled(_enable)
        self.label_10.setEnabled(_enable)
        self.ef_results_CB.setEnabled(_enable)
        self.ef_rejected_CB.setEnabled(_enable)
        self.ef_accepted_CB.setEnabled(_enable)
        self.ef_total_CB.setEnabled(_enable)
        self.label_9.setEnabled(_enable)
        self.ef_file_name_LE.setEnabled(_enable)
        self.label_8.setEnabled(_enable)
        self.ef_file_freq_SB.setEnabled(_enable)

    def connect_all_signals(self):
        self.fluctuation_FcnCB.currentTextChanged.connect(self.on_function_change)
        self.cell_TypeCB.currentTextChanged.connect(self.on_cell_type_change)
        self.type_ParamLE.textChanged.connect(self.on_cell_param_change)

        self.debug_CB.clicked.connect(self.debug_enable)
        self.random_seed_CB.clicked.connect(self.random_enable)
        self.ef_enable_CB.clicked.connect(self.ef_enable_widgets)

        self.ok_PB.clicked.connect(self.handle_accept)
        self.cancel_PB.clicked.connect(self.handle_reject)

    def on_function_change(self, fcn: str):
        if fcn == self.default_function:
            self.show_cell_types = False
        else:
            self.show_cell_types = True

        self.update_fluctuation_fields()

    def on_cell_type_change(self, text: str):
        self.type_ParamLE.setText(str(self.type_params[text]))

    def on_cell_param_change(self, text: str):
        self.type_params[self.cell_TypeCB.currentText()] = float(text)

    def handle_accept(self) -> None:
        self.user_decision = True
        pd = self.potts_data
        pd.dim = [self.xDimSB.value(), self.yDimSB.value(), self.zDimSB.value()]
        pd.membrane_fluctuations = float(self.membraneFluctuationsLE.text())
        pd.neighbor_order = self.neighborOrderSB.value()
        pd.mcs = self.mcsSB.value()
        pd.lattice_type = str(self.latticeTypeCB.currentText())
        pd.boundary_conditions["x"] = self.xbcCB.currentText()
        pd.boundary_conditions["y"] = self.ybcCB.currentText()
        pd.boundary_conditions["z"] = self.zbcCB.currentText()
        pd.offset = float(self.offset_LE.text())
        pd.k_boltzman = float(self.coefficient_LE.text())
        pd.anneal = self.anneal_SB.value()
        pd.flip_2_dim_ratio = float(self.flip_to_dim_LE.text())

        if self.debug_CB.isChecked():
            pd.debug_output_frequency = self.debug_SB.value()
        else:
            pd.debug_output_frequency = None

        if self.random_seed_CB.isChecked():
            pd.random_seed = self.random_seed_SB.value()
        else:
            pd.random_seed = None


        # self.gpd["Dim"] = [self.xDimSB.value(), self.yDimSB.value(), self.zDimSB.value()]
        # if self.fluctuation_FcnCB.currentText() == self.default_function:
        #     self.gpd["MembraneFluctuations"] = float(str(self.membraneFluctuationsLE.text()))
        # else:
        #     self.gpd['MembraneFluctuations'] = {'Parameters': self.type_params,
        #                                         'FunctionName': self.fluctuation_FcnCB.currentText()}
        # self.gpd["NeighborOrder"] = self.neighborOrderSB.value()
        # self.gpd["MCS"] = self.mcsSB.value()
        # self.gpd["LatticeType"] = str(self.latticeTypeCB.currentText())
        # self.gpd["BoundaryConditions"]['x'] = self.xbcCB.currentText()
        # self.gpd["BoundaryConditions"]['y'] = self.ybcCB.currentText()
        # self.gpd["BoundaryConditions"]['z'] = self.zbcCB.currentText()
        #
        # self.gpd["Offset"] = self.offset_SB.value()
        # self.gpd['KBoltzman'] = self.coefficient_SB.value()
        # self.gpd['Anneal'] = self.anneal_SB.value()
        # self.gpd['Flip2DimRatio'] = self.flip_to_dim_SB.value()
        #
        # if self.debug_CB.isChecked():
        #     self.gpd['DebugOutputFrequency'] = self.debug_SB.value()
        # else:
        #     self.gpd['DebugOutputFrequency'] = None
        #
        # if self.random_seed_CB.isChecked():
        #     self.gpd["RandomSeed"] = self.random_seed_SB.value()
        # else:
        #     self.gpd["RandomSeed"] = None
        #
        # if self.ef_enable_CB.isChecked():
        #     if self.gpd["EnergyFunctionCalculator"] is None:
        #         self.gpd["EnergyFunctionCalculator"] = {}
        #         self.gpd["EnergyFunctionCalculator"]["OutputFileName"] = {}
        #         self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"] = {}
        #
        #     self.gpd["EnergyFunctionCalculator"]["Type"] = 'Statistics'
        #
        #     ef_file_name = self.ef_file_name_LE.text()
        #     if ef_file_name.__len__() == 0:
        #         ef_file_name = self.__default_ef_file_name
        #     if os.path.splitext(ef_file_name)[1].__len__() == 0:
        #         ef_file_name += '.txt'
        #     ef_file_name = os.path.split(os.path.abspath(ef_file_name))[-1]
        #     self.gpd["EnergyFunctionCalculator"]["OutputFileName"] = {'OutputFileName': ef_file_name,
        #                                                               'Frequency': self.ef_file_freq_SB.value()}
        #
        #     self.gpd["EnergyFunctionCalculator"]["OutputCoreFileNameSpinFlips"] = {
        #         'OutputCoreFileNameSpinFlips': 'statDataSingleFlip',
        #         'Frequency': self.ef_spin_freq_SB.value(),
        #         'GatherResults': self.ef_results_CB.isChecked(),
        #         'OutputAccepted': self.ef_accepted_CB.isChecked(),
        #         'OutputRejected': self.ef_rejected_CB.isChecked(),
        #         'OutputTotal': self.ef_total_CB.isChecked()
        #     }
        # else:
        #     self.gpd["EnergyFunctionCalculator"] = None

        self.close()

    def handle_reject(self) -> None:
        self.user_decision = False
        self.close()

