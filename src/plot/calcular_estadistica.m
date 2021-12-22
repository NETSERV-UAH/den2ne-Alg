function medias_modelo_grado_criterio_nodo = calcular_estadistica(datos)   
    % media por semilla fijando criterio 
    total_seeds = 10;
    total_criteria = 6;
    total_nodes = 20;
    total_degrees = 3;
    
    media = zeros(10,5);
    media_de_medias_por_nodo = zeros(20,5);
    media_de_medias_por_nodo_y_criterio = cell(6,1);
    media_de_medias_por_nodo_criterio_y_grado = cell(3,1);
    medias_modelo_grado_criterio_nodo = cell (2,1);
    
    for model=1:2
        for degree=1:total_degrees
            for criteria=1:total_criteria
                for nodes=1:total_nodes
                    for seed=1:total_seeds
                        %se realiza la media de cada archivo csv 
                        media(seed,:,1) = mean(datos{model,nodes,degree}{criteria,seed});
                    end
                    %se realiza la media de medias por cada nodo
                    media_de_medias_por_nodo(nodes,:) = mean(media); 
                end
                %por cada criterio
                media_de_medias_por_nodo_y_criterio{criteria} = media_de_medias_por_nodo; 
            end
            %por cada grado de conectividad
            media_de_medias_por_nodo_criterio_y_grado{degree} = media_de_medias_por_nodo_y_criterio;
        end
        %por modelo
        medias_modelo_grado_criterio_nodo{model} = media_de_medias_por_nodo_criterio_y_grado;
    end
end

