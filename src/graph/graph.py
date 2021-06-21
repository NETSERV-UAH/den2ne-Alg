#!/usr/bin/python3

from .node import Node
from .link import Link


class Graph(object):
    """
        Clase para gestionar el gráfo que representará la red de distribución eléctrica 
    """

    def __init__(self, delta, loads, edges, switches, root=150):
        """
            Constructor de la clase Graph el cual conformará el grafo a partir de los datos procesados.
        """
        self.root = root
        self.nodes = list()
        self.buildGraph(delta, loads, edges, switches)

    def buildGraph(self, delta, loads, edges, switches):
        """
            Función para generar el grafo
        """

        # Primero vamos a añadir todos los nodos normales del grafo, ya que los tenemos listados con sus cargas en loads.
        for node in loads:
            self.nodes.append(Node(node, Node.NORMAL, loads[node][delta]))

        # Acto seguido vamos añadir todos los nodos virtuales
        for edge in edges:
            if self.findNode(edge["node_a"]) is None:
                self.nodes.append(Node(edge["node_a"], Node.VIRTUAL, 0))
            elif self.findNode(edge["node_b"]) is None:
                self.nodes.append(Node(edge["node_b"], Node.VIRTUAL, 0))

        for sw_edge in switches:
            if self.findNode(sw_edge["node_a"]) is None:
                self.nodes.append(Node(sw_edge["node_a"], Node.VIRTUAL, 0))
            elif self.findNode(sw_edge["node_b"]) is None:
                self.nodes.append(Node(sw_edge["node_b"], Node.VIRTUAL, 0))

        # A continuación, vamos a añadir a los nodos sus vecinos. Cada enlace es bi-direccional.
        for edge in edges:
            self.nodes[(self.findNode(edge["node_a"])[0])].addNeigbor(edge["node_b"], Link.NORMAL, 'closed', edge["dist"], edge["cap"])
            self.nodes[(self.findNode(edge["node_b"])[0])].addNeigbor(edge["node_a"], Link.NORMAL, 'closed', edge["dist"], edge["cap"])

        for sw_edge in switches:
            self.nodes[self.findNode(sw_edge["node_a"])[0]].addNeigbor(sw_edge["node_b"], Link.SWITCH, sw_edge["state"], 0, 3)
            self.nodes[self.findNode(sw_edge["node_b"])[0]].addNeigbor(sw_edge["node_a"], Link.SWITCH, sw_edge["state"], 0, 3)

    def findNode(self, name):
        """
            Funcion para buscar un nodo en la lista del grafo
        """

        for node in self.nodes:
            if node.name == name:
                return [self.nodes.index(node), node]

        return None
