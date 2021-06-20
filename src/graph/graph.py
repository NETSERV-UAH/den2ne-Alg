#!/usr/bin/python3

from node import Node


class Graph(object):
    """
        Clase para gestionar el gráfo que representará la red de distribución eléctrica 
    """

    def __init__(self, state, loads, edges, switches, root=150):
        """
            Constructor de la clase Graph el cual conformará el grafo a partir de los datos procesados.
        """
        self.root = root
        self.nodes = list()
        self.buildGraph()

    def buildGraph(self, state, loads, edges, switches):
