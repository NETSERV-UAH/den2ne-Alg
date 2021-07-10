#!/usr/bin/python3

import pathlib
from graph.graph import Graph
from den2ne.den2neALG import Den2ne
from dataCollector.dataCollector import DataGatherer


# Este es un ejemplo de uso de todo el repertorio de metodos programados para explorar la topología IEEE 123 y
# el algoritmo programado.


def usage():

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
    G_den2ne_alg.selectBestIDs(Den2ne.CRITERION_NUM_HOPS)

    # Tercera fase: Balance global de la red y establece los flujos de potencia
    [total_balance_ideal, abs_flux] = G_den2ne_alg.globalBalance(withLosses=False, withCap=False, withDebugPlot=False, positions=positions, path='results/')

    # Podemos calcular las perdidas totales:
    G_den2ne_alg.updateLoads(loads, 0)
    G_den2ne_alg.clearSelectedIDs()
    G_den2ne_alg.selectBestIDs(Den2ne.CRITERION_NUM_HOPS)
    [total_balance_with_losses, abs_flux_with_losses] = G_den2ne_alg.globalBalance(withLosses=True, withCap=False, withDebugPlot=False, positions=positions, path='results/')

    loss = total_balance_ideal - total_balance_with_losses

    # Pintamos de nuevo para ver los flujos de potencia
    G_den2ne_alg.G.plotDiGraph(positions, 'IEEE 123 Node test feeder - Directed Graph')

    # Genearación de informes
    G_den2ne_alg.write_ids_report('results/reports/report_ids.txt')
    G_den2ne_alg.write_swConfig_report('results/reports/report_swConfig.txt')
    G_den2ne_alg.write_loads_report('results/reports/report_loads.txt')

    # Generamos la configuración logica en formato CSV para su posterior procesado en Matlab
    G_den2ne_alg.write_swConfig_CSV('results/swConfig.csv')

    # Sacamos las figuras en modo iteractivo (Metodo que bloquea el flujo del script)
    G.showGraph()


# Vamos a programar unas pruebas globales sobre la topología IEEE 123
def test_ieee123():

    # Variables
    dirs = ['reports', 'csv', 'fig']
    topo_name = 'ieee123'
    criteria = [Den2ne.CRITERION_NUM_HOPS, Den2ne.CRITERION_DISTANCE, Den2ne.CRITERION_LINKS_LOSSES,
                Den2ne.CRITERION_POWER_BALANCE, Den2ne.CRITERION_POWER_BALANCE_WITH_LOSSES]
    out_data = dict()

    # Preparamos los directorios de resultados
    for dir in dirs:
        pathlib.Path('results/' + topo_name + '/' + dir).mkdir(parents=True, exist_ok=True)

    # Recolectamos los datos
    loads = DataGatherer.getLoads('data/loads.csv', 3)
    edges = DataGatherer.getEdges('data/links.csv')
    edges_conf = DataGatherer.getEdges_Config('data/links_config.csv')
    sw_edges = DataGatherer.getSwitches('data/switches.csv')
    positions = DataGatherer.getPositions('data/node_positions.csv')

    # Creamos la var del grafo para el primer instante
    G = Graph(0, loads, edges, sw_edges, edges_conf, root='150')

    # Podamos los nodos virtuales que estén a modo de ampliación.
    G.pruneGraph()

    # Iniciamos el algoritmo
    G_den2ne_alg = Den2ne(G)

    # Primera fase: difusión de IDs
    G_den2ne_alg.spread_ids()

    # Vamos a iterar por todos los intantes de cargas
    for delta in range(0, len(loads['1'])):

        # Vamos a iterar por criterio
        for criterion in criteria:

            # Init Loads
            G_den2ne_alg.updateLoads(loads, delta)
            G_den2ne_alg.clearSelectedIDs()
            G_den2ne_alg.selectBestIDs(criterion)

            # Ideal balance
            [total_balance_ideal, abs_flux] = G_den2ne_alg.globalBalance(withLosses=False, withCap=False, withDebugPlot=False, positions=positions, path='results/')

            # Re-Init loads
            G_den2ne_alg.updateLoads(loads, delta)
            G_den2ne_alg.clearSelectedIDs()
            G_den2ne_alg.selectBestIDs(criterion)

            # Withloss balance
            [total_balance_with_losses, abs_flux_with_losses] = G_den2ne_alg.globalBalance(withLosses=True, withCap=False, withDebugPlot=False, positions=positions, path='results/')

            # Re-Init loads
            G_den2ne_alg.updateLoads(loads, delta)
            G_den2ne_alg.clearSelectedIDs()
            G_den2ne_alg.selectBestIDs(criterion)

            # Withloss and Cap balance
            [total_balance_with_lossesCap, abs_flux_with_lossesCap] = G_den2ne_alg.globalBalance(withLosses=True, withCap=True, withDebugPlot=False, positions=positions, path='results/')

            # Save data
            out_data[delta][criteria] = {
                'total_balance_ideal': total_balance_ideal, 'abs_flux': abs_flux,
                'total_balance_with_losses': total_balance_with_losses, 'abs_flux_with_losses': abs_flux_with_losses,
                'total_balance_with_lossesCap': total_balance_with_lossesCap, 'abs_flux_with_lossesCap': abs_flux_with_lossesCap
            }

            # Genearación de informes
            G_den2ne_alg.write_swConfig_report(f'results/{topo_name}/report_swConfig_{delta}_{criterion}.txt')
            G_den2ne_alg.write_loads_report(f'results/{topo_name}/reports/report_loads_{delta}_{criterion}.txt')

            # Generamos la configuración logica
            G_den2ne_alg.write_swConfig_CSV(f'results/{topo_name}/csv/swConfig_{delta}_{criterion}.csv')

    G_den2ne_alg.write_ids_report(f'results/{topo_name}/reports/report_ids.txt')


if __name__ == "__main__":
    test_ieee123()
