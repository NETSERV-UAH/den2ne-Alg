%% loadsGenerator.m
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 6 Jun 2024  
clc
close all
clear variables

%% Global Vars 
PATH_LOADS_PROFILES = "";


%% Main

% First we are going to load the data

% Check if generacion.mat exists and load it
generacion_file = strcat(PATH_LOADS_PROFILES, "generacion.mat");

if exist(generacion_file, 'file')
    load(generacion_file);
    disp('generacion.mat loaded successfully');
else
    disp('generacion.mat does not exist');
end

% Check if consumos.mat exists and load it
consumos_file = strcat(PATH_LOADS_PROFILES, "consumos.mat");

if exist(consumos_file, 'file')
    load(consumos_file);
    disp('consumos.mat loaded successfully');
else
    disp('consumos.mat does not exist');
end

% Second, let's plot 24h consume vs generation
gen_vector = sum(perfiles_generacion,1);
con_vector = sum(perfiles_consumo,1);


% We have to check that con_vector and gen_vector have 96 points (24h in 15min slot times => 96 deltas)
if length(con_vector) ~= 96 || length(gen_vector) ~= 96
    error('Wrong dimension in/or con_vector/gen/vector.');
end

% Calculate the balance
balance_vector = gen_vector - con_vector;

% Create the time vector to plot easily
time_vector = linspace(0, 24, 96);

% Let's plot :)
figure();

% con
subplot(3, 1, 1);
plot(time_vector, con_vector, 'b', 'LineWidth', 1.5);
title('Consumption each 15 minutes');
xlabel('Time of the day');
ylabel('Consumption (kW)');
grid on;

% gen
subplot(3, 1, 2);
plot(time_vector, gen_vector, 'g', 'LineWidth', 1.5);
title('Generation each 15 minutes');
xlabel('Time of the day');
ylabel('Generation (kW)');
grid on;

% balance
subplot(3, 1, 3);
plot(time_vector, balance_vector, 'r', 'LineWidth', 1.5);
title('Balance (Generation - Consumption)');
xlabel('Time of the day');
ylabel('Balance (kW)');
grid on;

sgtitle('Consumption, Generation and Balance within 24 hours');


% Third, lets plot uG needs
figure();
hold on;
area(time_vector, balance_vector .* (balance_vector >= 0), 'FaceColor', 'green', 'EdgeColor', 'none');
area(time_vector, balance_vector .* (balance_vector < 0), 'FaceColor', 'red', 'EdgeColor', 'none');
plot(time_vector, balance_vector, 'k--', 'LineWidth', 1.5)
yline(0, 'k', 'LineWidth', 3);
title('Balance (Generation - Consumption) over 24 Hours');
xlabel('Time of Day (hours)');
ylabel('Balance (kW)');
xlim([0,24]);
ylim([-800,500]);
legend({'Generation (Positive Balance)', 'Consumption (Negative Balance)', 'Balance Line'}, 'Location', 'best');
grid on;
hold off;

%% Last, but not the least, generate the *.csv

perfiles_balance = perfiles_generacion - perfiles_consumo;

% Let's norm the matrix
perfiles_balance_max_abs = max(abs(perfiles_balance),[],'all');
perfiles_balance_norm = perfiles_balance / perfiles_balance_max_abs;

% Csv name
output_file = 'loads_v2_norm.csv';

% Lets create the header 
num_intervals = 96; 
time_intervals = 15:15:(num_intervals*15);
header = ['Bus_no', arrayfun(@num2str, time_intervals, 'UniformOutput', false)];

% Lets add bus_no
bus_numbers = (1:size(perfiles_balance_norm, 1))'; 
perfiles_balance_with_bus = [bus_numbers perfiles_balance_norm];

% Let's remove the row with zeros 
row_to_delete = [3,8,13,14,15,18,21,23,25,26,27,36,40,44,54,57,61,67,72,78,81,89,91,93,97,101,105,108,110];
perfiles_balance_with_bus_wout_zeros = perfiles_balance_with_bus;
perfiles_balance_with_bus_wout_zeros(row_to_delete,:) = [];


% Escribir la cabecera en el archivo
fileID = fopen(output_file, 'w');
fprintf(fileID, '%s\n', strjoin(header, ','));
fclose(fileID);

% Escribir los datos de la matriz en el archivo CSV
writematrix(perfiles_balance_with_bus_wout_zeros, output_file, 'WriteMode', 'append');

% Confirmación
disp(['CSV File created: ', output_file]);