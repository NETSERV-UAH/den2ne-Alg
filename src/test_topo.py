#!/usr/bin/python3

from graph.graph import Graph
from den2ne.den2neALG import Den2ne
import dataCollector.brite_intf as BRITE_interface
import sys
import time

#Definimos la configuración de pérdidas
CONF_LOSSES = ['Ideal', 'Losses', 'Capacity', 'Losses and Capacity']
LOSSES = [False, True, False, True]
CAPACITY = [False, False, True, True]
#Variables para los path
DEBUG_PLOT = False
RESULTS_PATH = 'results/'
PRUEBAS_DIR = 'Pruebas/'
SIN_LIMITE = 'Sin_limite.txt'
CON_LIMITE = 'Con_limite.txt'

def prueba(path, criterio, seed, conf_losses, cargas_con_limite):
    
    """Función que realiza las pruebas sistemáticas y las guarda en un fichero de texto"""

    node_file = path + 'Nodos.txt'
    edge_file = path + 'Enlaces.txt'
    pruebas_path = PRUEBAS_DIR + (CON_LIMITE if int(cargas_con_limite) else SIN_LIMITE)    #Donde guardamos los resultados

    #Para luego guardar en el txt
    datos = dict()

    #Recogemos los datos de la topología BRITE
    loads = BRITE_interface.cargas_aleatorias_con_limite(node_file, seed) if int(cargas_con_limite) else BRITE_interface.cargas_aleatorias(node_file, seed)
    edges_conf = BRITE_interface.conf_edges_aleatorio(seed)
    switches = list()
    edges = BRITE_interface.BRITEedges(edge_file, edges_conf, seed)
    positions = BRITE_interface.BRITEpositions(node_file)
    root = BRITE_interface.selectRoot(node_file, seed)
    
    #Creamos el grafo 
    G = Graph(0, loads, edges, switches, edges_conf, None, root)
    
    #Algoritmo
    G_den2ne_alg = Den2ne(G)
    G_den2ne_alg.spread_ids()
    #Ahora seleccionamos las IDS por el criterio
    G_den2ne_alg.selectBestIDs(int(criterio))
    inicio_globalbalance = time.time()
    [total_balance_ideal, abs_flux] = G_den2ne_alg.globalBalance(withLosses=LOSSES[int(conf_losses)], withCap=CAPACITY[int(conf_losses)], withDebugPlot=DEBUG_PLOT, positions=positions, path=RESULTS_PATH)
    fin_globalbalance = time.time()

    tiempo_globalbalance = fin_globalbalance - inicio_globalbalance

    #Almacenamos los datos para escribirlo en un fichero
    datos['modelo'] = node_file.split('/')[-5]
    datos['nodos'] = node_file.split('/')[-4]
    datos['grado'] = node_file.split('/')[-3]
    datos['topo_seed'] = node_file.split('/')[-2]
    datos['load_seed'] = str(seed)
    datos['conf_perdidas'] = CONF_LOSSES[int(conf_losses)]
    datos['criterio'] = criterio
    datos['balance_global'] = str(abs(total_balance_ideal)) #¿Con valor absoluto o sin valor absoluto?
    datos['abs_flux'] = str(abs_flux)
    datos['tiempo_globalbalance'] = str(tiempo_globalbalance)

    #Ahora rellenamos el txt
    with open(pruebas_path, 'a') as file:
       file.write(datos['modelo'] + '\t' + datos['nodos'] + '\t' + datos['grado'] + '\t' + datos['topo_seed'] + '\t' + datos['load_seed'] + '\t' + datos['conf_perdidas'] +'\t' + datos['criterio'] + '\t' + datos['balance_global'] + '\t'+ datos['abs_flux'] + '\t' + datos['tiempo_globalbalance'] + '\n')

if __name__ == "__main__":
    if (len(sys.argv)!=6):
        print('Error, debe introducir el directorio donde se encuentra la topología, criterio, semilla, configuración de pérdidas y la configuracion de cargas\n')
        exit(1)
    prueba(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
