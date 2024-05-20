%% plotRangeLoads.m
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha:  20 May 2024

function plotRangeLoads(init, fin)
    
    % Preparamos la matriz de datos 
    data3d = zeros (6,7,fin-init);
    
    
    % Obtenemos los datos de los ficheros csv indicados
    for i=init:1:fin
        data_table = readtable(strcat("csv/outdata_d",num2str(i),".csv"), 'NumHeaderLines',1);
            
        % Pasamos a matriz
        data3d(:,:,i+1) = data_table{:,:};
    end
    
    % Obtenemos la media
    data_avg = mean(data3d(:,2:end,:),3);
    sem = (std(data3d(:,2:end,:), [], 3)/(sqrt(fin-init+1)));
    
    % Pintamos la figura de balance global de potencias
    data_power = data_avg(:, [1 3 5]);
    sem_power = sem(:, [1 3 5]);
    
    h=figure();
    set(gcf,'Position',[100 100 900 700]);
    bar(data_power,1,'grouped','FaceColor','flat'), hold on;
    
    % Errors bars 
    ngroups = size(data_power, 1);
    nbars = size(data_power, 2);
    threshhold = 0.2;

    % Calculate the width for each bar group
    groupwidth = min(0.8, nbars/(nbars + 1.5));

    for i = 1:nbars
        % Calculate center of each bar
        x = (1:ngroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*nbars);
        errorbar(x, data_power(:,i), sem_power(:,i) + threshhold, 'k', 'linestyle', 'none');
    end

    grid on
    title("Balance de potencias global en promedio")
    ylabel("Potencia (kW)")
    legend("Ideal", "Con perdidas", "Con perdidas y capacidades", 'Location', 'southoutside', 'NumColumns', 3)
    set(gca,'XTickLabel', {'Criterion 1' 'Criterion 2' 'Criterion 3' 'Criterion 4' 'Criterion 5' 'Criterion 6'});
    hold off;
    set(h,'Units','Inches');
    pos = get(h,'Position');
    set(h,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
    print(h,'fig/powerBalance_global','-dpdf','-r0')

    % Pintamos la figura de balance absoluto de potencia
    data_power_abs = data_avg(:, [2 4 6]);
    sem_power_abs = sem(:, [2 4 6]);
    
    h=figure();
    set(gcf,'Position',[100 100 900 700]);
    b2 = bar(data_power_abs,1,'grouped','FaceColor', 'flat'); hold on;
    
    for k = 1:size(data_power_abs,2)
        b2(k).CData = k;
    end
    
    for i = 1:nbars
        % Calculate center of each bar
        x = (1:ngroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*nbars);
        errorbar(x, data_power_abs(:,i), sem_power_abs(:,i), 'k', 'linestyle', 'none');
    end
    
    grid on
    title("Valor absoluto del flujo de potencias en promedio")
    ylabel("Potencia (kW)")
    legend("Ideal", "Con perdidas", "Con perdidas y capacidades", 'Location', 'southoutside', 'NumColumns', 3)
    set(gca,'XTickLabel', {'Criterion 1' 'Criterion 2' 'Criterion 3' 'Criterion 4' 'Criterion 5' 'Criterion 6'}); 
    hold off;
    set(h,'Units','Inches');
    pos = get(h,'Position');
    set(h,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
    print(h,'fig/powerAbsflux_global','-dpdf','-r0')
    
    % Pintamos las perdidas por enlaces - switches
    data_loss = data_power(:,1) - data_power(:,2);
    sem_loss = (std(data3d(:,2,:) - data3d(:,4,:), [], 3)/(sqrt(fin-init+1)));
    
    h=figure();
    set(gcf,'Position',[100 100 900 700]);
    bar(data_loss.', 0.5, 'FaceColor', [0.9290 0.6940 0.1250]), hold on;
    errorbar(data_loss.', sem_loss.', 'k', 'linestyle', 'none');
    grid on
    title("Perdidas  por propagación e inserción de switches en promedio")
    ylabel("Potencia (kW)")
    set(gca,'XTickLabel', {'Criterion 1' 'Criterion 2' 'Criterion 3' 'Criterion 4' 'Criterion 5' 'Criterion 6'});
    hold off;
    set(h,'Units','Inches');
    pos = get(h,'Position');
    set(h,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
    print(h,'fig/powerLoss_global','-dpdf','-r0')
    
    % Pintamos las perdidas por exceso de la capacidad
    data_loss_Cap = data_power(:,2) - data_power(:,3);
    sem_loss_Cap = (std(data3d(:,4,:) - data3d(:,6,:), [], 3)/(sqrt(fin-init+1)));
    
    h=figure();
    set(gcf,'Position',[100 100 900 700]);
    bar(data_loss_Cap.', 0.5, 'FaceColor', [0.6350 0.0780 0.1840]), hold on;
    errorbar(data_loss_Cap.', sem_loss_Cap.', 'k', 'linestyle', 'none');
    grid on
    title("Perdidas por exceso en la capacidad del enlace en promedio")
    ylabel("Potencia (kW)")
    set(gca,'XTickLabel', {'Criterion 1' 'Criterion 2' 'Criterion 3' 'Criterion 4' 'Criterion 5' 'Criterion 6'});
    hold off;
    set(h,'Units','Inches');
    pos = get(h,'Position');
    set(h,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
    print(h,'fig/powerLossCap_global','-dpdf','-r0')
    
end