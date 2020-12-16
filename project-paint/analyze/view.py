import types

from Read_Write_XML.Main import *
from item import GraphicItem
import xml.dom.minidom
from PyQt5.QtWidgets import QGraphicsView, QDialog, QGraphicsPathItem, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter

from edge import Edge, GraphicEdge
from Interaction.AttributeWindow import UiNodeAttr, UiEdgeAttr


class GraphicView(QGraphicsView):

    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)

        self.gr_scene = graphic_scene
        self.parent = parent
        self.directed = True
        self.drag_edge = None
        # 判断当前状态是否为删除
        self.is_delete = False
        self.is_node = False
        self.is_edge = False

        self.init_ui()
        self.x = 0
        self.y = 0
    def init_ui(self):
        self.setScene(self.gr_scene)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform |
                            QPainter.LosslessImageRendering)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setDragMode(self.RubberBandDrag)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_N:
    #         print('view')
    #         item = GraphicItem(40, str(len(self.gr_scene.nodes) + 1))
    #         item.setPos(0, 0)
    #         self.gr_scene.add_node(item)
    #     if event.key() == Qt.Key_E:
    #         self.is_edge = ~self.is_edge
    #     # 组合键 Ctrl+O
    #     if (event.modifiers() == Qt.ControlModifier) & (event.key() == Qt.Key_O):
    #         self.load('network')
    #     if (event.modifiers() == Qt.ControlModifier) & (event.key() == Qt.Key_S):
    #         self.save('network1')
    #
    #     if (event.key() == Qt.Key_P):
    #         for k, e in self.gr_scene.edges.items():
    #             print(e.edge_wrap.start_item.nodeId, e.edge_wrap.end_item.nodeId)

    def mousePressEvent(self, event):
        item = self.get_item_at_click(event)
        self.x = event.x()
        self.y = event.y()
        # 右键修改对象属性
        if event.button() == Qt.RightButton:
            if hasattr(item, 'r'):
                self.showNodeAttr(item)
                for edge in list(self.gr_scene.edges.values()):
                    if edge.edge_wrap.start_item is item or edge.edge_wrap.end_item is item:
                        edge.edge_wrap.update_positions()
            elif hasattr(item, 'capacity'):
                self.showEdgeAttr(item)
        elif event.button() == Qt.LeftButton:
            # 先判断连线状态
            if self.windowTitle() != "网络可靠性":
                if self.is_edge:
                    if hasattr(item, 'r'):
                        self.edge_drag_start(item)
                # 再判断是否点了删除按钮
                elif self.is_delete:
                    # 根据不同类型调用不同的删除函数
                    if hasattr(item, 'r'):
                        self.gr_scene.remove_node(item)
                    elif hasattr(item, 'capacity'):
                        self.gr_scene.remove_edge(item)
                    # 删除一次后把is_delete还原
                    # self.is_delete = False
                elif self.is_node:
                    item = GraphicItem(40, str(len(self.gr_scene.nodes) + 1))
                    item.setPos(self.x, self.y)
                    self.gr_scene.add_node(item)
                else:
                    # # 如果没点删除键，点击边就可以换方向
                    # if hasattr(item, 'capacity'):
                    #     self.changeDirection(item)
                    super().mousePressEvent(event)

    def showNodeAttr(self, node):  # 定义窗口跳转槽函数
        dialog = QDialog()
        uiNodeAttr = UiNodeAttr()
        uiNodeAttr.setupUi(dialog, node, self.gr_scene.nodes)
        dialog.show()
        dialog.exec_()

    def showEdgeAttr(self, edge):  # 定义窗口跳转槽函数
        dialog = QDialog()
        uiEdgeAttr = UiEdgeAttr()
        uiEdgeAttr.setupUi(dialog, edge, self.gr_scene)
        dialog.show()
        dialog.exec_()

    # def showEdgeAttr(self, node):  # 定义窗口跳转槽函数
    #     print("待完善")
    #     # dialog = QDialog()
    #     # uiNodeAttr = UiNodeAttr()
    #     # uiNodeAttr.setupUi(dialog, node)
    #     # dialog.show()
    #     # dialog.exec_()

    def get_item_at_click(self, event):
        """ Return the object that clicked on. """
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def get_items_at_rubber(self):
        """ Get group select items. """
        area = self.rubberBandRect()
        return self.items(area)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.is_edge and self.drag_edge is not None:
            sc_pos = self.mapToScene(pos)
            self.drag_edge.gr_edge.set_dst(sc_pos.x(), sc_pos.y())
            self.drag_edge.gr_edge.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_edge:
            # self.is_edge = False
            item = self.get_item_at_click(event)
            if hasattr(item, 'r') and item is not self.drag_start_item:
                self.edge_drag_end(item)
            else:
                try:
                    self.drag_edge.remove()
                    self.drag_edge = None
                except AttributeError:
                    pass
        else:
            super().mouseReleaseEvent(event)

    def edge_drag_start(self, item):
        # 开始拖动时，产生一条边，并添加到edge中
        self.drag_start_item = item
        self.drag_edge = Edge(self.gr_scene, self.drag_start_item, None, None, '0')

    def edge_drag_end(self, item):
        edge_id = str(len(self.gr_scene.edges))
        for i in range(1, (len(self.gr_scene.edges.keys()))):
            if str(i) not in self.gr_scene.edges.keys():
                edge_id = str(i)
                break
        Edge(self.gr_scene, self.drag_start_item, item, 4, edge_id, directed=self.directed)
        self.drag_edge.remove()
        self.drag_edge = None

    # 改变线的方向
    def changeDirection(self, edge):
        temp = edge.edge_wrap.start_item
        edge.edge_wrap.start_item = edge.edge_wrap.end_item
        edge.edge_wrap.end_item = temp
        edge.edge_wrap.update_positions()

        edge.update()

    def load(self, filePath):
        ns, es, directed, radius = read_xml(filePath)[:4]
        self.directed = directed
        for n in ns.nodes:
            id = ns.nodes[n].name
            x = ns.nodes[n].position[0]
            y = ns.nodes[n].position[1]
            item = GraphicItem(radius, id)
            item.setPos(x, y)
            self.gr_scene.add_node(item)
        for e in es.edges:
            id = es.edges[e].name
            capacity = es.edges[e].capacity
            start = es.edges[e].start_node
            end = es.edges[e].end_node
            start_item = self.gr_scene.nodes[start.name]
            end_item = self.gr_scene.nodes[end.name]
            probability_distribution = es.edges[e].probability_distribution
            # print("load_probability_distribution", id, probability_distribution)
            Edge(self.gr_scene, start_item, end_item, capacity, id, probability_distribution, self.directed)

    def save(self, fileName):
        nodeList = []
        r = None
        for node in self.gr_scene.nodes.values():
            nodeList.append(Node(node.nodeId, (int(node.pos().x()), int(node.pos().y()))))
            r = node.r
        ns = Nodes(nodeList)

        edgeList = []
        for edge in self.gr_scene.edges.values():
            edgeId = edge.edge_wrap.id
            s = ns.nodes[edge.edge_wrap.start_item.nodeId]
            e = ns.nodes[edge.edge_wrap.end_item.nodeId]
            c = self.gr_scene.edges[edgeId].capacity
            p = edge.edge_wrap.probability_distribution
            edgeList.append(EdgeInfo(str(edge.edge_wrap.id), s, e, c, p))
        es = Edges(edgeList)
        write_xml(ns, es, fileName, radius=r,directed=self.directed)
