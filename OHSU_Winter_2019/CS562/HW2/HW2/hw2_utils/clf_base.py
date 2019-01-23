from hw2_utils.constants import OFFSET
import numpy as np

# HELPER FUNCTION
def argmax(score_dict):
    """
    Find the 
    :param score_dict: A dict whose keys are labels and values are scores
    :returns: Top-scoring label
    :rtype: string
    """
    items = list(score_dict.items())
    items.sort()
    return items[np.argmax([i[1] for i in items])][0]


# deliverable 2.1
def make_feature_vector(base_features, label):
    """
    Take a dict of bag-of-words features and a label; return a dict of features, corresponding to f(x,y)

    :param base_features: Counter of base features
    :param label: label string
    :returns dict of features, f(x,y)
    :rtype: dict
    """

    features = dict()
    features[(label, OFFSET)] = 1
    for word in base_features:
        features[(label, word)] = base_features[word]

    return features

# deliverable 2.2
def predict(base_features, weights, labels):
    """
    Simple linear prediction function y_hat = argmax_y \theta^T f(x,y)
 
    :param base_features: a dictionary of base features and counts (base features, NOT a full feature vector)
    :param weights: a defaultdict of features and weights. Features are tuples (label, base_feature)
    :param labels: a list of candidate labels
    :returns: top-scoring label, plus the scores of all labels
    :rtype: string, dict
    """

    scores = dict()
    for label in labels:
        score = 0.0
        for word in base_features:
            score += weights[(label,word)]*base_features[word]#+weights[(label,OFFSET)]
        if score == 0.0: score = weights[(label,OFFSET)]
        scores[label] = score#+weights[(label,OFFSET)]

    return (max(scores, key=scores.get), scores)

def predict_all(x, weights, labels):
    """
    Predict the label for all instances in a dataset. For bulk prediction.

    :param x: iterable of base instances
    :param weights: defaultdict of weights
    :param labels: a list of candidate labels
    :returns: predictions for each instance
    :rtype: numpy array
    """
    y_hat = np.array([predict(x_i, weights, labels)[0] for x_i in x])
    return y_hat
    
