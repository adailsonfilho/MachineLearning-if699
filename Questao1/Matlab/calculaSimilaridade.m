function [ U ] = calculaSimilaridade(D, prototipos, linhas, K, m, n)
%CALCULASIMILARIDADE Summary of this function goes here
%   Detailed explanation goes here

U = zeros(linhas, K);
for i = 1:linhas

    for k = 1:K

        somatorio = 0;
        numerador = somaElementosClasse(D, prototipos, k, i, n);
        for h = 1:K
            denominador = somaElementosClasse(D, prototipos, h, i, n);
            if (denominador ~= 0)
                somatorio = somatorio + (numerador/denominador)^(1/(m-1));
            else
                somatorio = somatorio + 0;
            end
        end   
        
        if (somatorio ~= 0)
            U(i, k) = 1/somatorio;
        else
            U(i, k) = 0;
        end
    end
end

end

