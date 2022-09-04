import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

# https://www.pythonguis.com/faq/remove-and-insertrow-for-martin-fitzpatricks-example/

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def insertRows(self, position, rows, QModelIndex, parent):
        self.beginInsertRows(QModelIndex, position, position+rows-1)
        default_row = ['']*len(self._data[0])  # or _headers if you have that defined.
        for i in range(rows):
            self._data.insert(position, default_row)
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def removeRows(self, position, rows, QModelIndex):
        self.beginRemoveRows(QModelIndex, position, position+rows-1)
        for i in range(rows):
            del(self._data[position])
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.insertaction = QtWidgets.QAction("Insert", self)
        self.insertaction.triggered.connect(self.insert_row)
        self.deletedaction = QtWidgets.QAction("Delete", self)
        self.deletedaction.triggered.connect(self.delete_row)

        toolbar = QtWidgets.QToolBar("Edit")
        toolbar.addAction(self.insertaction)
        toolbar.addAction(self.deletedaction)
        self.addToolBar(toolbar)


        self.table = QtWidgets.QTableView()

        data = [
          [1, 9, 2],
          [1, 0, -1],
          [3, 5, 2],
          [3, 3, 2],
          [5, 8, 9],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

    def insert_row(self):
        index = self.table.currentIndex()
        print(index)
        self.model.insertRows(index.row(), 1, index, None)

    def delete_row(self):
        index = self.table.currentIndex()
        self.model.removeRows(index.row(), 1, index)



app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()
