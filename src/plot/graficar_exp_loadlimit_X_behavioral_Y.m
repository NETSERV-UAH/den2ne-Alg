function grafo = graficar_exp_loadlimit_X_behavioral_Y(datos,titulo,f_objetivo) 
    %graficamos 
    %f_objetivo es el resultado que queremos mostrar. Puede ser, semilla(1)
    %Balance Global (2), abs_flux(3), tiempo IDs (4) y tiempo de
    %convergencia de cargas (5)

    medias_modelo_grado_criterio_nodo = calcular_estadistica(datos);
    
    criterio = ["Number Hops" "Distance" ,"Power Balance", "Power Balance with Losses", "Link Losses", "Power Balance Weighted"];
    title_column= ["Barabasi", "Waxman"];
    title_row = ["Degree 2", "Degree 4", "Degree 6"];
    etiqueta_y = ["Semilla", "Balance Global", "abs_flux", "Tiempo IDs (ms)", "Tiempo convergencia(ms)"];
    
    marker = ["-o", "--+", ":*", "-.d","-x", "--s"];
    
    
    number_subplot = 1;
    
    for degree=1:3
        for model=1:2
            subplot(3,2,number_subplot);
            %figure
            for criteria=1:6
                plot ((100:10:200), medias_modelo_grado_criterio_nodo{model}{degree}{criteria}(10:20,f_objetivo),marker(criteria));
                xticks((100:10:200));
                ylabel(etiqueta_y(f_objetivo));
                xlabel ("Number of nodes");
                grid on;
                hold on;
            end
            number_subplot = number_subplot+1;
            title(title_column(model) + " " + title_row(degree));
        end
    end
    
    % Get handles to center subplots
    
    legend( criterio,'location', 'northwest');
    sgtitle(titulo, "Interpreter", "none");
end

