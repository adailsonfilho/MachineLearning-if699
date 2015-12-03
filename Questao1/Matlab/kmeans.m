function [ J,  classesF, U ] = kmeans( D, linhas, colunas )
%KMEANS Summary of this function goes here
%   Detailed explanation goes here
clc


%Definição dos parametros
K = 2;
m = 2;
q = 2;
T = 10;
epsilon = 10^(-10);
t = 0;

%Escolher 2 protótipos, representando as 2 classes. p1 e p2 representam as
%linhas da matriz onde se encontram esses protótipos
prototipos = zeros(K, q);
p=0;
for y = 1:q
    for x = 1:K
        %disp(p);
        while (sum(any(prototipos == p)))
            rng shuffle
            p = randi([1 linhas]);
        end
        prototipos(x, y) = p;
        p=0;
    end
end
%disp('Prototipos Originais Gerados');
%disp(prototipos);
%disp(prototipos(2, 1));
%disp('Hora de parar');

%Calcular graus de similariadade de cada um dos elementos com os dois
%prototipos selecionados.
U = calculaSimilaridade(D, prototipos, linhas, K, m, q);
%disp('Hora de parar');


%Calculo da adequação das resposta a solução
J = 0;
%disp('Inicio do Calculo do J');
for k = 1:K
    for i = 1:linhas
        %disp(J);
        J = J + (U(i, k)^m)*somaElementosClasse(D, prototipos, k, i, q);
    end
end
%disp(J);
%disp('INICIO');

JT = zeros(t+1, 1);
JT(1,1) = J;
%Loop principal
for t = 1:T 
    
    disp(t);
    %disp(prototipos);
    
    prototipos = zeros(K, q);
    %Calcular novos protótipos
    for k = 1:K
        
            l = zeros(linhas, 1);
            for h = 1:linhas
                for i = 1:linhas
                    l(h, 1) = l(h, 1) + (U(i, k)^m)*D(i, h);
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
    
    %disp(prototipos);
    %Atualizar matriz de similaridades
    U = calculaSimilaridade(D, prototipos, linhas, K, m, q);
    
    
    %Calcula novo fitness
    newJ = 0;
    
    for k = 1:K
        soma = 0;
        for i = 1:linhas
            soma = soma + (U(i, k)^m)*somaElementosClasse(D, prototipos, k, i, q);
        end
        newJ = newJ + soma;
    end 
    
    %Condição de parada
    %disp(prototipos);
    
    if (abs(J-newJ) < epsilon)
        break;
    end
    
    J = newJ;
    JT(t+1, 1) = newJ;
    disp(J);
    disp('Fina da iteracao');
    
end
plot(JT);

classesF = zeros(1,1);
for x = 1:linhas
    
    if (U(x, 1) > U(x, 2))
        classesF(x, 1) = 1;
    else
        classesF(x, 1) = 2;
    end
end