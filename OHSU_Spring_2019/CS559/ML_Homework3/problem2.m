%%% Problem 2: SVM


%% load data from .txt files
training_data = dlmread('pima_train.txt');
testing_data = dlmread('pima_test.txt');

%% shuffle data and adjust split
data = [training_data; testing_data] % combine data
[r, c] = size(data) 
shuf_data = data % new matrix of same size
idx=randperm(r) % random permutation array
for i=1:r 
    shuf_data(i,:)=data(idx(i),:); % shuffle data
end
% create new tt split
training_data = shuf_data(1:690,:);
testing_data = shuf_data(691:r,:);

%% training
X = training_data(:,1:8);
Y_in = training_data(:,9);
cost = 1.0;
[W,b] = svml(X,Y_in,cost);

%% get model performance on training data
% get y and y_hat
Y_test = training_data(:,9);
Y_hat = double(training_data(:,1:8)*W+b >0);
%training data size
training_size = size(training_data)
% calculate accuracy
train_accuracy = sum(Y_hat(:,1) == Y_test)/size(Y_test,1)
% classification error
train_error = 1-train_accuracy
% build confusion matrix
train_confusion_matrix = [~Y_hat'*double(~Y_test), Y_hat'*~Y_test;
                    ~Y_hat'*Y_test, Y_hat'*Y_test]
                

%% get model performance on testing data
% get y and y_hat
Y_test = testing_data(:,9);
Y_hat = double(testing_data(:,1:8)*W+b >0);
% test data size
testing_size=size(testing_data)
% calculate accuracy
test_accuracy = sum(Y_hat(:,1) == Y_test)/size(Y_test,1)

% classification error
test_error = 1-test_accuracy

% build confusion matrix
test_confusion_matrix = [~Y_hat'*double(~Y_test), Y_hat'*~Y_test;
                    ~Y_hat'*Y_test, Y_hat'*Y_test]
                
