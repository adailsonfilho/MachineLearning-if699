function [ resultado ] = somaElementosClasse(D, prototipos, classe, elemento, q)
%SOMAELEMENTOSCLASSE Summary of this function goes here
%   Detailed explanation goes heresoma
        resultado = 0;
        for c1 = 1:q
            resultado = resultado + D(elemento, prototipos(classe, c1));
        end

end

