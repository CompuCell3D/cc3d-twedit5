# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dev_zone.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DevZoneDlg(object):
    def setupUi(self, DevZoneDlg):
        DevZoneDlg.setObjectName("DevZoneDlg")
        DevZoneDlg.resize(738, 325)
        self.verticalLayout = QtWidgets.QVBoxLayout(DevZoneDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(DevZoneDlg)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cc3d_git_dir_LE = QtWidgets.QLineEdit(DevZoneDlg)
        self.cc3d_git_dir_LE.setObjectName("cc3d_git_dir_LE")
        self.horizontalLayout.addWidget(self.cc3d_git_dir_LE)
        self.cc3d_git_browse_PB = QtWidgets.QPushButton(DevZoneDlg)
        self.cc3d_git_browse_PB.setObjectName("cc3d_git_browse_PB")
        self.horizontalLayout.addWidget(self.cc3d_git_browse_PB)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(DevZoneDlg)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.build_dir_LE = QtWidgets.QLineEdit(DevZoneDlg)
        self.build_dir_LE.setObjectName("build_dir_LE")
        self.horizontalLayout_2.addWidget(self.build_dir_LE)
        self.build_dir_browse_PB = QtWidgets.QPushButton(DevZoneDlg)
        self.build_dir_browse_PB.setObjectName("build_dir_browse_PB")
        self.horizontalLayout_2.addWidget(self.build_dir_browse_PB)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.dev_zone_status_TE = QtWidgets.QTextEdit(DevZoneDlg)
        self.dev_zone_status_TE.setReadOnly(True)
        self.dev_zone_status_TE.setObjectName("dev_zone_status_TE")
        self.verticalLayout.addWidget(self.dev_zone_status_TE)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushButton_2 = QtWidgets.QPushButton(DevZoneDlg)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(DevZoneDlg)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(DevZoneDlg)
        QtCore.QMetaObject.connectSlotsByName(DevZoneDlg)

    def retranslateUi(self, DevZoneDlg):
        _translate = QtCore.QCoreApplication.translate
        DevZoneDlg.setWindowTitle(_translate("DevZoneDlg", "DeveloperZone Configuration"))
        self.label.setText(_translate("DevZoneDlg", "CC3D GIT Repository Dir"))
        self.cc3d_git_dir_LE.setToolTip(_translate("DevZoneDlg", "<html><head/><body><p>Specify path where you have cloned CC3D git repository (top level)</p></body></html>"))
        self.cc3d_git_browse_PB.setText(_translate("DevZoneDlg", "Browse..."))
        self.label_2.setText(_translate("DevZoneDlg", "Build Dir. (compiler work directory)"))
        self.build_dir_LE.setToolTip(_translate("DevZoneDlg", "<html><head/><body><p>Specify directory where intermediate compiler files for DeveloperZone shole be written to</p></body></html>"))
        self.build_dir_browse_PB.setText(_translate("DevZoneDlg", "Browse..."))
        self.pushButton_2.setText(_translate("DevZoneDlg", "Cancel"))
        self.pushButton.setText(_translate("DevZoneDlg", "Configure"))

