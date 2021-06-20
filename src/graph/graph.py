#!/usr/bin/python3

class Graph(object):
    """
        Clase para gestionar el gráfo que representará la red de distribución eléctrica 
    """

    def __init__(self, loads, edges, switches, root=150):
        """
            Constructor de la clase Graph el cual conformará el grafo a partir de los datos procesados.
        """
