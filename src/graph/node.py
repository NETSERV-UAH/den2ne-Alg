#!/usr/bin/python3

class Node(object):
    """
        Clase para gestionar un nodo del grafo
    """

    def __init__(self, name, load, neighbors):
        """
            Constructor de la clase Node
        """
        self.name = name
        self.load = load
        self.neighbors = neighbors
