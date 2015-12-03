function [ bias, weights, out ] = treinaMLP( input, output )
%TREINAMLP Summary of this function goes here
%   Detailed explanation goes here

% XOR input for x1 and x2
[linhas, colunas] = size(input);

% Initialize the bias
bias = [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1];
% Learning coefficient
coeff = 0.7;
% Number of learning iterations
iterations = 1000;
% Calculate weights randomly using seed.
rand('state',sum(100*clock));
weights = -1 +2.*rand(colunas+1,colunas+1);

for i = 1:iterations
   disp(i);
   out = zeros(linhas,1);
   numIn = length (input(:,1));
   H = zeros(colunas, 1);
   x2 = zeros(colunas, 1);
   for j = 1:numIn
       
      % Hidden layer
      for x = 1:colunas
          H(x,1) = bias(1,x)*weights(x,1);
          for y = 1:colunas
            H(x,1) = H(x,1) + input(j,y)*weights(x,y+1);
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
      out(j) = sigma(x3_1);
      
      % Adjust delta values of weights
      % For output layer:
      % delta(wi) = xi*delta,
      % delta = (1-actual output)*(desired output - actual output) 
      deltaFinal = out(j)*(1-out(j))*(output(j)-out(j));
      
      % Propagate the delta backwards into hidden layers
      
      delta = zeros(colunas, 1);
      for y = 1:colunas
        delta(y, 1) = x2(y)*(1-x2(y))*weights(colunas+1,y+1)*deltaFinal;
      end
      
      % Add weight changes to original weights 
      % And use the new weights to repeat process.
      % delta weight = coeff*x*delta
      for k = 1:colunas+1
         if k == 1 % Bias cases
            weights(1,k) = weights(1,k) + coeff*bias(1,1)*delta(1, 1);
            weights(2,k) = weights(2,k) + coeff*bias(1,2)*delta(2, 1);
            weights(3,k) = weights(3,k) + coeff*bias(1,3)*delta(3, 1);
            weights(4,k) = weights(4,k) + coeff*bias(1,4)*delta(4, 1);
            weights(5,k) = weights(5,k) + coeff*bias(1,5)*delta(5, 1);
            weights(6,k) = weights(6,k) + coeff*bias(1,6)*delta(6, 1);
            weights(7,k) = weights(7,k) + coeff*bias(1,7)*delta(7, 1);
            weights(8,k) = weights(8,k) + coeff*bias(1,8)*delta(8, 1);
            weights(9,k) = weights(9,k) + coeff*bias(1,9)*delta(9, 1);
            weights(10,k) = weights(10,k) + coeff*bias(1,10)*deltaFinal;
         else % When k=2 or 3 input cases to neurons
            weights(1,k) = weights(1,k) + coeff*input(j,1)*delta(1, 1);
            weights(2,k) = weights(2,k) + coeff*input(j,2)*delta(2, 1);
            weights(3,k) = weights(3,k) + coeff*input(j,3)*delta(3, 1);
            weights(4,k) = weights(4,k) + coeff*input(j,4)*delta(4, 1);
            weights(5,k) = weights(5,k) + coeff*input(j,5)*delta(5, 1);
            weights(6,k) = weights(6,k) + coeff*input(j,6)*delta(6, 1);
            weights(7,k) = weights(7,k) + coeff*input(j,7)*delta(7, 1);
            weights(8,k) = weights(8,k) + coeff*input(j,8)*delta(8, 1);
            weights(9,k) = weights(9,k) + coeff*input(j,9)*delta(9, 1);
            weights(10,k) = weights(10,k) + coeff*x2(k-1)*deltaFinal;
         end
      end
   end   
end


end

