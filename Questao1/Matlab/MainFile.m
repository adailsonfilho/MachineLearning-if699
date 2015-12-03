repeticoes = 100;
melhorJ = 10^(10);

%Obter matriz de dados
dados = lerDados();
disp('Dados Lidos');
[linhas, colunas] = size(dados);

%Obter matriz de dissimilaridade
D = dissimilaridade(dados);
normD = D - min(D(:));
normD = normD./max(D(:));
D = normD;
disp('Matriz de Dissimilaridade Gerada');
a = zeros(958, 1);

for  i = 1:repeticoes

    [J, classes, U] = kmeans( D, linhas, colunas);
    if (J<melhorJ)
        melhorJ = J;
        classesF = classes;
        UF = U;
    end
    
end

soma = 0;
lab = zeros(958, 1);

c1 = [];
c2 = [];
for i = 1:958
    
    if (classesF(i, 1) == 1)
        c1 = [c1; i];
    else
        c2 = [c2; i];
    end
end

a = adjrand(classesF, lab);
        


        