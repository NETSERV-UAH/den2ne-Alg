#!/usr/bin/python3

import csv


class DataGatherer(object):
    """
        Clase para recolectar los datos suministrados en formato CSV
    """

    @staticmethod
    def getLoads(fileName, threshold):
        """
            Funcion para recolectar las cargas de los nodos
        """

        loads = dict()

        try:
            with open(fileName, 'r') as file:
                reader = csv.reader(file)
                lines = 0
                for row in reader:
                    if lines != 0:
                        loads[row[0]] = [round(float(load), threshold) for load in row[1:]]
                    lines += 1

        except Exception as e:
            print(str(e))

        return loads


data = DataGatherer.getLoads('data/loads.csv', 3)
print(str(data))
