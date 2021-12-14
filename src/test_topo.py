#!/usr/bin/python3
from graph.graph import Graph
from den2ne.den2neALG import Den2ne
import dataCollector.brite_intf as BRITE_interface
import sys
import time
import os
import datetime

#Variables globales
LOSSES = [False, True, False, True]
CAPACITY = [False, False, True, True]
DEBUG_PLOT = False

def prueba(path_results, path_topology, topo_seed, criterion, conf_losses, load_limit, n_runs):

    """
    Obj: Realizar las pruebas sistemáticas y guardar los resultados en un fichero de texto.
    ### PARÁMETROS ###
    - path_results (path) -> Path del directorio en el que se almacenarán los resultados (empezado por ./) Ejemplo: ./results
    - path_topology (path) -> Path del directorio donde se encuentran los ficheros de la topología en especifico (empieza por ./) Ejemplo: ./data/topos/waxman-30-4/seed_5/
    - topo_seed (int[1,10])-> Semilla de la topología. Va implícita en path_topology pero para evitar buscar (Tienen que coincidir) Ejemplo: 5 (por seed_5)
    - criterion (int[0,4])-> Índice del criterio elegido de la lista de criterios que se encuentra en ./den2ne/den2neALG.py
    - conf_losses (int[0,3])-> Índice de elección del escenario de pérdidas. Modifica valores de withLosses y withCap. 4 posibles escenarios
    - load_limit (int[0,1])-> Existencia o no de límite de carga: (Si=1-No=0)
    - n_runs (int) -> Número de ejecuciones que servirán para fijar la semilla de ejecución
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
    print('[' + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + '][INFO] Fichero de resultados generado: ' + path_results+ '/' + file_name)  #./results/topo_x_y/outdata_seed_%d_c_%s.csv
    file=open(path_results+ '/' + file_name, 'w')

    #EJECUCIONES = n_runs con semillas
    for seed_run in range(n_runs):
        #Recogemos los datos de la topología BRITE con semilla de ejecución (seed run)
        if load_limit:
            loads = BRITE_interface.cargas_aleatorias_con_limite(node_file, seed_run)
        else:
            loads = BRITE_interface.cargas_aleatorias(node_file, seed_run)

        edges_conf = BRITE_interface.conf_edges_aleatorio(seed_run)
        edges = BRITE_interface.BRITEedges(edge_file, edges_conf, seed_run)
        positions = BRITE_interface.BRITEpositions(node_file)
        root = BRITE_interface.selectRoot(node_file, seed_run)

        #Creamos el grafos
        G = Graph(0, loads, edges, list(), edges_conf, None, root)

        #ALGORITMO
        G_den2ne_alg = Den2ne(G)

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

        #Escritura de resultados
        #FORMATO: seed_run, balance, abs_flux, time_ID, time_balance
        file.write(str(seed_run) + ',' + str(total_balance_ideal) + ',' + str(abs_flux) + ',' + str(tiempo_id) + ',' + str(tiempo_balance) + '\n')

    file.close()

if __name__ == "__main__":
    if (len(sys.argv))!=8:
        print('Error, debe introducir: path de los resultados, path de la topología, semilla, criterio, escenario de pérdidas, límite de carga y número ejecuciones')
        print('AYUDA: resultados (path), topología (path), semilla (int[1-10]), criterio (int[0-4]), perdidas (int[0-3]), límite de carga (int[No=0 o Sí=1]), número ejecuciones (int)')
        exit(1)
    prueba(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
