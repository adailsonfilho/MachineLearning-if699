function [ M ] = lerDados( )

% Abre o arquivo e lê os dados contidos nele. Como se trata se aprendizagem
% não supervisionada, a ultima coluna, que contém as labels, é ignorada.
fileID = fopen('dados.dat');
C = textscan(fileID,'%c %c %c %c %c %c %c %c %c %s','Delimiter',',');
fclose(fileID);
C(:,10) = [];


%O retorno da função textscan é um cell array. Para facilitar a
%manipulação, convertemos para uma matriz.
M = cell2mat(C);

end

