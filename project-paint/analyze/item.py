import typing
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsEllipseItem, QWidget
from PyQt5.QtGui import QPixmap, QFont, QBrush


class GraphicItem(QGraphicsEllipseItem):

    def __init__(self, radius, nodeId, x=0, y=0):
        super().__init__(x, y, radius, radius)
        self.width = radius * 2
        self.height = radius * 2
        self.r = radius
        self.x = x
        self.y = y
        self.setBrush(Qt.white)
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择的
        self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动的
        self.nodeId = nodeId

        # 开启悬停
        self.setAcceptHoverEvents(True)

        self._mark_brush = QBrush()
        self._mark_brush.setColor(Qt.green)
        self._mark_brush.setStyle(Qt.SolidPattern)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # update selected node and its edge
        if self.isSelected():
            for gr_edge in self.scene().edges.values():
                gr_edge.edge_wrap.update_positions()

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
        self.setBrush(Qt.green)
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        self.setBrush(Qt.white)
        self.update()

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...):
        super().paint(painter, option, widget)
        painter.setFont(QFont("Times New Roman", 16))
        # print(self.nodeId,self.x,self.y)
        q = self.x + self.width / 4 - 7
        e = self.y + self.width / 4 + 7
        painter.drawText(q, e, self.nodeId)
