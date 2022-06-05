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
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(DevZoneDlg)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DevZoneDlg)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(DevZoneDlg)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cc3d_git_dir_LE = QtWidgets.QLineEdit(DevZoneDlg)
        self.cc3d_git_dir_LE.setObjectName("cc3d_git_dir_LE")
        self.verticalLayout_2.addWidget(self.cc3d_git_dir_LE)
        self.build_dir_LE = QtWidgets.QLineEdit(DevZoneDlg)
        self.build_dir_LE.setObjectName("build_dir_LE")
        self.verticalLayout_2.addWidget(self.build_dir_LE)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cc3d_git_browse_PB = QtWidgets.QPushButton(DevZoneDlg)
        self.cc3d_git_browse_PB.setObjectName("cc3d_git_browse_PB")
        self.verticalLayout_3.addWidget(self.cc3d_git_browse_PB)
        self.build_dir_browse_PB = QtWidgets.QPushButton(DevZoneDlg)
        self.build_dir_browse_PB.setObjectName("build_dir_browse_PB")
        self.verticalLayout_3.addWidget(self.build_dir_browse_PB)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.dev_zone_status_TE = QtWidgets.QTextEdit(DevZoneDlg)
        self.dev_zone_status_TE.setReadOnly(True)
        self.dev_zone_status_TE.setObjectName("dev_zone_status_TE")
        self.verticalLayout_4.addWidget(self.dev_zone_status_TE)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.cancelPB = QtWidgets.QPushButton(DevZoneDlg)
        self.cancelPB.setObjectName("cancelPB")
        self.horizontalLayout_3.addWidget(self.cancelPB)
        self.configurePB = QtWidgets.QPushButton(DevZoneDlg)
        self.configurePB.setObjectName("configurePB")
        self.horizontalLayout_3.addWidget(self.configurePB)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.retranslateUi(DevZoneDlg)
        self.cancelPB.clicked.connect(DevZoneDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(DevZoneDlg)

    def retranslateUi(self, DevZoneDlg):
        _translate = QtCore.QCoreApplication.translate
        DevZoneDlg.setWindowTitle(_translate("DevZoneDlg", "DeveloperZone Configuration"))
        self.label.setText(_translate("DevZoneDlg", "CC3D GIT Repository Dir"))
        self.label_2.setText(_translate("DevZoneDlg", "Build Dir. (compiler work directory)"))
        self.cc3d_git_dir_LE.setToolTip(_translate("DevZoneDlg", "<html><head/><body><p>Specify path where you have cloned CC3D git repository (top level)</p></body></html>"))
        self.build_dir_LE.setToolTip(_translate("DevZoneDlg", "<html><head/><body><p>Specify directory where intermediate compiler files for DeveloperZone shole be written to</p></body></html>"))
        self.cc3d_git_browse_PB.setText(_translate("DevZoneDlg", "Browse..."))
        self.build_dir_browse_PB.setText(_translate("DevZoneDlg", "Browse..."))
        self.cancelPB.setText(_translate("DevZoneDlg", "Cancel"))
        self.configurePB.setText(_translate("DevZoneDlg", "Configure"))

