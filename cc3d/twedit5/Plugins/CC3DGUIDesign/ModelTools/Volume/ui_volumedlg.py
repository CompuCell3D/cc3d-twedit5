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
        self.globalGB = QtWidgets.QGroupBox(VolumePluginGUI)
        self.globalGB.setObjectName("globalGB")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.globalGB)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.globalLayout = QtWidgets.QHBoxLayout()
        self.globalLayout.setObjectName("globalLayout")
        self.label = QtWidgets.QLabel(self.globalGB)
        self.label.setObjectName("label")
        self.globalLayout.addWidget(self.label)
        self.target_vol_LE = QtWidgets.QLineEdit(self.globalGB)
        self.target_vol_LE.setObjectName("target_vol_LE")
        self.globalLayout.addWidget(self.target_vol_LE)
        self.label_2 = QtWidgets.QLabel(self.globalGB)
        self.label_2.setObjectName("label_2")
        self.globalLayout.addWidget(self.label_2)
        self.lambda_vol_LE = QtWidgets.QLineEdit(self.globalGB)
        self.lambda_vol_LE.setObjectName("lambda_vol_LE")
        self.globalLayout.addWidget(self.lambda_vol_LE)
        self.horizontalLayout_3.addLayout(self.globalLayout)
        self.verticalLayout.addWidget(self.globalGB)
        self.bytypeGB = QtWidgets.QGroupBox(VolumePluginGUI)
        self.bytypeGB.setObjectName("bytypeGB")
        self.verticalLayout.addWidget(self.bytypeGB)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelPB = QtWidgets.QPushButton(VolumePluginGUI)
        self.cancelPB.setObjectName("cancelPB")
        self.horizontalLayout.addWidget(self.cancelPB)
        self.okPB = QtWidgets.QPushButton(VolumePluginGUI)
        self.okPB.setObjectName("okPB")
        self.horizontalLayout.addWidget(self.okPB)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(VolumePluginGUI)
        self.global_RB.toggled['bool'].connect(self.globalGB.setVisible)
        self.by_type_RB.toggled['bool'].connect(self.bytypeGB.setVisible)
        self.okPB.clicked.connect(VolumePluginGUI.accept)
        self.cancelPB.clicked.connect(VolumePluginGUI.reject)
        QtCore.QMetaObject.connectSlotsByName(VolumePluginGUI)

    def retranslateUi(self, VolumePluginGUI):
        _translate = QtCore.QCoreApplication.translate
        VolumePluginGUI.setWindowTitle(_translate("VolumePluginGUI", "Volume"))
        self.global_RB.setText(_translate("VolumePluginGUI", "Global"))
        self.by_type_RB.setText(_translate("VolumePluginGUI", "By Cell Type"))
        self.by_cell_RB.setText(_translate("VolumePluginGUI", "By Cell"))
        self.globalGB.setTitle(_translate("VolumePluginGUI", "Global"))
        self.label.setText(_translate("VolumePluginGUI", "<html><head/><body><p><span style=\" font-weight:600;\">TargetVolume</span></p></body></html>"))
        self.label_2.setText(_translate("VolumePluginGUI", "<html><head/><body><p><span style=\" font-weight:600;\">LambdaVolume</span></p></body></html>"))
        self.bytypeGB.setTitle(_translate("VolumePluginGUI", "By Cell Type"))
        self.cancelPB.setText(_translate("VolumePluginGUI", "Cancel"))
        self.okPB.setText(_translate("VolumePluginGUI", "OK"))

