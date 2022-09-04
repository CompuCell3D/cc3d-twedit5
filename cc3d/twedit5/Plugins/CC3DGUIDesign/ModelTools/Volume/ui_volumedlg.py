# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'volumedlg.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VolumePluginGUI(object):
    def setupUi(self, VolumePluginGUI):
        VolumePluginGUI.setObjectName("VolumePluginGUI")
        VolumePluginGUI.resize(487, 292)
        self.verticalLayout = QtWidgets.QVBoxLayout(VolumePluginGUI)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.global_RB = QtWidgets.QRadioButton(VolumePluginGUI)
        self.global_RB.setChecked(True)
        self.global_RB.setObjectName("global_RB")
        self.horizontalLayout_2.addWidget(self.global_RB)
        self.by_type_RB = QtWidgets.QRadioButton(VolumePluginGUI)
        self.by_type_RB.setObjectName("by_type_RB")
        self.horizontalLayout_2.addWidget(self.by_type_RB)
        self.by_cell_RB = QtWidgets.QRadioButton(VolumePluginGUI)
        self.by_cell_RB.setObjectName("by_cell_RB")
        self.horizontalLayout_2.addWidget(self.by_cell_RB)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.by_type_GB = QtWidgets.QGroupBox(VolumePluginGUI)
        self.by_type_GB.setObjectName("by_type_GB")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.by_type_GB)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout.addWidget(self.by_type_GB)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.add_PB = QtWidgets.QPushButton(VolumePluginGUI)
        self.add_PB.setObjectName("add_PB")
        self.horizontalLayout.addWidget(self.add_PB)
        self.cancel_PB = QtWidgets.QPushButton(VolumePluginGUI)
        self.cancel_PB.setObjectName("cancel_PB")
        self.horizontalLayout.addWidget(self.cancel_PB)
        self.ok_PB = QtWidgets.QPushButton(VolumePluginGUI)
        self.ok_PB.setObjectName("ok_PB")
        self.horizontalLayout.addWidget(self.ok_PB)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(VolumePluginGUI)
        self.ok_PB.clicked.connect(VolumePluginGUI.accept)
        self.cancel_PB.clicked.connect(VolumePluginGUI.reject)
        QtCore.QMetaObject.connectSlotsByName(VolumePluginGUI)

    def retranslateUi(self, VolumePluginGUI):
        _translate = QtCore.QCoreApplication.translate
        VolumePluginGUI.setWindowTitle(_translate("VolumePluginGUI", "Volume"))
        self.global_RB.setText(_translate("VolumePluginGUI", "Global"))
        self.by_type_RB.setText(_translate("VolumePluginGUI", "By Cell Type"))
        self.by_cell_RB.setText(_translate("VolumePluginGUI", "By Cell"))
        self.by_type_GB.setTitle(_translate("VolumePluginGUI", "Global"))
        self.add_PB.setText(_translate("VolumePluginGUI", "Add"))
        self.cancel_PB.setText(_translate("VolumePluginGUI", "Cancel"))
        self.ok_PB.setText(_translate("VolumePluginGUI", "OK"))

