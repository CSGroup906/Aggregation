"""
    Author: JGK
    Time: 2020/11/19 15:16
"""
from collections import OrderedDict


class EdgeInfo:
    def __init__(self, name, start_node, end_node, capacity, probability_distribution):
        self.name = name
        self.start_node = start_node
        self.end_node = end_node
        self.capacity = capacity
        self.probability_distribution = probability_distribution


class Edges:
    def __init__(self, edges=None):
        self.edges = OrderedDict()
        if edges is not None:
            for edge in edges:
                self.add_edge(edge)

    def __getattr__(self, name):
        if hasattr(self.edges, name):
            return getattr(self.edges, name)
        else:
            return self.edges[name]

    def add_edge(self, edge):
        self.edges[edge.name] = edge
