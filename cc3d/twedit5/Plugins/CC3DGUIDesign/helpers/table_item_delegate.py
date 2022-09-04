from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class EditorDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if not index.isValid():
            return

        model = index.model()
        df = model.df
        col_name = df.columns[index.column()]

        if col_name in model.editable_columns():
            if model.is_boolean(index.column()):
                return QCheckBox(parent)
            editor = QLineEdit(parent)

            # we set initial editor data in setEditorData method
            return editor
        else:
            return None

        # column_name = self.get_col_name_from_index(index)
        # print('column_name=',column_name)
        # if column_name == 'Value':
        #     editor = QLineEdit(parent)
        #     # editor.setText()
        #     return editor
        # else:
        #     return None
        # editor = QSpinBox(parent)
        # editor.setFrame(False)
        # editor.setMinimum(0)
        # editor.setMaximum(100)
        #
        # return editor

    def get_col_name_from_index(self, index):
        """
        returns column name from index
        :param index:
        :return:{str or NNne}
        """
        if not index.isValid():
            return

        model = index.model()
        df = model.df

        column_name = df.columns[index.column()]

        return column_name

    def setEditorData(self, editor, index):

        col_name = self.get_col_name_from_index(index)
        if not col_name:
            return
        if not index.isValid():
            return

        model = index.model()

        if col_name in model.editable_columns():
            value = index.model().data(index, Qt.DisplayRole)
            editor.setText(str(value))
        else:
            return

        # if column_name == 'Value':
        #     value = index.model().data(index, Qt.DisplayRole)
        #     print('i,j=',index.column(), index.row())
        #     print('val=',value)
        #     # editor.setText(str(value.toInt()))
        #     editor.setText(str(value))
        # else:
        #     return
        #     # editor.setValue(value.Int)
