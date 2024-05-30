%% loadsGenerator.m
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 30 May 2024  
clc
close all
clear variables

%% Main
Vd = 400; % V
coef_R = [0.272 0.78 1.91]; % ohm/km
dist = [300 500 800]/3.28084; % m 
Pin = 0.01:0.001:1000; % kW

% Conversión de distancias a km
dist_km = dist / 1000; % m a km

% Número de subplots
numCoefR = length(coef_R);
numDist = length(dist_km);

% Crear figura
figure;

% Índice para subplots
plotIndex = 1;

for i = 1:numCoefR
    for j = 1:numDist
        % Calcular pérdidas
        r_eff = coef_R(i) * dist_km(j); % ohm
        losses = ((r_eff / Vd^2) * (Pin * 1000).^2) / 1000; % kW

        % Crear subplot
        subplot(numCoefR, numDist, plotIndex);
        plot(Pin, losses);
        title(['coef\_R = ', num2str(coef_R(i)), ', dist = ', num2str(dist(j) * 3.28084), ' ft']);
        xlabel('P_{in} (kW)');
        ylabel('Losses (kW)');
        ylim([0 3000])
        grid on;

        % Incrementar el índice de subplots
        plotIndex = plotIndex + 1;
    end
end
