from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore
# from cc3d import CompuCellSetup


class TableView(QtWidgets.QTableView):
    def __init__(self, *args, **kwargs):

        QtWidgets.QTableView.__init__(self, *args, **kwargs)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if bool(modifiers == QtCore.Qt.ControlModifier):
                index = self.indexAt(event.pos())
                col_name = self.get_col_name(index)
                # if col_name == 'Value':
                #     self.edit(index)
                if col_name in self.model().editable_columns():
                    self.edit(index)
            else:
                super(TableView, self).mousePressEvent(event)
        else:
            super(TableView, self).mousePressEvent(event)
            # QTableView.mousePressEvent(event)

    def get_col_name(self, index):

        model = index.model()

        if not model:
            return None

        # return model.header_data[index.column()]
        return model.df.columns[index.column()]

    def sizeHint(self):
        """
        Implements basic size hint
        :return: {Qsize}
        """
        row_count = min(self.model().rowCount() + 1, 20)
        row_size = self.rowHeight(0)

        sugested_vsize = row_count * row_size
        return QSize(600, sugested_vsize)
