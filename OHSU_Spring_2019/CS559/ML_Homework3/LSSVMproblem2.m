% Download package at: https://www.esat.kuleuven.be/sista/lssvmlab/

% load data from .txt files
training_data = dlmread('pima_train.txt');
testing_data = dlmread('pima_test.txt');

% training data
X = training_data(:,1:8);
Y = 2*training_data(:,9) - 1;

% testing data
Xt = testing_data(:,1:8);
Yt = 2*testing_data(:,9) - 1;
Yt = (Yt+1)/2;

%% auto tune linear model
type = 'classification';
L_fold = 10; % L-fold crossvalidation
model = initlssvm(X,Y,type,[],[],'lin_kernel');
model = tunelssvm(model,'simplex','crossvalidatelssvm',{L_fold,'misclass'});
model = trainlssvm(model);

% calculate training performance
Y_hat = simlssvm(model,X);
Y_hat = (Y_hat+1)/2;
train_accuracy = sum(Y_hat(:,1) == ((Y+1)/2)) /size(Y,1)
train_error = 1-train_accuracy
train_confusion_matrix = [~Y_hat'*double(~((Y+1)/2)), Y_hat'*~((Y+1)/2);
                    ~Y_hat'*((Y+1)/2), Y_hat'*((Y+1)/2)]

% calculate testing performance
Y_hat = simlssvm(model,Xt);
Y_hat = (Y_hat+1)/2;
test_accuracy = sum(Y_hat(:,1) == Yt)/size(Yt,1)
test_error = 1-test_accuracy
test_confusion_matrix = [~Y_hat'*double(~Yt), Y_hat'*~Yt;
                    ~Y_hat'*Yt, Y_hat'*Yt]

                
%% auto tune polinomial model
type = 'classification';
L_fold = 10; % L-fold crossvalidation
model = initlssvm(X,Y,type,[],[],'poly_kernel');
model = tunelssvm(model,'simplex','crossvalidatelssvm',{L_fold,'misclass'});
model = trainlssvm(model);

% calculate training performance
Y_hat = simlssvm(model,X);
Y_hat = (Y_hat+1)/2;
train_accuracy = sum(Y_hat(:,1) == ((Y+1)/2)) /size(Y,1)
train_error = 1-train_accuracy
train_confusion_matrix = [~Y_hat'*double(~((Y+1)/2)), Y_hat'*~((Y+1)/2);
                    ~Y_hat'*((Y+1)/2), Y_hat'*((Y+1)/2)]

% calculate testing performance
Y_hat = simlssvm(model,Xt);
Y_hat = (Y_hat+1)/2;
test_accuracy = sum(Y_hat(:,1) == Yt)/size(Yt,1)
test_error = 1-test_accuracy
test_confusion_matrix = [~Y_hat'*double(~Yt), Y_hat'*~Yt;
                    ~Y_hat'*Yt, Y_hat'*Yt]



%% auto tune RBF model
type = 'classification';
L_fold = 10; % L-fold crossvalidation
model = initlssvm(X,Y,type,[],[],'RBF_kernel');
model = tunelssvm(model,'simplex','crossvalidatelssvm',{L_fold,'misclass'});
model = trainlssvm(model);

% calculate training performance
Y_hat = simlssvm(model,X);
Y_hat = (Y_hat+1)/2;
train_accuracy = sum(Y_hat(:,1) == ((Y+1)/2)) /size(Y,1)
train_error = 1-train_accuracy
train_confusion_matrix = [~Y_hat'*double(~((Y+1)/2)), Y_hat'*~((Y+1)/2);
                    ~Y_hat'*((Y+1)/2), Y_hat'*((Y+1)/2)]

% calculate testing performance
Y_hat = simlssvm(model,Xt);
Y_hat = (Y_hat+1)/2;
test_accuracy = sum(Y_hat(:,1) == Yt)/size(Yt,1)
test_error = 1-test_accuracy
test_confusion_matrix = [~Y_hat'*double(~Yt), Y_hat'*~Yt;
                    ~Y_hat'*Yt, Y_hat'*Yt]
