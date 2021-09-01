#!/usr/bin/python3
 
import pathlib
from graph.graph import Graph
from den2ne.den2neALG import Den2ne
from dataCollector.dataCollector import DataGatherer

def brite():
    loads = DataGatherer.getLoads('data/loads.csv', 3)
    edges = DataGatherer.getEdges('data/links.csv')
    edges_conf = DataGatherer.getEdges_Config('data/links_config.csv')
    sw_edges = DataGatherer.getSwitches('data/switches.csv')
    positions = DataGatherer.getPositions('data/node_positions.csv')
    G = Graph(0, loads, edges, sw_edges, edges_conf, json_path= '../../brite-patch-master/resultados_brite/prueba4.brite', root= '150')
    G.saveGraph('brite_prueba4.json')

if __name__ == "__main__":
    brite()
