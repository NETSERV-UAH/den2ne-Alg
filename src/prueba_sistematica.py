#!/usr/bin/python3

from graph.graph import Graph
from den2ne.den2neALG import Den2ne
import sys
import time

def prueba(path, criterio):
    
    """Función que realiza las pruebas sistemáticas y las guarda en un fichero de texto"""

    G = Graph(None, None, None, [], None, path, None)
    datos = dict()
    positions = list()
    with open(path) as file:
        cont = 0
        for linea in file.readlines():
            if cont == 1:
                linea = linea.split()
                datos['nodos'] = linea[4]
                datos['modelo'] = 'ASWaxman'
                datos['node_placement'] = linea[7]
                datos['conectividad'] = linea[9]
                datos['alpha'] = linea[10][:4]
                datos['beta'] = linea[11][:4]
            elif cont >= 4 and cont <= (3 + int(datos['nodos'])):
                linea = linea.split()
                positions.append(dict())
                positions[cont-4]['node'] = linea[0]
                positions[cont-4]['x'] = float(linea[1])
                positions[cont-4]['y'] = float(linea[2])
            cont += 1
    
    #Algoritmo
    inicio = time.time()
    G_den2ne_alg = Den2ne(G)
    inicio_ids = time.time()
    G_den2ne_alg.spread_ids()
    fin_ids = time.time()
    #Ahora seleccionamos las IDS por el criterio
    G_den2ne_alg.selectBestIDs(int(criterio))
    inicio_globalbalance = time.time()
    [total_balance_ideal, abs_flux] = G_den2ne_alg.globalBalance(withLosses=True, withCap=True, withDebugPlot=False, positions=positions, path='results/')
    fin_globalbalance = time.time()
    fin = time.time()

    tiempo = fin - inicio
    tiempo_ids = fin_ids - inicio_ids
    tiempo_globalbalance = fin_globalbalance - inicio_globalbalance

    datos['criterio'] = criterio
    datos['balance_global'] = str(abs(total_balance_ideal))
    datos['abs_flux'] = str(abs_flux)
    datos['tiempo'] = str(tiempo)
    datos['tiempo_ids'] = str(tiempo_ids)
    datos['tiempo_globalbalance'] = str(tiempo_globalbalance)
    datos['archivo'] =  path
    datos['conf_perdidas'] = 'Losses and Capacity'

    #Ahora rellenamos el excel
    with open('ConSemilla.txt', 'a') as file:
       #file.write('Nodos\tModelo\tNode_Placement\tConectividad\tAlpha\tBeta\tCriterio\tConf_Perdidas\tBalance_Global\tFlujo Energetico\tTiempo\tTiempo creando las IDs\tTiempo GlobalBalance\tArchivo\n') #Esta línea es solo para escribir las cabeceras si el fichero no existe
       file.write(datos['nodos'] + '\t' + datos['modelo'] + '\t' + datos['node_placement'] + '\t' + datos['conectividad'] + '\t' + datos['alpha'] + '\t' + datos['beta'] +'\t' + datos['criterio'] + '\t' + datos['conf_perdidas'] + '\t' + datos['balance_global'] +'\t'+ datos['abs_flux'] + '\t' + datos['tiempo'] + '\t' + datos['tiempo_ids'] + '\t' + datos['tiempo_globalbalance'] + '\t' + datos['archivo'] + '\n')

if __name__ == "__main__":
    if (len(sys.argv)!=3):
        print('Error, debe introducir el nombre del fichero .brite y la función objetivo')
        exit(1)
    prueba(sys.argv[1], sys.argv[2])
