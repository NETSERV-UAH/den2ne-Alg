%% Función para pintar datos de un experimento
%
%   [+] Autores: David Hernández Puerta <d.hernandezp@edu.uah.es>
%                Javier Díaz Fuentes <j.diazf@edu.uah.es>
%                David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 22 Dic 2021

function plot_experiments(data_exp, title, PLOT_MEAS, TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_SEEDS) 
        
    for plot_meas_index=0:length(PLOT_MEAS)-1
        % Init subplot
        subplot = @(m,n,p) subtightplot (m, n, p, [0.075 0.075], [0.32 0.02], [0.07 0.04]); 
        
        % Opciones para las graficas
        line_size = 1.3;

        % Cat title
        title_names =  ["Seed", "Global balance", "Abs flux", "IDs time","Global balance time"];
        title = strcat(title, " - ", title_names(PLOT_MEAS(plot_meas_index+1)+1));
        
        % Labels
        criterio = ["Number Hops" "Distance" ,"Power Balance", "Power Balance with Losses", "Link Losses", "Power Balance Weighted"];
        title_column= ["Barabasi", "Waxman"];
        marker = ["-o", "--+", ":*", "-.d","-x", "--s"];
        
        % Y axis
        y_min= -55;
        y_max= 25;
        y_jumps = 20;
        
        % X axis
        num_ticks_x = (100:10:200);
        name_ticks_x = {'100',' ','120',' ','140',' ','160',' ','180',' ','200'};
        
        % Error bar size
        Marker_Size = 6;
                
        % PDF specs
        size_legends = 7;
        paper_size = [18 20];
        paper_position = [0.25 0 14-0.25 15.99];
        pos_legend = [0.53 0.11 0 0]; 
        
        % Generate PDF file
        fig=figure('Name', sprintf('plot_%s.pdf', title));
        fig.PaperOrientation='landscape';
        fig.PaperSize=paper_size;
        fig.Units = 'centimeters';
        fig.PaperPosition = paper_position;
        
        % Get stats 
        [mean_model_grade_criterion_node, conf_int_model_grade_criterion_node] = statistics(data_exp,  TOPO_NAMES, TOPO_NUM_NODES, ...
                                                                                            TOPO_DEGREES, TOPO_CRITERIONS, TOPO_SEEDS);
        
        % Get rid of the current subplot
        number_subplot = 1;
    
    
        for degree_index=0:length(TOPO_DEGREES)-1
            for model_index=0:length(TOPO_NAMES)-1
               
                % Subplot init 
                subplot(3,2,number_subplot);
                hold on;
                
                % Plot all criteria 
                for criteria_index=0:length(TOPO_CRITERIONS)-1
                    plot ((100:10:200), mean_model_grade_criterion_node{model_index+1}{degree_index+1}{criteria_index+1}(10:20,PLOT_MEAS(plot_meas_index+1)+1),marker(criteria_index+1),...
                        'LineWidth',line_size, 'MarkerSize', Marker_Size);
                    errorbar((100:10:200), mean_model_grade_criterion_node{model_index+1}{degree_index+1}{criteria_index+1}(10:20,PLOT_MEAS(plot_meas_index+1)+1),...
                        conf_int_model_grade_criterion_node{model_index+1}{degree_index +1}{criteria}(10:20,PLOT_MEAS(plot_meas_index+1)+1)',".",'LineWidth',...
                        1, 'MarkerSize', Marker_Size);
                end
    
                % Adjust the curr subplot
                xticks(num_ticks_x);
                xticklabels(name_ticks_x);
                if (PLOT_MEAS(plot_meas_index+1) == 1 || PLOT_MEAS(plot_meas_index+1) == 2) 
                    ylim([y_min y_max]);
                    yticks(y_min:y_jumps:y_max)
                end
    
                % Set grid
                grid on;
                box on;
                
                if (number_subplot == 1 || number_subplot == 3 || number_subplot == 5)
                    if PLOT_MEAS(plot_meas_index+1) == 0
                        ylabel(sprintf("Degree %d\newline Seed",(degree_index +1)*2));
                    elseif (PLOT_MEAS(plot_meas_index+1) == 1 || PLOT_MEAS(plot_meas_index+1) == 2) 
                        ylabel(sprintf("Degree %d\newline Power (kW)",(degree_index +1)*2));
                    else
                        ylabel(sprintf("Degree %d\newline Time (ms)",(degree_index +1)*2));
                    end
    
                end
                
                if (number_subplot == 1 || number_subplot == 2)
                    title(title_column(model_index+1));
                end
    
                if(number_subplot == 5 || number_subplot == 6)
                    xlabel ("Number of nodes");
                end
                
                hold off
                number_subplot = number_subplot+1;
            end
        end
    
        % Set legend
        h_legend=legend(criterio, 'location','best');
        set(h_legend,'FontSize',size_legends);
        set(h_legend,'position',pos_legend);
        
        % Save the file
        if PLOT_MEAS(plot_meas_index+1) == 0
            format='%s/seed_%s.pdf';
            print(fig,sprintf(format, path, titulo),'-dpdf','-fillpage');
        elseif PLOT_MEAS(plot_meas_index+1) == 1
            format='%s/balance_%s.pdf';
            print(fig,sprintf(format, path, titulo),'-dpdf','-fillpage');
        elseif PLOT_MEAS(plot_meas_index+1) == 2
            format='%s/absFlux_%s.pdf';
            print(fig,sprintf(format, path, titulo),'-dpdf','-fillpage');
        elseif PLOT_MEAS(plot_meas_index+1) == 3
            format='%s/time_ID_%s.pdf';
            print(fig,sprintf(format, path, titulo),'-dpdf','-fillpage');
        else
            format='%s/time_balance_%s.pdf';
            print(fig,sprintf(format, path, titulo),'-dpdf','-fillpage');
        end
    end
end

