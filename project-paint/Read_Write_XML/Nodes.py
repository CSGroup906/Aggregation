"""
    Author: JGK
    Time: 2020/11/19 15:14
"""
from collections import OrderedDict


class Node:
    def __init__(self, name, position):
        self.name = name
        self.position = position

class Nodes:
    def __init__(self, nodes=None):
        self.nodes = OrderedDict()
        if nodes is not None:
            for node in nodes:
                self.add_node(node)

    def __getattr__(self, name):
        if hasattr(self.nodes, name):
            return getattr(self.nodes, name)
        else:
            return self.nodes[name]

    def add_node(self, node):
        self.nodes[node.name] = node
    def getName(self, nodeId):
        return self.nodes.nodeId