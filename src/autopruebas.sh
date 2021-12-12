#!/bin/bash
#Script para automatizar las pruebas

PRUEBAS_DIR="Pruebas"
SIN_LIMITE="Sin_limite.txt"
CON_LIMITE="Con_limite.txt"
ORDEN_PARAMETROS="Modelo\tNodos\tGrado\tSemilla Topologia\tSemilla cargas\tConfiguracion Perdidas\tCriterio\tBalance Global\tFlujo Energetico\tTiempo GlobalBalance"
PATH_BASE="../../brite2/Archivos_brite/" #Path para llegar a las topologías BRITE

cargas_con_limite=(0 1)	#Pruebas sin limite global (0), Pruebas con limite global de cargas (1)
conf_perdidas=(0 1 2 3)	#Caso ideal (0), Losses (1), Capacity (2), Losses and Capacity (3)
seed=(1 2 3 4 5 6 7 8 9 10)	#Semilla para cargas
criterion=(0 1 2 3 4 5)	#Criterio de selección de IDs
model=("Waxman" "Barabasi")
node=(10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200)
degree=(2 4 6)
topo_seed=(1 2 3 4 5 6 7 8 9 10)

#Primero creamos del directorio de pruebas
mkdir -p $PRUEBAS_DIR
echo -e $ORDEN_PARAMETROS > $PRUEBAS_DIR/$SIN_LIMITE 
echo -e $ORDEN_PARAMETROS > $PRUEBAS_DIR/$CON_LIMITE 

for c_cargas in ${cargas_con_limite[@]}
do
    for c_perdidas in ${conf_perdidas[@]}
    do
        for semilla in ${seed[@]}
        do
            for criterio in ${criterion[@]}
            do
                for modelo in ${model[@]}
                do 
                    for nodo in ${node[@]}
                    do 
                        for grado in ${degree[@]}
                        do
                            for semilla_topo in ${topo_seed[@]}
                            do
                                path=${PATH_BASE}${modelo}/${nodo}/${grado}/${semilla_topo}/
                                python3 prueba_sistematica.py $path $criterio $semilla $c_perdidas $c_cargas
                            done
                        done
                    done
                done
            done
        done
    done
done
