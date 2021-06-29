#!/usr/bin/python3

from .link import Link


class Node(object):
    """
        Clase para gestionar un nodo del grafo
    """

    # Declaramos los tipos de nodos mediante variables estáticas de la clase
    NORMAL = 1
    VIRTUAL = 0

    def __init__(self, name, type_node, load=0):
        """
            Constructor de la clase Node
        """
        self.name = name
        self.type = type_node
        self.load = load
        self.neighbors = list()
        self.links = list()
        self.ids = list()

    def addNeighbor(self, neighbor, type_link, state, dist, cap):
        """
            Funcion para añadir un vecino
        """
        self.neighbors.append(neighbor)
        self.links.append(Link(type_link, state, dist, cap))

    def getActiveID(self):
        """
            Función para obtener el ID activo
        """
        ret_ID = None

        for id in self.ids:
            if id.active is True:
                ret_ID = id
                break

        return ret_ID
