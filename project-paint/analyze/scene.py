import math
from collections import OrderedDict

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import QLine


class GraphicScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)

        # settings
        self.grid_size = 20
        self.grid_squares = 5

        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 1000, 800)

        self.nodes = OrderedDict()
        self.edges = OrderedDict()

        self.state_probability_distribution = []

    def add_distribution(self, edge):
        self.state_probability_distribution.append(edge.edge_wrap.probability_distribution)

    def remove_distribution(self, edge):
        self.state_probability_distribution.pop(edge.edge_wrap.id)

    def add_node(self, node):
        print("add_node_before:\n\t{}".format(self.nodes.keys()))
        for i in range(1, (len(self.nodes.keys()))):
            if str(i) not in self.nodes.keys():
                node.nodeId = str(i)
                break
        self.nodes[node.nodeId] = node
        self.addItem(node)
        print("add_node_after:\n\t{}".format(self.nodes.keys()))

    def remove_node(self, node):
        print("remove_node_before:\n\t{}".format(self.nodes.keys()))
        self.nodes.pop(str(node.nodeId))
        self.removeItem(node)
        for edge in list(self.edges.values()):
            if edge.edge_wrap.start_item is node or edge.edge_wrap.end_item is node:
                self.remove_edge(edge)
        print("remove_node_after:\n\t{}".format(self.nodes.keys()))

    def add_edge(self, edge):
        print("add_edge_before:\n\t{}".format(self.edges.keys()))

        self.edges[edge.edge_wrap.id] = edge
        self.addItem(edge)
        print("add_edge_after:\n\t{}".format(self.edges.keys()))

    def remove_edge(self, edge):
        print("remove_edge_before:\n\t{}".format(self.edges.keys()))
        self.edges.pop(edge.edge_wrap.id)
        self.removeItem(edge)
        print("remove_edge_after:\n\t{}".format(self.edges.keys()))

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)
