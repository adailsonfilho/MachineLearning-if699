clc

[input, output] = lerDados();
[input, output] = modificaEntradaSaida(input, output);
[linhas, colunas] = size(input);

K = 10;

qtdPositivos = sum(output);
qtdNegativos = linhas - qtdPositivos;

fixPositivos = floor(qtdPositivos/K);
fixNegativos = floor(qtdNegativos/K);

x = 0;
error = 0;
teste = [];
label = [];


for k = 1:K

        x = 0;
        i = 0;
        while (x<fixPositivos && qtdPositivos>0)

            num = randi([1 qtdPositivos]);
            teste = [teste; input(num,:)];
            label = [label; output(num)];
            input(num,:) = [];
            output(num,:) = [];
            qtdPositivos = qtdPositivos-1;
            x = x+1;

        end

        disp(qtdPositivos);
        x = 0;
        startNegativos = qtdPositivos+1;
        linhas = qtdPositivos+qtdNegativos;

        while (x<fixNegativos && qtdNegativos>0)

            num = randi([startNegativos linhas]);
            teste = [teste; input(num,:)];
            label = [label; output(num)];
            input(num,:) = [];
            output(num,:) = [];
            qtdNegativos = qtdNegativos-1;
            linhas = linhas-1;
            x = x+1;
            

        end
        
        
end

contador = 1;
for k = 1:K

    testData = teste(1:95,:);
    testLabel = label(1:95,:);
    
    teste(1:95,:) = [];
    label(1:95,:) = [];
    input = teste;
    output = label;
    
    [bias, weights, ~] = treinaMLP(input, output);
    
    [linhas_teste, ~] = size(testData);
    out = zeros(linhas_teste, 1);
    H = zeros(colunas, 1);
    x2 = zeros(colunas, 1);
    for i = 1:linhas_teste

          % Hidden layer
          for x = 1:colunas
              H(x,1) = bias(1,x)*weights(x,1);
              for y = 1:colunas
                H(x,1) = H(x,1) + testData(i,y)*weights(x,y+1);
              end
          end

          for x = 1:colunas
              x2(x,1) = sigma(H(x, 1));
          end

          % Output layer
          x3_1 = bias(1,colunas+1)*weights(colunas+1,1);
          for y = 1:colunas
            x3_1 = x3_1 + x2(y)*weights(colunas+1,y+1);   
          end
          out(i) = sigma(x3_1);

    end

    error = error + immse(out, testLabel);
    disp(error);
    
    teste = [teste; testData];
    label = [label; testLabel];
    
end

