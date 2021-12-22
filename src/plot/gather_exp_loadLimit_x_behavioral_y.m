function exp_loadLimit = gather_exp_loadLimit_x_behavioral_y(path)
    exp_loadLimit = cell(2,4);
    for limit=0:1
        for behavioral=0:3
            fullpath = path + "/exp_loadLimit_" + limit + "_behavioral_" + behavioral;
            exp_loadLimit{limit+1, behavioral +1} = gather_model_nodes_degree(fullpath);
        end
    end
end