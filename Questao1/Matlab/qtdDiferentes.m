function [ qtd ] = qtdDiferentes(vetorDados1, vetorDados2)
%QTDDIFERENTES Summary of this function goes here
%   Detailed explanation goes here

qtd = 0;
[linhas, colunas] = size(vetorDados1);

for x = 1:colunas
    if (vetorDados1(1, x) ~= vetorDados2(1, x))
        qtd = qtd+1;
    end
end

end

