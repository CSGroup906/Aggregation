"""
    Author: JGK
    Time: 2020/11/19 14:20
"""
from xml.dom import minidom

from Nodes import *
from Edges import *


def write_xml(ns, es, file_name, directed=True, radius=100,
              minimal_path_set_search=None, D_MP_search=None, reliability_evaluation=None):
    doc = minidom.Document()
    network = doc.createElement("network")
    network.setAttribute("directed", str(directed))
    network.setAttribute("radius", str(radius))
    doc.appendChild(network)

    nodes = doc.createElement("nodes")
    # nodes.appendChild(doc.createTextNode(', '.join(n for n in ns.nodes)))
    for n in ns.nodes.values():
        node = doc.createElement("node")
        node.setAttribute("name", n.name)
        node.setAttribute("position", str(n.position))
        nodes.appendChild(node)
    network.appendChild(nodes)

    edges = doc.createElement("edges")
    # edges.appendChild(doc.createTextNode(', '.join(e for e in es.edges)))
    for e in es.edges.values():
        edge = doc.createElement("edge")
        edge.setAttribute("name", e.name)
        edge.setAttribute("start_node", e.start_node.name)
        edge.setAttribute("end_node", e.end_node.name)
        edge.setAttribute("capacity", str(e.capacity))
        edge.setAttribute("probability_distribution", str(e.probability_distribution))
        edges.appendChild(edge)
    network.appendChild(edges)

    results = doc.createElement("results")
    mpss = doc.createElement("minimal_path_set_search")
    mpss.appendChild(doc.createTextNode(str(minimal_path_set_search)))
    results.appendChild(mpss)
    dmps = doc.createElement("D_MP_search")
    dmps.appendChild(doc.createTextNode(str(D_MP_search)))
    results.appendChild(dmps)
    re = doc.createElement("reliability_evaluation")
    re.appendChild(doc.createTextNode(str(reliability_evaluation)))
    results.appendChild(re)
    network.appendChild(results)

    f = open(file_name + ".xml", "w")
    f.write(doc.toprettyxml(indent="  "))
    f.close()


def read_xml(file_name):
    doc = minidom.parse(file_name + ".xml").documentElement
    directed = True
    if doc.getAttribute("directed") == 'False':
        directed = False
    radius = int(doc.getAttribute("radius"))
    minimal_path_set_search = doc.getElementsByTagName("minimal_path_set_search")[0].firstChild.data
    if minimal_path_set_search == 'None':
        minimal_path_set_search = None
    D_MP_search = doc.getElementsByTagName("D_MP_search")[0].firstChild.data
    if D_MP_search == 'None':
        D_MP_search = None
    reliability_evaluation = doc.getElementsByTagName("reliability_evaluation")[0].firstChild.data
    if reliability_evaluation == 'None':
        reliability_evaluation = None

    ns = Nodes()
    nodes = doc.getElementsByTagName("node")
    for node in nodes:
        name = node.getAttribute("name")
        p = node.getAttribute("position")
        position = tuple(map(int, p[1:-1].split(', ')))
        ns.add_node(Node(name, position))

    es = Edges()
    edges = doc.getElementsByTagName("edge")
    for edge in edges:
        name = edge.getAttribute("name")
        start_node = edge.getAttribute("start_node")
        end_node = edge.getAttribute("end_node")
        capacity = int(edge.getAttribute("capacity"))
        probability_distribution = edge.getAttribute("probability_distribution")
        if probability_distribution == '[]':
            probability_distribution = None
        es.add_edge(EdgeInfo(name, ns.nodes[start_node], ns.nodes[end_node], capacity, probability_distribution))
    return ns, es, directed, radius, minimal_path_set_search, D_MP_search, reliability_evaluation


if __name__ == '__main__':
    fn1 = 'network'
    ns1 = Nodes([Node('n1', (1, 1)), Node('n2', (1, 2)),
                 Node('n3', (2, 1)), Node('n4', (1, 2))])
    es1 = Edges([EdgeInfo('e1', ns1.n1, ns1.n2, 3, []), EdgeInfo('e2', ns1.n2, ns1.n3, 3, []),
                 EdgeInfo('e3', ns1.n3, ns1.n4, 3, []), EdgeInfo('e4', ns1.n4, ns1.n1, 3, [])])
    write_xml(ns1, es1, fn1)

    ns2, es2 = read_xml(fn1)[:2]

    write_xml(ns1, es1, fn1 + '_')
