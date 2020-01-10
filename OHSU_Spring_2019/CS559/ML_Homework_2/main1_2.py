#!/usr/bin/python3

''' 
main1_2.py

Write and submit the program main1_2 that:
    *loads the train and test set.
    * learns the weights for the training set.
    * computes the mean squared error of your predictor on:
        * The training set.
        * The testing set.

'''

import numpy as np

def LR_solve(X,Y):
    ''' retruns linear coeffs'''
    Xm = np.matrix(X)
    Ym = np.matrix(Y)
    Ym = Ym.T

    A = Xm.T*Xm
    B = Xm.T*Ym

    return np.array((A.I*B).T)[0]

def LR_predict(X,W):
    ''' returns linear solution '''
    return np.matmul(X,W.T)

def calc_mse(X,Y,W):
    ''' Uses a previously calculated W to
    calculate the error between an input
    X matrix and the correspoding 'true'
    dependent values Y'''

    SqErr = 0.0

    for x,y in zip(X,Y):

        y_hat = LR_predict(x,W)
        SqErr += (y_hat - y)**2

    return SqErr/len(Y)


def main():
    '''
    * loads the train and test set.
    * learns the weights for the training set.
    * computes the mean squared error of your predictor on:
        * The training set.
        * The testing set.
    '''


    # load the training set
    data_train = np.loadtxt('housing_train.txt')

    # load the testing data
    data_test = np.loadtxt('housing_test.txt')


    # set X and Y training variables
    X_train = data_train[:,:13]
    Y_train = data_train[:,13]

    # set X and Y training variables
    X_test= data_test[:,:13]
    Y_test= data_test[:,13]

    # get the weights form the training data
    W = LR_solve(X_train,Y_train)
    print(W)

    # calculate the mse for the training data
    training_MSE = calc_mse(X_train, Y_train, W)
    print("Training MSE:", training_MSE)

    # calculate the mse for the testing data
    testing_MSE = calc_mse(X_test, Y_test, W)
    print("Testing MSE:", testing_MSE)

if __name__ == "__main__":
    # execute only if run as a script
    main()

