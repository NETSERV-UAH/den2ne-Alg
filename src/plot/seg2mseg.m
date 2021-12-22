function Tiempos_ms = seg2mseg(matriz)
    matriz(:,end-1:end) = matriz(:,end-1:end) .* 1000;
    Tiempos_ms = matriz;
end