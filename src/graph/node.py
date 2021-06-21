#!/usr/bin/python3

from link import Link


class Node(object):
    """
        Clase para gestionar un nodo del grafo
    """

    def __init__(self, name, type_node, load=0, neighbors=[]):
        """
            Constructor de la clase Node
        """
        self.name = name
        self.type = type_node
        self.load = load
        self.neighbors = neighbors
        self.links = list()

    def addNeigbor(self, neighbor, dist, cap, type_link, state):
        """
            Funcion para añadir un vecino
        """
        self.neighbors.append(neighbor)
        self.links.append(Link(type_link, state, dist, cap))

    # Tipos de nodos

    @property
    def NORMAL():
        return 1

    @property
    def VIRTUAL():
        return 0
