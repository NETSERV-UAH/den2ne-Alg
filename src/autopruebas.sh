#!/bin/bash
#Script para automatizar las pruebas

for r in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
	for k in 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200
	do 
		for i in 8 9 10 11 12 13 14 15 16 17 18 19
		do
			for j in 0 1 2 3 4 5
			do
				python3 prueba_sistematica.py brite/ps${k}nodos$i.brite $j
			done
		done
	done
done
