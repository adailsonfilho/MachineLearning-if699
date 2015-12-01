function [ mD ] = dissimilaridade( dados )

[linhas, colunas] = size(dados);
mD = zeros(linhas, linhas);


	for i = 1:linhas
	    for j = i:linhas
	        if (i ~= j)
	            mD(i, j) = qtdDiferentes(dados(i,:), dados(j,:));
	            mD(j, i) = mD(i, j);
	        end
	    end
	end

end
