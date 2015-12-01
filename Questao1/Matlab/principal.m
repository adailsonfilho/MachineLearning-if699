clc

%Obter dados do arquivo
dados = lerDados();
[nObjetos, colunas] = size(dados);
disp('Dados Lidos');

%A partir dos dados, obter matriz de dissimilaridade
D = dissimilaridade(dados);


%Normalizar matriz de dissimilaridade
normD = D - min(D(:));
normD = normD./max(D(:));
D = normD;
disp('Matriz de Dissimilaridade gerada');


%Estabelecer parametros fixos
%Numero de Classes
K = 2;

%Controle de fuzzificação
m = 3;

%Controle de iterações
T = 50;
t = 0;

%Quantidade de elementos que definem um prototipo
q = 2;

%Definição dos protótipos iniciais
prototipos = zeros(K, q);
for k = 1:K
    for x = 1:q
        
        %Selecione um elemento aleatoriamente e verififque se o mesmo já é
        %um prototipo, se não for atribuir ao vetor de prototipos.
        prototipo = randi([1 nObjetos]);
        while (any(prototipo == prototipos))
             prototipo = randi([1 nObjetos]);
        end
        prototipos(k, x) = prototipo;
        
        
    end
end
disp('Prototipos iniciais escolhidos');
disp(prototipos);

%Calcular grau de pertinencia de cada elemento.
u = calculaPertinencia(D, prototipos, nObjetos, K, q, m);


%Calcular fitness inicial
J = 0;
for k=1:K
    for i = 1:nObjetos
        
        somatorio = 0;
        for Q = 1:q
            somatorio = somatorio + D(i, prototipos(k, Q));
        end
        
        J = J + (u(i, k)^m)*somatorio;
        
    end
end

disp(J);


totalJ = zeros(T, 1);

%Dar inicio às iterações de evolução
for t = 1:T
    
    prototipos = zeros(K, q);
    %Calculo dos novos prototipos 
    for k = 1:K
    
        l = zeros(nObjetos, 1);
        for i = 1:nObjetos
            for h = 1:nObjetos
                l(i, 1) = l(i, 1) + (u(i, k)^m)*D(i, h);
            end
        end
        
        for x = 1:q
              [~, argmin] = min(l);
              
              while (sum(any(prototipos == argmin)))
                  l(argmin,1) = 10^10;
                  [~, argmin] = min(l);
              end
              
              prototipos(k, x) = argmin;
              l(argmin,1) = 10^10;
        end
        
    end
    
    disp('Novos prototipos definidos');
    disp(prototipos);
    
    u = calculaPertinencia(D, prototipos, nObjetos, K, q, m);
    
    J = 0;
    for k=1:K
        for i = 1:nObjetos

            somatorio = 0;
            for Q = 1:q
                somatorio = somatorio + D(i, prototipos(k, Q));
            end

            J = J + (u(i, k)^m)*somatorio;

        end
    end
    
    totalJ(t, 1) = J;
    disp(J);
    
    disp('Continua...');
    
end


plot(totalJ);





