from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.TableModel import TableModel
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.TableView import TableView
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.table_item_delegate import EditorDelegate
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.module_data import ModuleData


class TableComponent:
    def __init__(self, module_data: ModuleData):
        self.module_data = module_data
        self.model = TableModel(module_data=module_data)
        self.table_view = TableView()
        self.table_view.setModel(self.model)
        if not self.model.contains_matrix():
            self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.delegate = EditorDelegate()
        self.table_view.setItemDelegate(self.delegate)

    def get_ui(self):
        return self.table_view
