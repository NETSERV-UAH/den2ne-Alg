#!/usr/bin/python3

from graph.graph import Graph
from dataCollector.dataCollector import DataGatherer


def main():

    # Recolectamos los datos
    loads = DataGatherer.getLoads('data/loads.csv', 3)
    edges = DataGatherer.getEdges('data/links.csv')
    sw_edges = DataGatherer.getSwitches('data/switches.csv')
    positions = DataGatherer.getPositions('data/node_positions.csv')

    # Creamos la var del grafo para el primer instante
    G = Graph(0, loads, edges, sw_edges)

    # Parseamos a NetworkX y pintamos el grafo
    G.plotGraph(positions)

    print('Ejecutamos mas cosas')

    # Sacamos las figuras en modo iteractivo (Metodo que bloquea el flujo del script)
    G.showGraph()

if __name__ == "__main__":
    main()
