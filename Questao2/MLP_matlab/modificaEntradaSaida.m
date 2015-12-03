function [ in, out ] = modificaEntradaSaida( input, output )
%MODIFICAENTRADASAIDA Summary of this function goes here
%   Detailed explanation goes here


[linhas, colunas] = size(input);
in = zeros(linhas, colunas);
for x = 1:linhas
    for y = 1:colunas
        
        if (input(x,y) == 'x')
            in(x,y) = 1;
        elseif (input(x,y) == 'o')
            in(x, y) = 0;
        elseif (input(x,y) == 'b')
            in(x,y) = -1;
        end
    end
end

[linhas, colunas] = size(output);
out = zeros(linhas, 1);
for x = 1:linhas
    
    if (strcmp(output(x, 1), 'p'))
        out(x, 1) = 1;
    else
        out(x, 1) = 0;
    end
end



end

