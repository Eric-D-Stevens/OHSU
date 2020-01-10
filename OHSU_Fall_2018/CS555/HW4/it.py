import random as rdm
import time
import matplotlib.pyplot as plt


def get_the_file():
    with open("seq_H_T.txt") as textFile:
        lines = [[float(i) for i in line.split()] for line in textFile]
    return lines

'''
k_means_update:
IN: 
    trials - a 2d list of H/T data
    centers - a list of centroids
OUT:
    updated_centers - revised centroids
'''
def k_mean_update(trials, centers):

    means = [sum(line)/float(len(line)) for line in trials] 

    # empty two-d array to be filled with values closest to each center
    segments = [[] for center in centers]

    # seperate values into segments closest to centroid
    for value in means:
        distance = [(value-center)**2 for center in centers]
        add_to_index = distance.index(min(distance))
        segments[add_to_index].append(value)

    # calulate mean of segments and make them new centers
    updated_centers = [sum(seg)/float(len(seg)) for seg in segments]

    # return updated centers in form of input centers
    return updated_centers


'''
expectation_maximization:
IN: 
    trials - a 2d list of H/T data
    centers - a list of centroids
OUT:
    theta_updates - revised centroids
'''
def expectation_maximization(trials, centers):

    sample_size = len(trials[0])
    heads_probabilities = [sum(line)/float(len(line)) for line in trials]

    theta_primes = [[] for center in centers]

    # get probabilities of each centroid for each observation
    for h in heads_probabilities:
        temp = []
        for c in centers:
            temp.append((c**(h*sample_size))*((1-c)**(sample_size*(1-h))))
        for i in range(len(temp)):
            theta_primes[i].append(temp[i]/sum(temp))

    # calculate centroid updates
    theta_updates = []
    for tp in theta_primes:
        H = sum([tp[i]*heads_probabilities[i]*sample_size for i in range(len(tp))])
        T = sum([tp[i]*(1-heads_probabilities[i])*sample_size for i in range(len(tp))])
        theta_updates.append(H/(H+T))

    return theta_updates






from math import log

# this function is the same as the one above except it
# returns the pi values of all runs as well
def expectation_maximization_return_pis(trials, centers):

    sample_size = len(trials[0])
    heads_probabilities = [sum(line)/float(len(line)) for line in lines]

    theta_primes = [[] for center in centers]

    # get probabilities of each centroid for each observation
    for h in heads_probabilities:
        temp = []
        for c in centers:
            temp.append((c**(h*sample_size))*((1-c)**(sample_size*(1-h))))
        for i in range(len(temp)):
            theta_primes[i].append(temp[i]/sum(temp))

    # calculate centroid updates
    theta_updates = []
    for tp in theta_primes:
        H = sum([tp[i]*heads_probabilities[i]*sample_size for i in range(len(tp))])
        T = sum([tp[i]*(1-heads_probabilities[i])*sample_size for i in range(len(tp))])
        theta_updates.append(H/(H+T))

    return [theta_updates, theta_primes]


def EM(trials):

    ss = len(trials[0])
    hp = [sum(line)/float(len(line)) for line in trials]

    init_theta = [1.0/3.0 for i in range(3)]
    theta_prime = []

    for h in hp:
        temp = []
        for c in centers:
            temp.append((c**(h*ss))*((1-c)**(ss*(1-h))))
        for i in range(len(temp)):














