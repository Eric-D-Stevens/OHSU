%% Problem 1 with SVM

% enter the data manually
class1 = [-1 -1; 2 0; 2 1; 0 1; 0.5 1.5];
class2 = [3.5 2.5; 3 4; 5 2; 5.5 3];

XY = [[class1, ones(size(class1,1),1)];
    [class2, -ones(size(class2,1),1)]];

X = XY(:,1:2)
Y = XY(:,3)

%% auto tune linear model
type = 'classification';
L_fold = 10; % L-fold crossvalidation
model = initlssvm(X,Y,type,[],[],'lin_kernel');
model = tunelssvm(model,'simplex','crossvalidatelssvm',{L_fold,'misclass'});
model = trainlssvm(model);
plotlssvm(model);

%% auto tune polynomial model
type = 'classification';
L_fold = 10; % L-fold crossvalidation
model = initlssvm(X,Y,type,[],[],'poly_kernel');
model = tunelssvm(model,'simplex','crossvalidatelssvm',{L_fold,'misclass'});
model = trainlssvm(model);
plotlssvm(model);

%% auto tune RBF model
type = 'classification';
L_fold = 10; % L-fold crossvalidation
model = initlssvm(X,Y,type,[],[],'RBF_kernel');
model = tunelssvm(model,'simplex','crossvalidatelssvm',{L_fold,'misclass'});
model = trainlssvm(model);
plotlssvm(model);