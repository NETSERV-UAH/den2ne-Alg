#!/usr/bin/python3

import sys
import pathlib
from graph.graph import Graph
from den2ne.den2neALG import Den2ne
from den2ne.den2neALGMultiRoot import Den2neMultiRoot
from dataCollector.dataCollector import DataGatherer
import dataCollector.brite_intf as BRITE_interface
import time
import os
import datetime

#Variables globales
LOSSES = [False, True, False, True]
CAPACITY = [False, False, True, True]
DEBUG_PLOT = False

NUMBER_OF_ROOTS = 4

# Este es un test para ver como funciona el algoritmo en redes con múltiples nodos roots
CRITERION_NUM_HOPS = 0 
CRITERION_DISTANCE = 1 
CRITERION_POWER_BALANCE = 2 
CRITERION_POWER_BALANCE_WITH_LOSSES = 3
CRITERION_LINKS_LOSSES = 4 
CRITERION_POWER_BALANCE_WEIGHTED = 5

def test(path_results, path_topology, topo_seed, criterion, conf_losses, load_limit, n_runs):

    """
    Obj: Realizar las pruebas sistemáticas y guardar los resultados en un fichero de texto.
    ### PARÁMETROS ###
    - path_results (path)   -> Path del directorio en el que se almacenarán los resultados (empezado por ./) Ejemplo: ./results
    - path_topology (path)  -> Path del directorio donde se encuentran los ficheros de la topología en especifico (empieza por ./) Ejemplo: ./data/topos/waxman-30-4/seed_5/
    - topo_seed (int[1,10]) -> Semilla de la topología. Va implícita en path_topology pero para evitar buscar (Tienen que coincidir) Ejemplo: 5 (por seed_5)
    - criterion (int[0,4])  -> Índice del criterio elegido de la lista de criterios que se encuentra en ./den2ne/den2neALG.py
    - conf_losses (int[0,3])-> Índice de elección del escenario de pérdidas. Modifica valores de withLosses y withCap. 4 posibles escenarios
    - load_limit (int[0,1]) -> Existencia o no de límite de carga: (Si=1-No=0)
    - n_runs (int)          -> Número de ejecuciones que servirán para fijar la semilla de ejecución
    ##################
    """

    #Obtención ficheros de la topología
    node_file = path_topology + 'Nodos.csv'
    if not os.path.exists(node_file):
        print('Error, no existe el fichero ' + str(node_file))
        return
    edge_file = path_topology + 'Enlaces.csv'
    if not os.path.exists(edge_file):
        print('Error, no existe el fichero ' + str(edge_file))
        return

    #Crear directorios de resultados si no existen
    if not os.path.isdir(path_results):   #./results
        os.mkdir(path_results)

    data=path_topology.split('/')   #Obtención nombre topologia
    path_results=path_results+'/'+data[3]
    if not os.path.isdir(path_results):  #./results/topo_x_y
        os.mkdir(path_results)

    #Preparación de fichero de resultados
    file_name='outdata_seed_%d_c_%d.csv' % (topo_seed,criterion)
    root_file_name='rootdata_seed_%d_c_%d.csv' % (topo_seed,criterion)
    print('[' + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + '][INFO] Fichero de resultados generado: ' + path_results+ '/' + file_name)  #./results/topo_x_y/outdata_seed_%d_c_%s.csv
    file=open(path_results+ '/' + file_name, 'w')
    rootfile=open(path_results+ '/' + root_file_name, 'w')

    n_nodes = int(node_file.split('-')[1]
    #EJECUCIONES = n_runs con semillas
    for seed_run in range(n_runs):
        seed = n_nodes*10 + seed_run
        #Recogemos los datos de la topología BRITE con semilla de ejecución (seed run)
        if load_limit:
            loads = BRITE_interface.cargas_aleatorias_con_limite(node_file, seed)
        else:
            loads = BRITE_interface.cargas_aleatorias(node_file, seed)

        edges_conf = DataGatherer.getEdges_Config('data/links_config.csv')
        edges = BRITE_interface.BRITEedges(edge_file, edges_conf, seed)
        positions = BRITE_interface.BRITEpositions(node_file)
        root = BRITE_interface.selectMultiRoot(node_file, NUMBER_OF_ROOTS, seed)

        #Creamos el grafos
        G = Graph(0, loads, edges, list(), edges_conf, None, root)

        #ALGORITMO
        G_den2ne_alg = Den2neMultiRoot(G)

        inicio_id = time.time()
        G_den2ne_alg.spread_ids()
        fin_id = time.time()

        #Ahora seleccionamos las IDS por el criterio
        G_den2ne_alg.selectBestIDs(criterion)

        inicio_balance = time.time()
        [total_balance_ideal, abs_flux] = G_den2ne_alg.globalBalance(withLosses=LOSSES[conf_losses], withCap=CAPACITY[conf_losses], withDebugPlot=DEBUG_PLOT, positions=positions, path=path_results)
        # Si hay roots con carga negativa los cerramos como root y redirigimos la carga a otro nodo root
        roots_to_close = G_den2ne_alg.check_roots(total_balance_ideal)
        roots_closed = set()
        n_iteration = 0
        while len(roots_to_close) > 0:
            roots_closed = roots_closed.union(roots_to_close)
            # Limpiamos la seleccion de los IDs para volver a hacerla ahora quitando los roots cerrados
            G_den2ne_alg.updateLoads(loads, 0)
            G_den2ne_alg.clearSelectedIDs()
            # Reseleccionamos las IDs ahora teniendo en cuenta los roots cerrados
            G_den2ne_alg.selectBestIDs(int(criterion), roots_closed)
            [total_balance_ideal, abs_flux] = G_den2ne_alg.globalBalance(withLosses=LOSSES[conf_losses], withCap=CAPACITY[conf_losses], withDebugPlot=DEBUG_PLOT, positions=positions, path=path_results)
            roots_to_close = G_den2ne_alg.check_roots(total_balance_ideal)
            n_iteration += 1
        fin_balance = time.time()

        tiempo_balance = fin_balance - inicio_balance
        tiempo_id = fin_id - inicio_id

        #Por ahora para los resultados de balance voy a poner la suma de las cargas en todos los roots
        balance_global = 0
        for root in G_den2ne_alg.roots:
            balance_global += total_balance_ideal[root]
        #Escritura de resultados
        #FORMATO: seed_run, balance, abs_flux, time_ID, time_balance
        file.write(str(seed) + ',' + str(balance_global) + ',' + str(abs_flux) + ',' + str(tiempo_id) + ',' + str(tiempo_balance) + ',' +str(n_iteration) + '\n')
        rootfile.write(str(seed) + ',' + str(total_balance_ideal[G.root[0]]) + ',' + str(total_balance_ideal[G.root[1]]) + ',' + str(total_balance_ideal[G.root[2]]) + ',' + str(total_balance_ideal[G.root[3]]) + ',' +str(balance_global) + '\n')

    file.close()

def test_without_iterations(path_results, path_topology, topo_seed, criterion, conf_losses, load_limit, n_runs):

    """
    Codigo de pruebas sin iteraciones, busca obtener los reslutados sin cerrar los roots
    Obj: Realizar las pruebas sistemáticas y guardar los resultados en un fichero de texto.
    ### PARÁMETROS ###
    - path_results (path)   -> Path del directorio en el que se almacenarán los resultados (empezado por ./) Ejemplo: ./results
    - path_topology (path)  -> Path del directorio donde se encuentran los ficheros de la topología en especifico (empieza por ./) Ejemplo: ./data/topos/waxman-30-4/seed_5/
    - topo_seed (int[1,10]) -> Semilla de la topología. Va implícita en path_topology pero para evitar buscar (Tienen que coincidir) Ejemplo: 5 (por seed_5)
    - criterion (int[0,4])  -> Índice del criterio elegido de la lista de criterios que se encuentra en ./den2ne/den2neALG.py
    - conf_losses (int[0,3])-> Índice de elección del escenario de pérdidas. Modifica valores de withLosses y withCap. 4 posibles escenarios
    - load_limit (int[0,1]) -> Existencia o no de límite de carga: (Si=1-No=0)
    - n_runs (int)          -> Número de ejecuciones que servirán para fijar la semilla de ejecución
    ##################
    """

    #Obtención ficheros de la topología
    node_file = path_topology + 'Nodos.csv'
    if not os.path.exists(node_file):
        print('Error, no existe el fichero ' + str(node_file))
        return
    edge_file = path_topology + 'Enlaces.csv'
    if not os.path.exists(edge_file):
        print('Error, no existe el fichero ' + str(edge_file))
        return

    #Crear directorios de resultados si no existen
    if not os.path.isdir(path_results):   #./results
        os.mkdir(path_results)

    data=path_topology.split('/')   #Obtención nombre topologia
    path_results=path_results+'/'+data[3]
    if not os.path.isdir(path_results):  #./results/topo_x_y
        os.mkdir(path_results)

    #Preparación de fichero de resultados
    file_name='outdata_seed_%d_c_%d.csv' % (topo_seed,criterion)
    root_file_name='rootdata_seed_%d_c_%d.csv' % (topo_seed,criterion)
    print('[' + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + '][INFO] Fichero de resultados generado: ' + path_results+ '/' + file_name)  #./results/topo_x_y/outdata_seed_%d_c_%s.csv
    file=open(path_results+ '/' + file_name, 'w')
    rootfile=open(path_results+ '/' + root_file_name, 'w')

    n_nodes = int(node_file.split('-')[1])
    #EJECUCIONES = n_runs con semillas
    for seed_run in range(n_runs):
        seed = n_nodes*10 + seed_run
        #Recogemos los datos de la topología BRITE con semilla de ejecución (seed run)
        if load_limit:
            loads = BRITE_interface.cargas_aleatorias_con_limite(node_file, seed)
        else:
            loads = BRITE_interface.cargas_aleatorias(node_file, seed)

        edges_conf = DataGatherer.getEdges_Config('data/links_config.csv')
        edges = BRITE_interface.BRITEedges(edge_file, edges_conf, seed)
        positions = BRITE_interface.BRITEpositions(node_file)
        root = BRITE_interface.selectMultiRoot(node_file, NUMBER_OF_ROOTS, seed)

        #Creamos el grafos
        G = Graph(0, loads, edges, list(), edges_conf, None, root)

        #ALGORITMO
        G_den2ne_alg = Den2neMultiRoot(G)

        inicio_id = time.time()
        G_den2ne_alg.spread_ids()
        fin_id = time.time()

        #Ahora seleccionamos las IDS por el criterio
        G_den2ne_alg.selectBestIDs(criterion)

        inicio_balance = time.time()
        [total_balance_ideal, abs_flux] = G_den2ne_alg.globalBalance(withLosses=LOSSES[conf_losses], withCap=CAPACITY[conf_losses], withDebugPlot=DEBUG_PLOT, positions=positions, path=path_results)
        fin_balance = time.time()

        tiempo_balance = fin_balance - inicio_balance
        tiempo_id = fin_id - inicio_id

        #Por ahora para los resultados de balance voy a poner la suma de las cargas en todos los roots
        balance_global = 0
        for root in G_den2ne_alg.roots:
            balance_global += total_balance_ideal[root]
        #Escritura de resultados
        #FORMATO: seed_run, balance, abs_flux, time_ID, time_balance
        file.write(str(seed) + ',' + str(balance_global) + ',' + str(abs_flux) + ',' + str(tiempo_id) + ',' + str(tiempo_balance) + '\n')
        rootfile.write(str(seed) + ',' + str(total_balance_ideal[G.root[0]]) + ',' + str(total_balance_ideal[G.root[1]]) + ',' + str(total_balance_ideal[G.root[2]]) + ',' + str(total_balance_ideal[G.root[3]]) + ',' +str(balance_global) + '\n')

    file.close()

if __name__ == "__main__":
    if (len(sys.argv))!=8:
        print('Error, debe introducir: path de los resultados, path de la topología, semilla, criterio, escenario de pérdidas, límite de carga y número ejecuciones')
        print('AYUDA: resultados (path), topología (path), semilla (int[1-10]), criterio (int[0-4]), perdidas (int[0-3]), límite de carga (int[No=0 o Sí=1]), número ejecuciones (int)')
        exit(1)
    test(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
    #test_without_iterations(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
