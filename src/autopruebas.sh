#!/bin/bash
#Script para automatizar las pruebas

for r in 1 2 3 4 5 6 7 8 9 10 11 12 13
do
	for i in 0 1 2 3 4 5
	do
		for j in 0 1 2 3 4 5
		do
			python3 prueba_sistematica.py brite/ps20nodos$i.brite $j
		done
	done
done
