#!/usr/bin/python3

from graph.graph import Graph
from den2ne.den2neALG import Den2ne
from dataCollector.dataCollector import DataGatherer


def main():

    # Recolectamos los datos
    loads = DataGatherer.getLoads('data/loads.csv', 3)
    edges = DataGatherer.getEdges('data/links.csv')
    edges_conf = DataGatherer.getEdges_Config('data/links_config.csv')
    sw_edges = DataGatherer.getSwitches('data/switches.csv')
    positions = DataGatherer.getPositions('data/node_positions.csv')

    # Creamos la var del grafo para el primer instante
    G = Graph(0, loads, edges, sw_edges, edges_conf, root='150')

    # Parseamos a NetworkX y pintamos el grafo
    G.plotGraph(positions, 'IEEE 123 Node test feeder - Graph')

    # Podamos los nodos virtuales que estén a modo de ampliación.
    G.pruneGraph()

    # Podemos vovler a pintar para comprobar la poda realziada
    G.plotGraph(positions, ' IEEE 123 Node test feeder - Pruned Graph')

    # Iniciamos el algoritmo
    G_den2ne_alg = Den2ne(G)

    # Primera fase: difusión de IDs
    G_den2ne_alg.spread_ids()

    # Segunda fase: Decisión de IDs en base a un criterio
    G_den2ne_alg.selectBestIDs(Den2ne.CRITERION_DISTANCE)

    # Tercera fase: Balance global de la red y establece los flujos de potencia
    total_balance = G_den2ne_alg.globalBalance_Ideal()

    # Pintamos de nuevo para ver los flujos de potencia
    G_den2ne_alg.G.plotDiGraph(positions, 'IEEE 123 Node test feeder - Directed Graph')

    # Genearación de informes
    G_den2ne_alg.write_ids_report('results/reports/report_ids.txt')
    G_den2ne_alg.write_swConfig_report('results/reports/report_swConfig.txt')

    # Generamos la configuración logica en formato CSV para su posterior procesado en Matlab
    G_den2ne_alg.write_swConfig_CSV('results/swConfig.csv')

    # Sacamos las figuras en modo iteractivo (Metodo que bloquea el flujo del script)
    G.showGraph()


if __name__ == "__main__":
    main()
