function [ M, R ] = lerDados( )

% Abre o arquivo e l� os dados contidos nele. Como se trata se aprendizagem
% n�o supervisionada, a ultima coluna, que cont�m as labels, � ignorada.
fileID = fopen('dados.dat');
C = textscan(fileID,'%c %c %c %c %c %c %c %c %c %s','Delimiter',',');
fclose(fileID);
R = C(:,10);
C(:,10) = [];


%O retorno da fun��o textscan � um cell array. Para facilitar a
%manipula��o, convertemos para uma matriz.
M = cell2mat(C);
R = cell2mat(R{1,1});

end

