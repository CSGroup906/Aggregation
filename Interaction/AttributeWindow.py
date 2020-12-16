from PyQt5 import QtCore, QtGui, QtWidgets

from analyze.edge import Edge, GraphicEdge
from Read_Write_XML.Edges import EdgeInfo


class UiNodeAttr(object):
    def setupUi(self, Dialog, node, nodeDic):
        Dialog.setObjectName("Dialog")
        Dialog.resize(251, 169)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-90, 130, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButtonName = QtWidgets.QPushButton(Dialog)
        self.pushButtonName.setGeometry(QtCore.QRect(30, 10, 75, 23))
        self.pushButtonName.setObjectName("pushButtonName")
        self.pushButtonX = QtWidgets.QPushButton(Dialog)
        self.pushButtonX.setGeometry(QtCore.QRect(30, 50, 75, 23))
        self.pushButtonX.setObjectName("pushButtonX")
        self.pushButtonY = QtWidgets.QPushButton(Dialog)
        self.pushButtonY.setGeometry(QtCore.QRect(30, 90, 75, 23))
        self.pushButtonY.setObjectName("pushButtonY")
        self.lineEditName = QtWidgets.QLineEdit(Dialog)
        self.lineEditName.setGeometry(QtCore.QRect(120, 10, 113, 20))
        self.lineEditName.setObjectName("lineEditName")
        self.lineEditName.setPlaceholderText(str(node.nodeId))
        self.lineEditX = QtWidgets.QLineEdit(Dialog)
        self.lineEditX.setGeometry(QtCore.QRect(120, 50, 113, 20))
        self.lineEditX.setObjectName("lineEditX")
        self.lineEditX.setPlaceholderText(str(int(node.pos().x())))
        self.lineEditY = QtWidgets.QLineEdit(Dialog)
        self.lineEditY.setGeometry(QtCore.QRect(120, 90, 113, 21))
        self.lineEditY.setObjectName("lineEditY")
        self.lineEditY.setPlaceholderText(str(int(node.pos().y())))

        self.node = node
        self.nodeDic = nodeDic
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok_met)
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "修改当前节点参数"))
        self.pushButtonName.setText(_translate("Dialog", "名称"))
        self.pushButtonX.setText(_translate("Dialog", "x坐标"))
        self.pushButtonY.setText(_translate("Dialog", "y坐标"))

    def ok_met(self):
        if self.lineEditName.text():
            if self.lineEditName.text() not in self.nodeDic.keys():
                # print('change_nodeName_before:\n\t', self.nodeDic)
                self.nodeDic.pop(self.node.nodeId)
                self.node.nodeId = self.lineEditName.text()
                self.nodeDic[self.node.nodeId] = self.node
                # print('change_nodeName_after:\n\t', self.nodeDic)
            else:
                QtWidgets.QMessageBox.warning(self.buttonBox, '警告！', '当前节点名称已存在！', QtWidgets.QMessageBox.Ok)
        if self.lineEditX.text():
            self.node.setX(int(self.lineEditX.text()))
        if self.lineEditY.text():
            self.node.setY(int(self.lineEditY.text()))


class UiEdgeAttr(object):
    def setupUi(self, Dialog, edge, gr_scene):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 289)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-30, 230, 221, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton_name = QtWidgets.QPushButton(Dialog)
        self.pushButton_name.setGeometry(QtCore.QRect(20, 30, 75, 23))
        self.pushButton_name.setObjectName("pushButton_name")
        self.pushButton_sNode = QtWidgets.QPushButton(Dialog)
        self.pushButton_sNode.setGeometry(QtCore.QRect(20, 70, 75, 23))
        self.pushButton_sNode.setObjectName("pushButton_sNode")
        self.pushButton_eNode = QtWidgets.QPushButton(Dialog)
        self.pushButton_eNode.setGeometry(QtCore.QRect(20, 110, 75, 23))
        self.pushButton_eNode.setObjectName("pushButton_eNode")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 150, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_PD = QtWidgets.QPushButton(Dialog)
        self.pushButton_PD.setGeometry(QtCore.QRect(20, 190, 75, 23))
        self.pushButton_PD.setObjectName("pushButton_PD")
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_name.setGeometry(QtCore.QRect(110, 30, 113, 20))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setPlaceholderText(edge.edge_wrap.id)
        self.lineEdit_sNode = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_sNode.setGeometry(QtCore.QRect(110, 70, 113, 20))
        self.lineEdit_sNode.setObjectName("lineEdit_sNode")
        self.lineEdit_sNode.setPlaceholderText(edge.edge_wrap.start_item.nodeId)
        self.lineEdit_eNode = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_eNode.setGeometry(QtCore.QRect(110, 110, 113, 20))
        self.lineEdit_eNode.setObjectName("lineEdit_eNode")
        self.lineEdit_eNode.setPlaceholderText(edge.edge_wrap.end_item.nodeId)
        self.lineEdit_capacity = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_capacity.setGeometry(QtCore.QRect(110, 150, 113, 20))
        self.lineEdit_capacity.setObjectName("lineEdit_capacity")
        self.lineEdit_capacity.setPlaceholderText(str(edge.capacity))
        self.lineEdit_PD = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_PD.setGeometry(QtCore.QRect(110, 190, 113, 20))
        self.lineEdit_PD.setObjectName("lineEdit_PD")
        self.lineEdit_PD.setPlaceholderText(str(edge.edge_wrap.probability_distribution))

        self.edge = edge
        self.gr_scene = gr_scene
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok_met)
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "修改当前边的参数"))
        self.pushButton_name.setText(_translate("Dialog", "边的名称"))
        self.pushButton_sNode.setText(_translate("Dialog", "开始节点"))
        self.pushButton_eNode.setText(_translate("Dialog", "目的节点"))
        self.pushButton_4.setText(_translate("Dialog", "边的容量"))
        self.pushButton_PD.setText(_translate("Dialog", "概率分布"))

    def ok_met(self):
        if self.lineEdit_name.text():
            if self.lineEdit_name.text() not in self.gr_scene.edges.keys():
                self.gr_scene.edges.pop(self.edge.edge_wrap.id)
                self.edge.edge_wrap.id = self.lineEdit_name.text()
                self.gr_scene.edges[self.edge.edge_wrap.id] = self.edge
            else:
                QtWidgets.QMessageBox.warning(self.buttonBox, '警告！', '当前边的名称已存在！', QtWidgets.QMessageBox.Ok)
        if self.lineEdit_capacity.text():
            self.gr_scene.edges[self.edge.edge_wrap.id].capacity = int(self.lineEdit_capacity.text())
        if self.lineEdit_PD.text():
            pd = self.lineEdit_PD.text().split(',')
            self.edge.edge_wrap.probability_distribution = [float(p) for p in pd]
        if self.lineEdit_sNode.text() or self.lineEdit_eNode.text():
            if self.lineEdit_sNode.text():
                if self.lineEdit_sNode.text() in self.gr_scene.nodes.keys():
                    start_node = self.lineEdit_sNode.text()
                    self.edge.edge_wrap.start_item = self.gr_scene.nodes[start_node]
                else:
                    QtWidgets.QMessageBox.warning(self.buttonBox, '警告！', '当前开始节点不存在！', QtWidgets.QMessageBox.Ok)
            if self.lineEdit_eNode.text():
                if self.lineEdit_eNode.text() in self.gr_scene.nodes.keys():
                    end_node = self.lineEdit_eNode.text()
                    self.edge.edge_wrap.end_item = self.gr_scene.nodes[end_node]
                else:
                    QtWidgets.QMessageBox.warning(self.buttonBox, '警告！', '当前目的节点不存在！', QtWidgets.QMessageBox.Ok)
            self.edge.edge_wrap.update_positions()
            # self.edge.update()


if __name__ == "__main__":
    pass
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # Dialog = QtWidgets.QDialog()
    # ui = UiNodeAttr()
    # node = GraphicItem(40, 'exam_node')
    # ui.setupUi(Dialog, node)
    # Dialog.show()
    # sys.exit(app.exec_())
