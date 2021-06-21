#!/usr/bin/python3

class Link(object):
    """
        Clase para gestionar un enlace del grafo
    """

    def __init__(self, type_link, state, dist, cap):
        """
            Constructor de la clase Link
        """
        self.type = type_link
        self.state = state
        self.dist = dist
        self.cap = cap

    # Tipos de enlace
    @property
    def NORMAL():
        return 1

    @property
    def SWITCH():
        return 0

    # Estados del enlace
    @property
    def OPEN():
        return 1

    @property
    def CLOSED():
        return 0

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
