from PyQt5 import QtCore, QtGui, QtWidgets


class Table(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwds):
        try:
            column_names = kwds['column_names']
            del kwds['column_names']
        except KeyError:
            column_names = None

        super(Table, self).__init__(*args, **kwds)
        if column_names is not None:
            self.setColumnCount(len(column_names))

            for i, col_name in enumerate(column_names):
                item = QtWidgets.QTableWidgetItem(col_name)
                self.setHorizontalHeaderItem(i, item)


