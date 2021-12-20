function data_csv = gather_csv(path)
    total_criteria=6;
    total_seeds = 10;
    %Iniciar célula de matrices a 0 
    data_csv = cell(total_criteria,total_seeds);
    %en los archivos el criterio va de c0 a c6. En matlab empieza en 1 por
    %tanto se resta c1 - 1 = c0 
    for criteria=1:total_criteria
        criterio = criteria -1;
        for seed=1:total_seeds
            %disp(path + "outdata_seed_" + seed+ "_c_" + criterio + ".csv")
            data_csv{criteria, seed} = seg2mseg(importdata(path + "outdata_seed_" + seed+ "_c_" + criterio + ".csv"));
        end
    end
end 
