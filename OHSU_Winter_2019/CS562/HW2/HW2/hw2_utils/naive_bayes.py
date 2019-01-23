from hw2_utils.constants import OFFSET
from hw2_utils import clf_base, evaluation

import numpy as np
from collections import defaultdict, Counter
from itertools import chain
import math

# deliverable 3.1
def get_corpus_counts(x,y,label):
    """
    Compute corpus counts of words for all documents with a given label.

    :param x: list of counts, one per instance
    :param y: list of labels, one per instance
    :param label: desired label for corpus counts
    :returns: defaultdict of corpus counts
    :rtype: defaultdict

    """

    count_dict = defaultdict(int)

    for i in range(len(x)):
        if y[i] == label:
            for word in x[i]:
                count_dict[word] += x[i][word]

    return count_dict

# deliverable 3.2
def estimate_pxy(x,y,label,smoothing,vocab):
    """
    Compute smoothed log-probability P(word | label) for a given label. (eq. 2.30 in Eisenstein, 4.14 in J&M)

    :param x: list of counts, one per instance
    :param y: list of labels, one per instance
    :param label: desired label
    :param smoothing: additive smoothing amount
    :param vocab: list of words in vocabulary
    :returns: defaultdict of log probabilities per word
    :rtype: defaultdict of log probabilities per word

    """

    probability_dict = defaultdict(float)
    count_dict = get_corpus_counts(x,y,label)

    V = len(count_dict)
    CNT = sum(count_dict.values())

    for word in vocab:
        probability_dict[word] = math.log((float(count_dict[word])+smoothing)/(CNT+smoothing*V))

    return probability_dict

# deliverable 3.3
def estimate_nb(x,y,smoothing):
    """
    Estimate a naive bayes model

    :param x: list of dictionaries of base feature counts
    :param y: list of labels
    :param smoothing: smoothing constant
    :returns: weights, as a default dict where the keys are (label, word) tuples and values are smoothed log-probs of P(word|label)
    :rtype: defaultdict 

    """
 
    labels = set(y)
    counts = defaultdict(float)
    doc_counts = defaultdict(float)

    vocab = set()
    for label in labels:
        counts = get_corpus_counts(x,y,label)
        vocab = vocab.union(set(counts.keys()))

    for label in labels:
        current_dict = estimate_pxy(x, y, label, smoothing, vocab)
        for word in current_dict:
            doc_counts[(label,word)] += current_dict[word]

    return doc_counts





# deliverable 3.4
def find_best_smoother(x_tr,y_tr,x_dv,y_dv,smoothers):
    """
    Find the smoothing value that gives the best accuracy on the dev data

    :param x_tr: training instances
    :param y_tr: training labels
    :param x_dv: dev instances
    :param y_dv: dev labels
    :param smoothers: list of smoothing values
    :returns: best smoothing value, scores
    :rtype: float, dict mapping smoothing value to score
    """

    smoothe_scores = dict()

    for s in smoothers:
        current_model = estimate_nb(x_tr, y_tr, s)
        y_hat = clf_base.predict_all(x_dv, current_model, list(set(y_tr)))
        smoothe_scores[s] = evaluation.acc(y_hat, y_dv)

    return (max(smoothe_scores, key=smoothe_scores.get), smoothe_scores)








