import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
import pandas as pd
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.module_data import ModuleData, TableType


class CC3DModulesModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super(CC3DModulesModel, self).__init__()
        data = [
            ['Potts', ''],  # marking of Potts section
            ['Potts', 'Potts'],
            ['Plugins', ''],  # marking of plugin section
            ['Plugin', 'CellType'],
            ['Plugin', 'Contact'],
            ['Plugin', 'Volume'],
            ['Steppables', ''],
            ['Steppable', 'DiffusionSolverFE'],
            ['Steppable', 'DiffusionSolverFE'],
            ['Steppable', 'BlobInitializer'],

        ]
        self.df = pd.DataFrame(data, columns=['ModuleType', 'ModuleName'])

    def set_dirty(self, flag):
        self.dirty_flag = flag

    def is_dirty(self):
        return self.dirty_flag

    def update(self, item_data):

        self.item_data = item_data

    def is_section_header(self, index):
        if not index.isValid():
            return False

        i = index.row()
        row = self.df.loc[i]
        if row['ModuleName'] == '':
            return True
        return False

    def headerData(self, p_int, orientation, role=None):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if p_int == 0:
                return self.df.columns[p_int]
            else:
                return QVariant()

        return QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.df.shape[0]

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 1

    def get_item(self, index):

        if not index.isValid():
            return

        i = index.row()
        j = index.column()
        if self.table_type & TableType.ROW_LIST:
            col_name = self.df.columns[j]

            return self.df[col_name].values[i]
        else:
            return self.arr[i, j]

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if not index.isValid():
            return

        i = index.row()
        row = self.df.loc[i]

        if role == QtCore.Qt.DisplayRole:
            if row['ModuleName'] == '':
                # padding of 10 spaces for better esthetics
                return ' ' * 10 + row['ModuleType']
            return row['ModuleName']
        elif role == QtCore.Qt.FontRole:
            if row['ModuleName'] == '':

                font = QtGui.QFont()
                font.setBold(True)
                return font
        elif role == Qt.BackgroundRole:
            if row['ModuleName'] == '':
                # return QtGui.QColor("darkGray")
                return QtGui.QColor(30, 27, 24)
        elif role == Qt.ForegroundRole:
            if row['ModuleName'] == '':
                # return QtGui.QColor("darkGray")
                return QtGui.QColor(215, 214, 213)

            # if self.table_type & TableType.ROW_LIST:
            #     batch = (index.row()) % 2
            #     if batch == 0:
            #         return QtGui.QColor("white")
            #
            #     else:
            #         return QtGui.QColor("gray")

        # elif role == QtCore.Qt.TextAlignmentRole:
        #     if row['ModuleName'] == '':
        #         return QtCore.Qt.AlignCenter

        # elif role == Qt.BackgroundRole:
        #     if self.table_type & TableType.ROW_LIST:
        #         batch = (index.row()) % 2
        #         if batch == 0:
        #             return QtGui.QColor("white")
        #
        #         else:
        #             return QtGui.QColor("gray")


        else:
            return QtCore.QVariant()

        return QtCore.QVariant()

    def setData(self, index, value, role=None):
        """
        This needs to be reimplemented if  allowing editing
        :param index:
        :param Any:
        :param role:
        :return:
        """
        return
        if role != QtCore.Qt.EditRole:
            return False

        if not index.isValid():
            return False

        i = index.row()
        j = index.column()
        if self.contains_matrix():
            try:
                value = self.arr_element_type(value)
            except ValueError:
                return False
            self.arr[i, j] = value
            if self.table_type & TableType.IS_SYMMETRIC:
                self.arr[j, i] = value
            self.dirty_flag = True
        else:

            col_name = self.df.columns[j]

            col_type = self.df_types[j]
            try:
                value = col_type(value)
            except ValueError:
                return False

            self.df[col_name].values[i] = value
            # item = self.item_data[index.row()]
            # item.val = value
            # item.dirty_flag = True
            self.dirty_flag = True

        return True

    def flags(self, index):

        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        existing_flags = super(CC3DModulesModel, self).flags(index)

        existing_flags |= QtCore.Qt.ItemIsEditable

        # if self.df is not None and self.df_types is not None:
        #     col = index.column()
        #     if self.df_types[col] == bool:
        #         existing_flags |= QtCore.Qt.ItemIsUserCheckable

        return existing_flags

    # def insertRows(self, position, rows, QModelIndex, parent):
    #     if self.inserted_df is None:
    #         return
    #     self.beginInsertRows(QModelIndex, position, position+rows-1)
    #     default_row = ['']*len(self.df.columns)  # or _headers if you have that defined.
    #     insert_df = self.df[:1]
    #     for i in range(rows):
    #         self.df = pd.concat([self.df, insert_df])
    #         # self._data.insert(position, default_row)
    #     self.endInsertRows()
    #
    #
    #     self.layoutChanged.emit()
    #
    #
    #     return True

    def append_rows(self, append_df: pd.DataFrame):
        """
        Appending row to model. Two thins are important
        1. calling self.beginInsertRows and  self.endInsertRows()
        2. emitting layoutChanged signal to tell view that data layout has changed
        for more information see https://www.pythonguis.com/faq/remove-and-insertrow-for-martin-fitzpatricks-example/
        """
        rows = append_df.shape[0]
        index = self.index(self.rowCount() - 1, 0, QtCore.QModelIndex())
        position = index.row()
        self.beginInsertRows(index, position, position + rows - 1)
        self.df = pd.concat([self.df, append_df], ignore_index=True)
        self.endInsertRows()

        self.layoutChanged.emit()

    def remove_row(self, index: QtCore.QModelIndex, num_rows: int = 1):
        """
        Removing row from model. Two thins are important
        1. calling self.beginRemoveRows and  self.endRemoveRows
        2. emitting layoutChanged signal to tell view that data layout has changed
        for more information see https://www.pythonguis.com/faq/remove-and-insertrow-for-martin-fitzpatricks-example/
        """

        if not index.isValid():
            return
        i = index.row()
        self.beginRemoveRows(index, i, i + num_rows - 1)
        mask = np.ones(self.df.shape[0], dtype=bool)
        mask[i] = False
        self.df = self.df[mask]
        self.endRemoveRows()
        self.layoutChanged.emit()

        # rows = append_df.shape[0]
        # index = self.index(self.rowCount() - 1, 0, QtCore.QModelIndex())
        # position = index.row()
        # self.beginInsertRows(index, position, position + rows - 1)
        # self.df = pd.concat([self.df, append_df], ignore_index=True)
        # self.endInsertRows()
        #
        # self.layoutChanged.emit()
        #
