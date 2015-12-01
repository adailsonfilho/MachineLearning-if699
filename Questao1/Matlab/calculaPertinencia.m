function [ u ] = calculaPertinencia( D, prototipos, nObjetos, K, q, m)
%CALCULAPERTINENCIA Summary of this function goes here
%   Detailed explanation goes here


%Definir matriz de pertinencia 'u'.
u = zeros(nObjetos, K);

for i = 1:nObjetos

    for h = 1:K

        numerador = 0;
        for Q = 1:q
            numerador = numerador + D(i,prototipos(h, Q));
        end;
        
        somatorio = 0;
        for k = 1:K
            denominador = 0;
            for Q = 1:q
                denominador = denominador + D(i, prototipos(k, Q));
            end
            somatorio = somatorio + (numerador/denominador^(1/(m-1)));
        end
        
        resultado = somatorio;
        if (resultado > 0)
          resultado = 1/resultado;
        end
        
        u(i, h) = resultado;
    end

end

