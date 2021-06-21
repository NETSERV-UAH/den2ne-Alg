#!/usr/bin/python3

class Link(object):
    """
        Clase para gestionar un enlace del grafo
    """

    # Declaramos tipos de enlace mediante variables estáticas de la clase
    NORMAL = 1
    SWITCH = 0

    def __init__(self, type_link, state, dist, cap):
        """
            Constructor de la clase Link
        """
        self.type = type_link
        self.state = state
        self.dist = dist
        self.cap = cap

    @staticmethod
    def ft2meters(fts):
        """
            Funcion de conversion a feet (american unit)
        """
        return (fts)/3.28084

    @staticmethod
    def meters2ft(meters):
        """
            Funcion de conversion a metros
        """
        return meters * 3.28084
