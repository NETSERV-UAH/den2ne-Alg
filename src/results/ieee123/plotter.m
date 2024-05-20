%% Plotter.m
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 20 May 2024
clc
close all
clear varibles

%% Main

% Pintamos las graficas correspondientes al balance global de potencias, el
% valor absoluto del flujo de potencia, perdias por enlaces - switches,
% perdidas por superar el valor máximo de la configuración de un enlace 
plotDeltaLoads(0)

% Pintamos el valor medio de todos los intantes de carga 
plotRangeLoads(0, 95)