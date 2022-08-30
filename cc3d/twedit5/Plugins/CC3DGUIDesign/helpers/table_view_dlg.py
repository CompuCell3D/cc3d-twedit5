from copy import deepcopy
from itertools import product
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.ui_tableview import Ui_TableView


class TableViewGUI(Ui_TableView):
    def __init__(self, parent=None):
        super(TableViewGUI, self).__init__(parent)
        self.setupUi(self)

        # self.showNormal()

