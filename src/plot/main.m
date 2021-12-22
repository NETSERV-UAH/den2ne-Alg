%% Fichero Main para dibijar todos los resultados 
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 22 Dic 2021
clc
close all
clear variables

%% Global Vars

% Paths
PATH_RESUTLS_DIR = '../results/';
PATH_RESUTLS_MAT_DATA = './';
PATH_OUTPUT_FIG_PDF = './fig/';

% Name 
NAME_RESUTLS = 'results_v3';

% Script flags
SAVE_FIG = true;

% Experiments vars
TOPO_NAMES = ["barabasi" , "waxman"];
TOPO_NUM_NODES = 10:10:200;
TOPO_DEGREES = 2:2:6;
TOPO_CRITERIONS = 0:1:5;
TOPO_BEHAVIORAL = 0:1:3;
TOPO_LOAD_LIMIT = 0:1:1;
TOPO_SEEDS = 1:1:10;
TOPO_RUNS = 1:1:10;

% Plot vars
PLOT_MEAS = [0 1 2 3];  % Seed(0)
                        % Global balance (1)
                        % Abs flux(2)
                        % IDs time (3)
                        % Global balance time(4)


%% Main block

% First of all, we have to check if we have already parse the data into a
% *.mat file..
if isfile(strcat(PATH_RESUTLS_MAT_DATA, NAME_RESUTLS,'.mat'))
    % File exist.
    load(strcat(PATH_RESUTLS_MAT_DATA, NAME_RESUTLS,'.mat'));
else
    % File does not exist, then we have to generate it
    data = gather_experiments(strcat(PATH_RESUTLS_DIR, NAME_RESUTLS), TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_BEHAVIORAL, TOPO_LOAD_LIMIT, TOPO_SEEDS, TOPO_RUNS);

    % And, we are going to save it in order to speed up future plots
    save(strcat(PATH_RESUTLS_MAT_DATA, NAME_RESUTLS,'.mat'), "data");
end


% Second, we are going to plot all the results
for limit_index=0:length(TOPO_LOAD_LIMIT)-1
    for behavioral_index=0:length(TOPO_BEHAVIORAL)-1
        plot_experiments(data{load_limit,behavioral}, PLOT_MEAS, TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_BEHAVIORAL, TOPO_LOAD_LIMIT, TOPO_SEEDS, TOPO_RUNS);
    end
end