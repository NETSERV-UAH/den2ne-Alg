%% Plotter.m
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 20 May 2024  
clc
close all
clear global


%% Main

% First we have to indicate where are the loads distribution
PATH_LOADS_DIST = "../../data/";

% Lets read the csv with all the info
data_table = readtable(strcat(PATH_LOADS_DIST,"load_v2.csv"), 'NumHeaderLines',1);
    
% Parse from table to matrix 
data = data_table{:,2:end};

% Flatten the matrix to a single vector
data_vector = data(:);

% Plot histogram
h=figure();
set(gcf,'Position',[100 100 900 700]);
histogram(data_vector);
grid on
title('Distribution of end node load profiles','FontSize',16);
xlabel('Power (kW)');
ylabel('Frequency');
set(h,'Units','Inches');
pos = get(h,'Position');
set(h,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
strPath = strcat('fig/', 'loadsHist');
print(h,strPath,'-dpdf','-r0')