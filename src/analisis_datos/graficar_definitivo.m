%exp_loadLimit_0_behavioral_0
%load_Limit = [0, 1];
%behavioral = [0, 1 ,2 ,3];



for load_limit=1:2
    title_load_limit = load_limit-1;
    for behavioral=1:4
        title_behavioral= behavioral-1;
        titulo = "exp_loadLimit_"+ title_load_limit + "_behavioral_"+ title_behavioral;
        figure
        graficar_exp_loadlimit_X_behavioral_Y(datos{load_limit,behavioral}, titulo);
    end
end