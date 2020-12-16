

from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PyQt5.QtGui import QColor, QPen, QBrush, QPainterPath, QPolygonF, QFont, QPainterPathStroker
from PyQt5.QtCore import Qt, QPointF, QLineF


class Edge:

    def __init__(self, scene, start_item, end_item, capacity, id, probability_distribution=None, directed=True):
        super().__init__()
        if probability_distribution is None:
            probability_distribution = []
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item
        self.capacity = capacity
        self.id = id
        while self.id in self.scene.edges.keys():
            self.id = str(int(self.id) + 1)
        self.gr_edge = GraphicEdge(self, directed)
        # add edge on graphic scene
        self.scene.add_edge(self.gr_edge)
        self.probability_distribution = probability_distribution
        if self.start_item is not None:
            self.update_positions()

    def store(self):
        self.scene.add_edge(self.gr_edge)

    def update_positions(self):
        startPatch = self.start_item.width / 4

        src_pos = self.start_item.pos()
        self.gr_edge.set_src(src_pos.x() + startPatch, src_pos.y() + startPatch)
        if self.end_item is not None:
            end_pos = self.end_item.pos()
            endPatch = self.end_item.width / 4
            self.gr_edge.set_dst(end_pos.x() + endPatch, end_pos.y() + endPatch)
        else:
            self.gr_edge.set_dst(src_pos.x() + startPatch, src_pos.y() + startPatch)
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        self.gr_edge = None


class GraphicEdge(QGraphicsPathItem):

    def __init__(self, edge_wrap, directed, parent=None):
        super().__init__(parent)
        self.edge_wrap = edge_wrap
        self.width = 3.0
        self.pos_src = [0, 0]
        self.pos_dst = [0, 0]
        # 是否有向
        self.directed = directed
        self.flag = 0
        self.capacity = self.edge_wrap.capacity

        self.setAcceptHoverEvents(True)
        # 普通画图时的pen样式
        self._n_pen = QPen(QColor("#000"))
        self._n_pen.setWidthF(self.width)
        # 画图时的pen样式
        self._pen = self._n_pen
        # 悬浮时的pen样式
        self._hover_pen = QPen(Qt.green)
        self._hover_pen.setWidthF(self.width)
        # 拖拽时的样式
        self._pen_dragging = QPen(QColor("#000"))
        self._pen_dragging.setStyle(Qt.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self._mark_brush = QBrush()
        self._mark_brush.setColor(Qt.green)
        self._mark_brush.setStyle(Qt.SolidPattern)

        self._normal_brush = QBrush()
        self._normal_brush.setColor(Qt.black)
        self._normal_brush.setStyle(Qt.SolidPattern)

        self.brush = self._normal_brush

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

    def set_src(self, x, y):
        self.pos_src = [x, y]

    def set_dst(self, x, y):
        self.pos_dst = [x, y]

    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))  # 起点
        path.lineTo(QPointF(self.pos_dst[0], self.pos_dst[1]))  # 终点
        if self.directed:
            # 画箭头
            self.line = QLineF(QPointF(self.pos_src[0], self.pos_src[1]), QPointF(self.pos_dst[0], self.pos_dst[1]))
            if self.flag == 0:
                self.line.setLength(self.line.length() - 20)
            else:
                self.line.setLength(self.line.length() - self.edge_wrap.end_item.r)
            v = self.line.unitVector()
            v.setLength(20)
            v.translate(QPointF(self.line.dx(), self.line.dy()))

            n = v.normalVector()
            n.setLength(n.length() * 0.5)
            n2 = n.normalVector().normalVector()

            p1 = v.p2()
            p2 = n.p2()
            p3 = n2.p2()
            # 方法2
            arrow = QPolygonF([p1, p2, p3, p1])
            path.addPolygon(arrow)
        # path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))
        # path.lineTo(self.pos_dst[0], self.pos_dst[1])
        return path

    def boundingRect(self):
        return self.shape().boundingRect()

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
        self.brush = self._mark_brush
        self._pen = self._hover_pen
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        self.brush = self._normal_brush
        self._pen = self._n_pen
        self.update()

    def shape(self):
        # 设置宽度 这里用了100 很大
        qps = QPainterPathStroker()
        qps.setWidth(100)
        return qps.createStroke(self.calc_path())

    def paint(self, painter, graphics_item, widget=None):

        if self.edge_wrap.end_item is None:
            self.ensureVisible()
            self.setPath(self.calc_path())
            path = self.path()

            painter.setPen(self._pen_dragging)
            painter.setBrush(self.brush)
            painter.drawPath(path)
        else:
            # 这画的才是连接后的线
            self.flag = 1
            self.setPath(self.calc_path())  # 设置路径
            path = self.path()
            painter.setPen(self._pen)
            painter.setBrush(self.brush)
            painter.drawPath(path)
            self.flag = 0
            painter.setFont(QFont("Times New Roman", 16))
            painter.setPen(Qt.red)
            x = int((self.pos_src[0] + self.pos_dst[0]) / 2 - 17)
            y = int((self.pos_src[1] + self.pos_dst[1]) / 2 - 7)
            painter.drawText(x, y, "({}) {}".format(self.edge_wrap.id, self.capacity))
