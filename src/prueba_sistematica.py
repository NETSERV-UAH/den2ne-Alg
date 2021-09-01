#!/usr/bin/python3

from graph.graph import Graph
from den2ne.den2neALG import Den2ne
import sys
import time

def prueba(path, criterio):
    G = Graph(None, None, None, [], None, path, None)
    datos = dict()
    positions = list()
    with open(path) as file:
        cont = 0
        for linea in file.readlines():
            if cont == 1:
                linea = linea.split()
                datos['nodos'] = linea[4]
                datos['modelo'] = linea[3].split(')')[0]
                datos['node_placement'] = linea[7]
                datos['conectividad'] = linea[8]
                datos['alpha'] = linea[9][:4]
                datos['beta'] = linea[10][:4]
            elif cont >= 4 and cont <= (3 + int(datos['nodos'])):
                linea = linea.split()
                positions.append(dict())
                positions[cont-4]['node'] = linea[0]
                positions[cont-4]['x'] = int(linea[1])
                positions[cont-4]['y'] = int(linea[2])
            cont += 1
    
    #Algoritmo
    inicio = time.time()
    G_den2ne_alg = Den2ne(G)
    G_den2ne_alg.spread_ids()
    #Ahora seleccionamos las IDS por el criterio
    G_den2ne_alg.selectBestIDs(int(criterio))
    [total_balance_ideal, abs_flux] = G_den2ne_alg.globalBalance(withLosses=False, withCap=False, withDebugPlot=False, positions=positions, path='results/')
    fin = time.time()

    path_json = path.split('/')[-1]
    path_json = path_json.split('.')[0]
    path_json = 'resultado_pruebas/' + path_json + '_' + criterio + '.json'
    #G.saveGraph(path_json)
    tiempo = fin - inicio

    datos['criterio'] = criterio
    datos['balance_global'] = str(abs(total_balance_ideal))
    datos['abs_flux'] = str(abs_flux)
    datos['tiempo'] = str(tiempo)
    datos['archivo'] =  path
    #Ahora rellenamos el excel
    with open('pruebas2.txt', 'a') as file:
        #file.write('Nodos\tModelo\tNode_Placement\tConectividad\tAlpha\tBeta\tCriterio\tBalance_Global\tFlujo Energetico\tTiempo\tArchivo\n')
        file.write(datos['nodos'] + '\t' + datos['modelo'] + '\t' + datos['node_placement'] + '\t' + datos['conectividad'] + '\t' + datos['alpha'] + '\t' + datos['beta'] + '\t' + datos['criterio'] + '\t' + datos['balance_global'] +'\t'+ datos['abs_flux'] + '\t' + datos['tiempo'] + '\t' + datos['archivo'] + '\n')

if __name__ == "__main__":
    if (len(sys.argv)!=3):
        print('Error, debe introducir el nombre del fichero .brite y la función objetivo')
        exit(1)
    prueba(sys.argv[1], sys.argv[2])
