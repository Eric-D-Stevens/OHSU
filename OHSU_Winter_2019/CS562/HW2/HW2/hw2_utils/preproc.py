from collections import Counter

import pandas as pd
import numpy as np

# deliverable 1.1
def bag_of_words(text):
    """
    Count the number of word occurrences for a given document

    :param text: a document, as a single string
    :returns: a Counter representing a single document's word counts
    :rtype: Counter
    """
    text_list = text.split()
    cnt = Counter()
    for word in text_list:
        cnt[word] += 1

    return cnt

# deliverable 1.2
def aggregate_counts(bags_of_words):
    """
    Aggregate bag-of-words word counts across an Iterable of documents into a single bag-of-words.

    :param bags_of_words: an iterable of bags of words, produced from the bag_of_words() function above
    :returns: an aggregated bag of words for the whole corpus
    :rtype: Counter
    """
    aggregate_counter = Counter() 
    for counter in bags_of_words:
        aggregate_counter += counter

    return aggregate_counter

# deliverable 1.3
def compute_oov(bow1, bow2):
    """
    Return a set of words that appears in bow1, but not bow2

    :param bow1: a bag of words
    :param bow2: a bag of words
    :returns: the set of words in bow1, but not in bow2
    :rtype: set
    """
    only_in_bow1 = set()    
    len(bow1)
    len(bow2)
    for word in bow1:
        if bow2[word] < 1:
            only_in_bow1.add(word)

    return only_in_bow1
    
# deliverable 1.4
def prune_vocabulary(training_counts, target_data, min_counts):
    """
    Prune target_data to only include words that occur at least min_counts times in training_counts
    
    :param training_counts: aggregated Counter for the training data
    :param target_data: list of Counters containing dev bow's
    :returns: new list of Counters, with pruned vocabulary
    :returns: list of words in pruned vocabulary
    :rtype list of Counters, set
    """

    new_set_of_words = set()

    for word in training_counts:
        if training_counts[word] >= min_counts:
            new_set_of_words.add(word)
        '''
        else:
            for counter in new_target_data:
                del counter[word]
        '''
    new_target_data = list()
    for counter in target_data:
        cnt = Counter()
        for word in counter:
            if word in new_set_of_words:
                cnt[word] = counter[word]
        new_target_data.append(cnt)

    return (new_target_data, new_set_of_words)

# Helper functions

def read_data(fname, label='Era', preprocessor=bag_of_words): 
    df = pd.read_csv(fname)
    return (df[label].values, [preprocessor(string) for string in df['Lyrics'].values])
    
def oov_rate(bow1, bow2):
    return len(compute_oov(bow1, bow2)) / len(bow1.keys())
