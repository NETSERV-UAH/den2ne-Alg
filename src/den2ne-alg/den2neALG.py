#!/usr/bin/python3

from .den2neHLMAC import HLMAC


class Den2ne(object):
    """
        Clase para gestionar la lógica del algoritmo
    """

    def __init__(self, graft, root=150):
        """
            Constructor de la clase Den2ne 
        """
        self.G = graft
        self.root = root
