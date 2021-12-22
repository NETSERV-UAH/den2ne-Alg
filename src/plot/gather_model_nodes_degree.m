function data_model_node_degree = gather_model_nodes_degree(path)
    num_model=2; % modelos: waxman y barabasi
    models = ["barabasi" , "waxman"];
    num_nodes = 20; % de 10 al 200 
    nodes = 0;
    incr_node = 10; %los nodos se incrementa de 10 en 10
    num_degree = 3; 
    degrees = [2 4 6]; % grados 2 4 y 6
    

    %iniciar cell
    data_model_node_degree = cell(num_model, num_nodes, num_degree);
 
    for model=1:2
        nodes = 0; %por cada modelo se incializa a 0 los nodos 
        for node=1:20
            nodes = nodes + incr_node;
            for degree=1:3
                full_path = path + "/" + models(model) + "-" + nodes + "-" + degrees(degree) + "/";
                data_model_node_degree{model, node, degree} = gather_csv(full_path);
            end
        end
    end
end