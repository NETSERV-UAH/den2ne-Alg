#!/bin/bash

TOPO_TEST='test_topo.py'
# Global PATH vars
RESULT_DIR='./results'
TOPO_DIR='./data/topos'

# Experiment vars
TOPO_NAMES=('barabasi' 'waxman')
#TOPO_NUM_NODES=(10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200)
TOPO_NUM_NODES=$(seq 25 25 200)
TOPO_DEGREES=(2 4 6)
TOPO_SEEDS=(1 2 3 4 5 6 7 8 9 10)
TOPO_CRITERIONS=(0 1 2 3 4 5)	     # Criterio de selección de IDs
TOPO_BEHAVIORAL=(0 1 2 3)	         # Caso ideal (0), Losses (1), Capacity (2), Losses and Capacity (3)

TOPO_LOAD_LIMIT=(0 1)              # Limite de carga (False or True)
TOPO_RUNS=10

echo "[$(date +%T)][INFO] Inicio de las pruebas ... "
echo "[$(date +%T)][INFO] Leyendo topogias del dir: $(pwd)/${TOPO_DIR}"
echo "[$(date +%T)][INFO] Escribiendo resultados en la raiz de las pruebas ${RESULT_DIR}"

# Main loops
for topo_load_limit in ${TOPO_LOAD_LIMIT[@]}
do
    for topo_behave in ${TOPO_BEHAVIORAL[@]}
    do
        for topo_name in ${TOPO_NAMES[@]}
        do
            for topo_num_node in ${TOPO_NUM_NODES[@]}
            do
                for topo_dregree in ${TOPO_DEGREES[@]}
                do
                    for topo_seed in ${TOPO_SEEDS[@]}
                    do
                        for topo_criterion in ${TOPO_CRITERIONS[@]}
                        do 
                            echo "[$(date +%T)][INFO] RUNNING: python3 ${TOPO_TEST} ${RESULT_DIR}/exp_loadLimit_${topo_load_limit}_behavioral_${topo_behave} ${TOPO_DIR}/${topo_name}-${topo_num_node}-${topo_dregree}/seed_${topo_seed}/ ${topo_seed} ${topo_criterion} ${topo_behave} ${topo_load_limit} ${TOPO_RUNS}"
                            python3 ${TOPO_TEST} ${RESULT_DIR}/exp_loadLimit_${topo_load_limit}_behavioral_${topo_behave} ${TOPO_DIR}/${topo_name}-${topo_num_node}-${topo_dregree}/seed_${topo_seed}/ ${topo_seed} ${topo_criterion} ${topo_behave} ${topo_load_limit} ${TOPO_RUNS}
                            sleep 0.25
                        done
                    done
                done
            done
        done
    done
done

echo "[$(date +%T)][INFO] Fin de las pruebas ... "
