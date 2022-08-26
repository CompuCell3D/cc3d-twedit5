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
        self.globalGB = QtWidgets.QGroupBox(VolumePluginGUI)
        self.globalGB.setGeometry(QtCore.QRect(0, 60, 501, 72))
        self.globalGB.setObjectName("globalGB")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.globalGB)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.globalLayout = QtWidgets.QHBoxLayout()
        self.globalLayout.setObjectName("globalLayout")
        self.label = QtWidgets.QLabel(self.globalGB)
        self.label.setObjectName("label")
        self.globalLayout.addWidget(self.label)
        self.targetVolLE = QtWidgets.QLineEdit(self.globalGB)
        self.targetVolLE.setObjectName("targetVolLE")
        self.globalLayout.addWidget(self.targetVolLE)
        self.label_2 = QtWidgets.QLabel(self.globalGB)
        self.label_2.setObjectName("label_2")
        self.globalLayout.addWidget(self.label_2)
        self.lambdaVolLE = QtWidgets.QLineEdit(self.globalGB)
        self.lambdaVolLE.setObjectName("lambdaVolLE")
        self.globalLayout.addWidget(self.lambdaVolLE)
        self.horizontalLayout_3.addLayout(self.globalLayout)
        self.bytypeGB = QtWidgets.QGroupBox(VolumePluginGUI)
        self.bytypeGB.setGeometry(QtCore.QRect(10, 140, 461, 80))
        self.bytypeGB.setObjectName("bytypeGB")
        self.widget = QtWidgets.QWidget(VolumePluginGUI)
        self.widget.setGeometry(QtCore.QRect(300, 240, 173, 32))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelPB = QtWidgets.QPushButton(self.widget)
        self.cancelPB.setObjectName("cancelPB")
        self.horizontalLayout.addWidget(self.cancelPB)
        self.okPB = QtWidgets.QPushButton(self.widget)
        self.okPB.setObjectName("okPB")
        self.horizontalLayout.addWidget(self.okPB)
        self.widget1 = QtWidgets.QWidget(VolumePluginGUI)
        self.widget1.setGeometry(QtCore.QRect(20, 20, 253, 20))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.globalRB = QtWidgets.QRadioButton(self.widget1)
        self.globalRB.setChecked(True)
        self.globalRB.setObjectName("globalRB")
        self.horizontalLayout_2.addWidget(self.globalRB)
        self.bytypeRB = QtWidgets.QRadioButton(self.widget1)
        self.bytypeRB.setObjectName("bytypeRB")
        self.horizontalLayout_2.addWidget(self.bytypeRB)
        self.bycellRB = QtWidgets.QRadioButton(self.widget1)
        self.bycellRB.setObjectName("bycellRB")
        self.horizontalLayout_2.addWidget(self.bycellRB)

        self.retranslateUi(VolumePluginGUI)
        self.globalRB.toggled['bool'].connect(self.globalGB.setVisible)
        self.bytypeRB.toggled['bool'].connect(self.bytypeGB.setVisible)
        QtCore.QMetaObject.connectSlotsByName(VolumePluginGUI)

    def retranslateUi(self, VolumePluginGUI):
        _translate = QtCore.QCoreApplication.translate
        VolumePluginGUI.setWindowTitle(_translate("VolumePluginGUI", "Volume"))
        self.globalGB.setTitle(_translate("VolumePluginGUI", "Global"))
        self.label.setText(_translate("VolumePluginGUI", "<html><head/><body><p><span style=\" font-weight:600;\">TargetVolume</span></p></body></html>"))
        self.label_2.setText(_translate("VolumePluginGUI", "<html><head/><body><p><span style=\" font-weight:600;\">LambdaVolume</span></p></body></html>"))
        self.bytypeGB.setTitle(_translate("VolumePluginGUI", "By Cell Type"))
        self.cancelPB.setText(_translate("VolumePluginGUI", "Cancel"))
        self.okPB.setText(_translate("VolumePluginGUI", "OK"))
        self.globalRB.setText(_translate("VolumePluginGUI", "Global"))
        self.bytypeRB.setText(_translate("VolumePluginGUI", "By Cell Type"))
        self.bycellRB.setText(_translate("VolumePluginGUI", "By Cell"))

