%% Función para pintar datos de un experimento
%
%   [+] Autores: David Hernández Puerta <d.hernandezp@edu.uah.es>
%                Javier Díaz Fuentes <j.diazf@edu.uah.es>
%                David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 22 Dic 2021

function plot_experiments(data_exp, PLOT_MEAS, TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_BEHAVIORAL, TOPO_LOAD_LIMIT, TOPO_SEEDS, TOPO_RUNS) 
    
      subplot = @(m,n,p) subtightplot (m, n, p, [0.075 0.075], [0.32 0.02], [0.07 0.04]); 
    %%Opciones para las graficas
        line_size = 1.3;
    %nombres para las graficas
        criterio = ["Number Hops" "Distance" ,"Power Balance", "Power Balance with Losses", "Link Losses", "Power Balance Weighted"];
        title_column= ["Barabasi", "Waxman"];
        title_row = ["Degree 2", "Degree 4", "Degree 6"];
    %Tamaños
        marker = ["-o", "--+", ":*", "-.d","-x", "--s"];
    %eje y
        y_min= -55;
        y_max= 25;
        y_jumps = 20;
    %eje x
        num_ticks_x = (100:10:200);
        name_ticks_x = {'100',' ','120',' ','140',' ','160',' ','180',' ','200'};
    %tamaño del marcador del error bar
        Marker_Size = 6;
            
    %%Caracteristicas de la hoja pdf que vamos usar para guardar las
    %%gráficas
        position_windows = [2 2 20 2];
        pos_text = [0.075 0.55 1 0];
        size_titles = 8;
        size_axis = 8;
        size_legends = 7;
        paper_size = [18 20]; %[10.42 19];
        paper_position = [0.25 0 14-0.25 15.99];
        pos_legend = [0.53 0.11 0 0]; %[0.5 0.5 0 0];
    %generamos la hoja del pdf
        fig=figure('Name', sprintf('Grafica_%s.pdf', titulo));
        fig.PaperOrientation='landscape';
        fig.PaperSize=paper_size;
        fig.Units = 'centimeters';
        fig.PaperPosition = paper_position;
    
    %Obtenemos los datos para graficar 
        [medias_modelo_grado_criterio_nodo, int_conf_modelo_grado_criterio_nodo] = calcular_estadistica(datos);
    
    %variables de estado
        %tipo_repres=4;
        number_subplot = 1;
        Temporal = 1;

    for degree=1:3
        for model=1:2
            subplot(3,2,number_subplot);
            %figure
            hold on;
            %%generamos el plot con los intervalos de confianza
            for criteria=1:6
                plot ((100:10:200), medias_modelo_grado_criterio_nodo{model}{degree}{criteria}(10:20,tipo_repres),marker(criteria),...
                    'LineWidth',line_size, 'MarkerSize', Marker_Size);
                errorbar((100:10:200), medias_modelo_grado_criterio_nodo{model}{degree}{criteria}(10:20,tipo_repres),...
                    int_conf_modelo_grado_criterio_nodo{model}{degree}{criteria}(10:20,tipo_repres)',".",'LineWidth',...
                    1, 'MarkerSize', Marker_Size);
            end
            %%modificamos las condiciones gráficas del plot
            xticks(num_ticks_x);
            xticklabels(name_ticks_x);
            if tipo_repres ==2
                ylim([y_min y_max]);
                yticks(y_min:y_jumps:y_max)
            end
            grid on;
            box on;
            
            if (number_subplot == 1 || number_subplot == 3 || number_subplot == 5)
                if tipo_repres == 2 
                    ylabel(sprintf("Degree %d\newline Power (kW)",degree*2));
                else
                    ylabel(sprintf("Degree %d\newline Time (ms)",degree*2));
                end
            end
            
            if (number_subplot == 1 || number_subplot == 2)
                title(title_column(model));
            end

            if(number_subplot == 5 || number_subplot == 6)
                xlabel ("Number of nodes");
            end
            
            hold off
            number_subplot = number_subplot+1;
        end
    end
    % Get handles to center subplots

    %legend( criterio,'location', 'northwest');
    %sgtitle(titulo, "Interpreter", "none");

    %%leyenda
    h_legend=legend(criterio, 'location','best');
    set(h_legend,'FontSize',size_legends);
    set(h_legend,'position',pos_legend);
    if tipo_repres ==2
        format='%s/balance_%s.pdf';
        print(fig,sprintf(format, path, titulo),'-dpdf','-fillpage');
    elseif tipo_repres == 4
        format='%s/time_ID_%s.pdf';
        print(fig,sprintf(format, path, titulo),'-dpdf','-fillpage');
    else
        format='%s/time_balance_%s.pdf';
        print(fig,sprintf(format, path, titulo),'-dpdf','-fillpage');
    end
end

