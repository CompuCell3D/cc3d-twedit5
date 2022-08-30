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



if __name__ == '__main__':
    app = QApplication(sys.argv)  # needs to be defined first
    module_data = ModuleData(
        df=pd.DataFrame(data=[['Condensing', 25.0, 2.0],
                              ['NonCondensing', 26.0, 2.1]],
                        columns=['CellType', 'TargetVolume', 'LambdaVolume']),
        types=[str, float, float],
        editable_columns=['TargetVolume', 'LambdaVolume']

    )

    table_component = TableComponent(module_data=module_data)

    window = QWidget()
    layout = QHBoxLayout()

    group_box = QGroupBox("Group Box")
    group_box_layout = QVBoxLayout()
    group_box_layout.addWidget(table_component.get_ui())
    group_box.setLayout(group_box_layout)

    layout.addWidget(group_box)
    window.setLayout(layout)


    # self.group_box_layout = QVBoxLayout(self.by_type_GB)
    # self.group_box_layout.addWidget(self.volume_params_table.get_ui())


    # layout.addWidget(table_component.get_ui())
    # window.setLayout(layout)


    # table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # window.setWindowTitle("Spin Box Delegate")
    # tableView.setWindowTitle("Spin Box Delegate")
    window.resize(QSize(800, 300))
    window.show()
    # tableView.show()
    sys.exit(app.exec_())


# if __name__ == '__main__':
#     app = QApplication(sys.argv)  # needs to be defined first
#     module_data = ModuleData(
#         df=pd.DataFrame(data=[['Condensing', 25.0, 2.0],
#                               ['NonCondensing', 26.0, 2.1]],
#                         columns=['CellType', 'TargetVolume', 'LambdaVolume']),
#         types=[str, float, float]
#
#     )
#
#     window = QWidget()
#     layout = QHBoxLayout()
#
#     # model = QStandardItemModel(4, 2)
#
#     # cdf = get_data_frame()
#     model = TableModel(module_data=module_data)
#     table_view = TableView()
#     table_view.setModel(model)
#
#     # model.update(cdf)
#     # model.update_type_conv_fcn(get_types())
#     #
#     # tableView = QTableView()
#     # tableView.setModel(model)
#     #
#     delegate = EditorDelegate()
#     table_view.setItemDelegate(delegate)
#     #
#     # for row in range(4):
#     #     for column in range(2):
#     #         index = model.index(row, column, QModelIndex())
#     #         model.setData(index, (row + 1) * (column + 1))
#     #
#     #
#     layout.addWidget(table_view)
#     window.setLayout(layout)
#     table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#     # window.setWindowTitle("Spin Box Delegate")
#     # tableView.setWindowTitle("Spin Box Delegate")
#     window.resize(QSize(800, 300))
#     window.show()
#     # tableView.show()
#     sys.exit(app.exec_())
