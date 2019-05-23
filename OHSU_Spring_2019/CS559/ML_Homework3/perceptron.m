
% This function will take an input of two
% datasets where X1 is class 1 and X2 is
% class 2. X1 and X2 must have the same 
% number of columns. It will then perform 
% the perceptron learning algorithm. The
% function will return the final weights
% as well as the random initial weights.
function [W, Winit] = perceptron(X1, X2)

    moves = 0;
    % Create seperate and combined class matricies
    % by adding bias in column one and y in column 4
    C1 = [ones(size(X1,1),1), X1, ones(size(X1,1),1)]
    C2 = [ones(size(X2,1),1), X2, -1*ones(size(X2,1),1)]
    C = [C1;C2]
    
    % get the dimentionality of the training data
    dim = size(C,2)-1;
    
    % initialize random weights
    W = rand(1, dim);
    Winit = W; % store initial
        figure
    hold on
    scatter(C1(:,2)', C1(:,3)', 'filled', 'r');
    scatter(C2(:,2)', C2(:,3)', 'filled', 'b');
    xax = floor(min(C(:,2)))-1: ceil(max(C(:,2)))+1;
    plot(xax, -(W(2)/W(3))*xax - (W(1)/W(3)));
    hold off
    
    
    % initialize plots with class colored data points
    % as well as a line reflecting the initial weights
    figure
    hold on
    scatter(C1(:,2)', C1(:,3)', 'filled', 'r');
    scatter(C2(:,2)', C2(:,3)', 'filled', 'b');
    xax = floor(min(C(:,2)))-1: ceil(max(C(:,2)))+1;
    plot(xax, -(W(2)/W(3))*xax - (W(1)/W(3)));
    
    % while learning has not converged
    while ~converged(C,W) % helper, see below
        
        % for every point in the dataset
        for i = 1:size(C,1);
            
            % calculate y hat
            y = C(i,dim+1);
            y_hat = y*(W*C(i,1:dim)');

            % update weights
            lrn_rate =  1;
            if y_hat < 0
                moves = moves+1;
                W = W+(y*lrn_rate)*C(i,1:dim);

                % plot at each weight update
                plot(xax, -(W(2)/W(3))*xax - (W(1)/W(3)));
            end
        end
    end

    hold off
    
    figure
    hold on
    scatter(C1(:,2)', C1(:,3)', 'filled', 'r');
    scatter(C2(:,2)', C2(:,3)', 'filled', 'b');
    plot(xax, -(W(2)/W(3))*xax - (W(1)/W(3)));
    hold off
    
    moves
end

% This is a helper function for the perceptron
% function. Handed a data set that includes 
% binary lables in the last column, it will
% return true if all labels are classifiec 
% correctly and false if they are not.
function has_converged = converged(C,W)

    % for every data point in set
    for i = 1:size(C,1)
        dim = size(C,2); 
        y = C(i,dim);
        y_hat = y*(W*C(i,1:dim-1)');
        % if missclassification
        if y_hat <0;
            has_converged = false;
            return
        end
    end
    % if no missclassification occoured
    has_converged = true;
end






