from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
import pandas as pd
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.module_data import ModuleData


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, module_data: ModuleData=None):
        super(TableModel, self).__init__()
        self.df = None
        self.df_types = None
        self._editable_columns = None

        # self.inserted_df = None

        if module_data is not None:
            self.df = module_data.df
            self.df_types = module_data.types
            self._editable_columns = module_data.editable_columns

        # self.df = pd.DataFrame(data=[['Condensing', 25.0, 2.0],
        #                              ['NonCondensing', 26.0, 2.1]],
        #                        columns=['CellType', 'TargetVolume', 'LambdaVolume'])
        # self.df_types = [str, float, float]
        # self.df.append(['Condensing', 25.0, 2.0])
        # self.df.append(['NonCondensing', 26.0, 2.1])
        print(self.df)
        # self.item_data = None
        # self.dirty_flag = False
        #
        # self.header_data = [
        #     'Value',
        #     # 'Type'
        # ]
        # self.item_data_attr_name = {
        #     0: 'val',
        #     # 1: 'item_type'
        # }

    def is_boolean(self, col):
        try:
            return self.df_types[col] == bool
        except IndexError:
            return False

    def editable_columns(self):
        return self._editable_columns

    def set_dirty(self, flag):
        self.dirty_flag = flag

    def is_dirty(self):
        return self.dirty_flag

    def update(self, item_data):

        self.item_data = item_data

    def headerData(self, p_int, orientation, role=None):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.df.columns[p_int]
            except IndexError:
                return QVariant()

        # if orientation == Qt.Vertical and role == Qt.DisplayRole:
        #     try:
        #         return self.item_data[p_int].name
        #     except IndexError:
        #         return QVariant()

        return QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.df.shape[0]

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.df.shape[1]

    def get_item(self, index):
        if not index.isValid():
            return

        i = index.row()
        j = index.column()
        col_name = self.df.columns[j]

        return self.df[col_name].values[i]

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.CheckStateRole:
            if self.df is not None and self.df_types is not None:
                i = index.row()
                j = index.column()

                if self.df_types[j] == bool:
                    col_name = self.df.columns[j]
                    if self.df[col_name].values[i]:
                        return QtCore.Qt.Checked
                    else:
                        return QtCore.Qt.Unchecked
            return QVariant()

        elif role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            col_name = self.df.columns[j]
            if self.df_types[j] != bool:

                return str(self.df[col_name].values[i])
            else:
                return QVariant()
            # item = self.item_data[i]
            # item_data_to_display = getattr(item, self.item_data_attr_name[j])
            # return '{}'.format(item_data_to_display)

        elif role == Qt.BackgroundRole:
            batch = (index.row()) % 2
            if batch == 0:
                return QtGui.QColor('white')

            else:
                return QtGui.QColor('gray')

        # elif role == Qt.ToolTipRole:
        #     i = index.row()
        #     j = index.column()
        #     item = self.item_data[i]
        #     return str(item.item_type)

        else:

            return QtCore.QVariant()

    def setData(self, index, value, role=None):
        """
        This needs to be reimplemented if  allowing editing
        :param index:
        :param Any:
        :param role:
        :return:
        """

        if role != QtCore.Qt.EditRole:
            return False

        if not index.isValid():
            return False

        i = index.row()
        j = index.column()
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
        existing_flags = super(TableModel, self).flags(index)

        existing_flags |= QtCore.Qt.ItemIsEditable
        if self.df is not None and self.df_types is not None:
            col = index.column()
            if self.df_types[col] == bool:
                existing_flags |= QtCore.Qt.ItemIsUserCheckable

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


