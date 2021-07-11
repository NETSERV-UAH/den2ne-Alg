%% plotDeltaLoads.m
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 11 Jul 2021

function plotDeltaLoads(delta)

    % Obtenemos los datos del fichero csv indicado
    data_table = readtable(strcat("ieee123/csv/outdata_d",num2str(delta),".csv"), 'NumHeaderLines',1);
    
    % Pasamos a matriz
    data = data_table{:,:};
    
    % Pintamos la figura de balance global de potencias
    data_power = data(:, [2 4 6]);
    figure();
    set(gcf,'Position',[100 100 900 700]);
    bar(data_power,1,'grouped','FaceColor','flat');
    grid on
    title("Balance de potencias global - Instante \delta_{" + num2str(delta) + "}")
    ylabel("Potencia (kW)")
    legend("Ideal", "Con perdidas", "Con perdidas y capacidades", 'Location', 'southoutside', 'NumColumns', 3)
    set(gca,'XTickLabel', {'Criterion 1' 'Criterion 2' 'Criterion 3' 'Criterion 4' 'Criterion 5' });

    % Pintamos la figura de balance absoluto de potencia
    data_power_abs = data(:, [3 5 7]);
    figure();
    set(gcf,'Position',[100 100 900 700]);
    b2 = bar(data_power_abs,1,'grouped','FaceColor', 'flat');
    for k = 1:size(data_power_abs,2)
        b2(k).CData = k;
    end
    grid on
    title("Valor absoluto del flujo de potencias - Instante \delta_{" + num2str(delta) + "}")
    ylabel("Potencia (kW)")
    legend("Ideal", "Con perdidas", "Con perdidas y capacidades", 'Location', 'southoutside', 'NumColumns', 3)
    set(gca,'XTickLabel', {'Criterion 1' 'Criterion 2' 'Criterion 3' 'Criterion 4' 'Criterion 5' });
    
    % Pintamos las perdidas por enlaces - switches
    data_loss = data_power(:,1) - data_power(:,2);
    figure();
    set(gcf,'Position',[100 100 900 700]);
    bar(data_loss.', 0.5, 'FaceColor', [0.9290 0.6940 0.1250])
    grid on
    title("Perdidas  por propagación e inserción de switches - Instante \delta_{" + num2str(delta) + "}")
    ylabel("Potencia (kW)")
    set(gca,'XTickLabel', {'Criterion 1' 'Criterion 2' 'Criterion 3' 'Criterion 4' 'Criterion 5' });
    
    % Pintamos las perdidas por exceso de la capacidad
    data_loss_Cap = data_power(:,2) - data_power(:,3);
    figure();
    set(gcf,'Position',[100 100 900 700]);
    bar(data_loss_Cap.', 0.5, 'FaceColor', [0.6350 0.0780 0.1840])
    grid on
    title("Perdidas por exceso en la capacidad del enlace - Instante \delta_{" + num2str(delta) + "}")
    ylabel("Potencia (kW)")
    set(gca,'XTickLabel', {'Criterion 1' 'Criterion 2' 'Criterion 3' 'Criterion 4' 'Criterion 5' });

    
end

