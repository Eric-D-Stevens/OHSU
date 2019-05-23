%% Problem 1

% enter the data manually
class1 = [-1 -1; 2 0; 2 1; 0 1; 0.5 1.5];
class2 = [3.5 2.5; 3 4; 5 2; 5.5 3];

% run perceptron learning algorithm on data
[W, Winit] = perceptron(class1, class2)

% calculate slope an intercept (class2 is y axis)
slope = -W(2)/W(3)
intercept = -W(1)/W(3)

C1 = [ones(size(class1,1),1),class1,ones(size(class1,1),1)]
C2 = [ones(size(class2,1),1),class2,-ones(size(class2,1),1)]
C = [C1;C2]

Mags = ones(size(C,1),1)
Gammas = ones(size(C,1),1)
Wnrm = W/norm(W)
for i=[1:9]
    Mags(i,1) = norm(C(i,1:3));
    Gammas(i,1) = C(i,4)*C(i,1:3)*Wnrm';
end
 
R = max(Mags)
gamma = min(Gammas)

Itts = R/gamma

Wnrm = W/norm(W);
norm(Wnrm);
