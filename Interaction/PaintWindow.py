"""
    Author: j1193
    Time: 2020/11/24 21:28
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog
from PyQt5.QtCore import Qt

from NRAProject.MainWindow import Ui_MainWindow
from analyze.main import MainWindow
from analyze.item import GraphicItem
from AttributeWindow import UiNodeAttr


class PaintWindow(Ui_MainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.ui_init()
        self.action_UseGraph.triggered.connect(self.UseGraphAction)

        self.fileName = "Untitled*"
        self.action_Open.triggered.connect(self.openFile)
        self.action_New.triggered.connect(self.newFile)
        self.action_SaveAs.triggered.connect(self.saveAs)
        self.action_Save.triggered.connect(self.saveFile)

        self.action_point.triggered.connect(self.changeState)
        self.action_lineation.triggered.connect(self.changeState)
        self.action_point_2.triggered.connect(self.changeState)
        self.action_mouse.triggered.connect(self.changeState)
        self.setTitle("网络可靠性")
    # 向导界面的跳转函数
    def UseGraphAction(self):
        if self.windowTitle() == "网络可靠性":
            QMessageBox.warning(self, '警告！', '您尚未打开文件！', QMessageBox.Ok)
        else:
            self.showToolBar()
            # self.ui_init()
            # self.button.setVisible(False)

    # 根据响应改变标志的值，根据标志在view里进行相关操作
    def changeState(self):
        if self.action_lineation.isChecked():
            self.view.is_edge = True
            self.view.is_delete = False
            self.view.is_node = False
        elif self.action_point.isChecked():
            self.view.is_node = True
            self.view.is_edge = False
            self.view.is_delete = False
        elif self.action_point_2.isChecked():
            self.view.is_delete = True
            self.view.is_node = False
            self.view.is_edge = False
        else:
            self.view.is_delete = False
            self.view.is_node = False
            self.view.is_edge = False

    def setTitle(self, title="network"):
        self.setWindowTitle(title)

    def newFile(self):
        if self.windowTitle()[-1] == '*':
            QMessageBox.warning(self, '警告！', '您尚未保存当前文件！', QMessageBox.Ok)
        else:
            self.ui_init()
            self.setTitle("Untitled*")
            self.button.setVisible(False)

    def openFile(self):
        if self.windowTitle()[-1] == '*':
            QMessageBox.warning(self, '警告！', '您尚未保存当前文件！', QMessageBox.Ok)
        else:
            if self.windowTitle() != "网络可靠性":
                self.ui_init()
                self.button.setVisible(False)
            fileName = QFileDialog.getOpenFileName(self, "选取文件", "./", "xml Files (*.xml)")[0]
            if fileName:
                self.fileName = fileName[:-4]
                self.setTitle(fileName.split('/')[-1] + '*')
                self.view.load(self.fileName)

    def saveFile(self):
        if self.windowTitle() == "网络可靠性":
            QMessageBox.warning(self, '警告！', '您尚未打开文件！', QMessageBox.Ok)
        elif self.windowTitle() == "Untitled*":
            self.saveAs()
        else:
            self.view.save(self.fileName)
            self.setTitle(self.windowTitle()[:-1])


    def saveAs(self):
        if self.windowTitle() == "网络可靠性":
            QMessageBox.warning(self, '警告！', '您尚未打开文件！', QMessageBox.Ok)
        else:
            fileName = QFileDialog.getSaveFileName(filter="xml Files (*.xml)")[0]
            if fileName:
                self.fileName = fileName[:-4]
                self.view.save(self.fileName)
                self.setTitle(self.fileName.split('/')[-1])

    def drawNode(self):
        if self.windowTitle() != "网络可靠性":
            item = GraphicItem(40, str(len(self.view.gr_scene.nodes) + 1))
            item.setPos(self.view.x, self.view.y)
            self.view.gr_scene.add_node(item)

    def drawEdge(self):
        if self.windowTitle() != "网络可靠性":
            self.view.edge_enable = ~self.view.edge_enable

    def deleteObject(self):
        self.view.is_delete = True
        # if self.windowTitle() != "网络可靠性":
        #     item = self.view.get_item_at_click(event)
        #     if isinstance(item, GraphicItem):
        #         self.gr_scene.remove_node(item)
        #     elif isinstance(item, QGraphicsPathItem):
        #         self.gr_scene.remove_edge(item)



    # def keyPressEvent(self, event):
    #     """启用快捷键"""
    #     if event.key() == Qt.Key_N:
    #         self.drawNode()
    #     if event.key() == Qt.Key_E:
    #         self.drawEdge()
    #     if event.key() == Qt.Key_D:
    #         self.deleteObject()
    #     # # 组合键 Ctrl+O
    #     if (event.modifiers() == Qt.ControlModifier) & (event.key() == Qt.Key_N):
    #         self.newFile()
    #     if (event.modifiers() == Qt.ControlModifier) & (event.key() == Qt.Key_O):
    #         self.openFile()
    #     if (event.modifiers() == Qt.ControlModifier) & (event.key() == Qt.Key_S):
    #         self.saveFile()
    #     if (event.modifiers() == Qt.ControlModifier) & (event.key() == Qt.Key_P):
    #         print('debug')

    # def mousePressEvent(self, event):
    #     """
    #     响应双击事件，尚未找到bug源头
    #     单机会调用project-paint\analyze\view.py中的GraphicView.mousePressEvent(self, event)
    #     双击会先调用上面的函数，再调用此函数。
    #     只能修改
    #     """
    #     print("paint")


if __name__ == '__main__':
    pass
