import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from cc3d.twedit5.Plugins.CC3DGUIDesign.helpers.cc3d_modules_model import CC3DModulesModel


class ViewWidget(QtWidgets.QWidget):
    def __init__(self, x, index, use_buttons=True, parent=None):
        super(ViewWidget, self).__init__(parent)
        self.p_index = QtCore.QPersistentModelIndex(index)
        self.content_button = QtWidgets.QWidget(self)
        lay = QtWidgets.QHBoxLayout(self.content_button)
        lay.setContentsMargins(0, 0, 0, 0)
        if use_buttons:
            self.edit_PB = QtWidgets.QPushButton("edit")
            self.edit_PB.setStyleSheet("color: white; background-color: blue")
            self.edit_PB.clicked.connect(self.edit_clicked)
            # self.delete_btn = QtWidgets.QPushButton("delete")
            # self.delete_btn.clicked.connect(self.delete_clicked)
            lay.addWidget(self.edit_PB)
            # lay.addWidget(self.delete_btn)
            self.content_button.move(x, 0)

    # # @QtCore.Slot()
    # def delete_clicked(self):
    #     model = self.p_index.model()
    #     model.removeRow(self.p_index.row())

    # @QtCore.Slot()
    def edit_clicked(self):
        text = self.p_index.data()
        full_path = self.p_index.data(QtCore.Qt.UserRole + 1)
        print(text, full_path)


class ButtonsDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        self.parent().openPersistentEditor(index)
        super(ButtonsDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        model = index.model()
        section_header_flag = model.is_section_header(index=index)
        return ViewWidget(150, index, use_buttons=not section_header_flag, parent=parent)


class ModuleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ModuleWidget, self).__init__(parent)
        layout = QtWidgets.QGridLayout(self)

        self.model = QtGui.QStandardItemModel(self)
        self.model = CC3DModulesModel()
        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.clicked.connect(self.onClick)
        self.tableView.verticalHeader().hide()
        # self.appendRowItems(dirPath)

        delegate = ButtonsDelegate(self.tableView)
        self.tableView.setItemDelegate(delegate)

        layout.addWidget(self.tableView)
        self.resize(self.minimumSizeHint())

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return QtCore.QSize(300, 500)

    def onClick(self, ix):
        it = self.model.itemFromIndex(ix)
        print(it.data())


class Example(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)

        self.module_widget =  ModuleWidget(parent=parent)

        self.setCentralWidget(self.module_widget)
        self.resize(300, 500)

# class Example(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(Example, self).__init__(parent)
#
#
#         self.setCentralWidget(QtWidgets.QWidget())
#         layout = QtWidgets.QGridLayout(self.centralWidget())
#
#         self.model = QtGui.QStandardItemModel(self)
#         self.model = CC3DModulesModel()
#         self.tableView = QtWidgets.QTableView()
#         self.tableView.setModel(self.model)
#         self.tableView.horizontalHeader().setStretchLastSection(True)
#         self.tableView.clicked.connect(self.onClick)
#         self.tableView.verticalHeader().hide()
#         # self.appendRowItems(dirPath)
#
#         delegate = ButtonsDelegate(self.tableView)
#         self.tableView.setItemDelegate(delegate)
#
#         layout.addWidget(self.tableView)
#         self.resize(300, 500)
#
#     def appendRowItems(self, dir_path):
#         for root, dirs, files in os.walk(dir_path):
#             if root == dir_path:
#                 for file in files:
#                     item = QtGui.QStandardItem(file)
#                     item.setData(os.path.join(root, file))
#                     self.model.appendRow(item)
#
#     # @QtCore.Slot(QtCore.QModelIndex)
#     def onClick(self, ix):
#         it = self.model.itemFromIndex(ix)
#         print(it.data())
#

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    eg = Example()
    eg.show()
    sys.exit(app.exec_())
