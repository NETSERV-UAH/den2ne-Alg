#!/usr/bin/python3

import csv


class DataGatherer(object):
    """
        Clase para recolectar los datos suministrados en formato CSV
    """

    @staticmethod
    def getLoads(filename, threshold):
        """
            Funcion para recolectar las cargas de los nodos
        """

        loads = dict()

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                lines = 0
                for row in reader:
                    if lines != 0:
                        loads[row[0]] = [round(float(load), threshold) for load in row[1:]]
                    lines += 1

        except Exception as e:
            print(str(e))

        return loads

    @staticmethod
    def getEdges(filename):
        """
            Funcion para recolectar los enlaces del grafo
        """

        edges = list()

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                lines = 0
                for row in reader:
                    if lines >= 3:
                        edges.append({"node_a": row[0], "node_b": row[1], "dist": int(row[2]), "cap": int(row[3])})
                    lines += 1

        except Exception as e:
            print(str(e))

        return edges

    @staticmethod
    def getSwitches(filename):
        """
            Funcion para recolectar los enlaces especiales del grafo con posibilidad de conmutar
        """

        switches = list()

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                lines = 0
                for row in reader:
                    if lines >= 3:
                        switches.append({"node_a": row[0], "node_b": row[1], "state": row[2]})
                    lines += 1

        except Exception as e:
            print(str(e))

        return switches


data = DataGatherer.getLoads('data/loads.csv', 3)
print(str(data))

# Obtener
