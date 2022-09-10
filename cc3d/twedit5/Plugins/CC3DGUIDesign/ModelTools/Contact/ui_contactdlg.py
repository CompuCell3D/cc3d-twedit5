# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contactdlg.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ContactPluginGUI(object):
    def setupUi(self, ContactPluginGUI):
        ContactPluginGUI.setObjectName("ContactPluginGUI")
        ContactPluginGUI.setWindowModality(QtCore.Qt.NonModal)
        ContactPluginGUI.resize(496, 454)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ContactPluginGUI)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.energy_GB = QtWidgets.QGroupBox(ContactPluginGUI)
        self.energy_GB.setMinimumSize(QtCore.QSize(0, 300))
        self.energy_GB.setObjectName("energy_GB")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.energy_GB)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addWidget(self.energy_GB)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(ContactPluginGUI)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(ContactPluginGUI)
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.cancel_PB = QtWidgets.QPushButton(ContactPluginGUI)
        self.cancel_PB.setObjectName("cancel_PB")
        self.horizontalLayout_2.addWidget(self.cancel_PB)
        self.ok_PB = QtWidgets.QPushButton(ContactPluginGUI)
        self.ok_PB.setObjectName("ok_PB")
        self.horizontalLayout_2.addWidget(self.ok_PB)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ContactPluginGUI)
        QtCore.QMetaObject.connectSlotsByName(ContactPluginGUI)

    def retranslateUi(self, ContactPluginGUI):
        _translate = QtCore.QCoreApplication.translate
        ContactPluginGUI.setWindowTitle(_translate("ContactPluginGUI", "Contact Plugin: Please define adhesion coefficients"))
        self.energy_GB.setTitle(_translate("ContactPluginGUI", "Contact Energies (per unit surface)"))
        self.label.setText(_translate("ContactPluginGUI", "Neighbor Order"))
        self.cancel_PB.setText(_translate("ContactPluginGUI", "Cancel"))
        self.ok_PB.setText(_translate("ContactPluginGUI", "OK"))

