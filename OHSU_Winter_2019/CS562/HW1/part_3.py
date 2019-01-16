'''Eric D. Stevens : OHSU : CS 562 : Homework 1 : Part 3'''

import collections
import pickle
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


def file_to_unigram_dict(input_file="nltk_tokenized.txt",
                         output_file='unigram_count_dict.pkl',):

    ''' Truns space seperated corpus file into a
    defaultdict and writes the default dict object'''

    unigram_count_dict = collections.defaultdict(int)
    with open(input_file, 'r') as input_stream:
        line = input_stream.readline()
        while line:
            split_line = line[:-1].split(' ')
            for token in split_line:
                unigram_count_dict[token] += 1
            line = input_stream.readline()

    with open(output_file, 'wb') as output:
        pickle.dump(unigram_count_dict, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    ''' loads object file using pickle '''
    with open(filename, 'rb') as object_file_stream:
        return pickle.load(object_file_stream)

def get_token_count(gram_dict):
    ''' returns number of tokens in gram dict '''
    return sum(gram_dict.values())

def get_type_count(gram_dict):
    ''' returns number of types in gram dict '''
    return len(gram_dict.values())

def plot_rank_freq(gram_dict):
    ''' generates a log frequence/rank plot '''
    freqs = gram_dict.values()
    freqs.sort(reverse=True)
    ranks = range(1, len(freqs)+1)
    plt.plot(ranks, freqs)
    plt.ylabel('log(frequency)')
    plt.xlabel('log(rank)')
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig('rand_freq.png')
    #plt.show()

def unigram_list_sorter(gram_dict):
    ''' returns a reversed sorted 2d unigram list '''
    unigram_list = list()
    for types in gram_dict:
        unigram_list.append([gram_dict[types], types])
    unigram_list.sort(reverse=True, key=lambda pair: pair[0])
    return unigram_list

def remove_stopwords_from_list(unigram_list):
    ''' takes list of tokens as output by unigram_list_sorter
    and removes english_stopwords from the list, returns list '''
    english_stopwords = stopwords.words('english')
    no_stopword_list = [pair for pair in unigram_list
                        if pair[1].lower() not in english_stopwords]
    return no_stopword_list

def int_dd():
    ''' pickle needs 'module level' functions
    to opperate. This simply allows for the use
    of pickle on an embedded defaultdict'''
    return collections.defaultdict(int)

def file_to_bigram_dict(input_file='nltk_tokenized.txt',
                        output_file='bigram_count_dict.pkl'):

    ''' Truns space seperated corpus file into embedded defaultdict
    bigram lookup. Saves object to disk using pickel '''

    # pickle will need module level functions
    bigram_count_dict = collections.defaultdict(int_dd)
    with open(input_file, 'r') as input_stream:
        line = input_stream.readline()
        while line:
            split_line = line[:-1].split(' ')
            for i in range(len(split_line)-1):
                bigram_count_dict[split_line[i]][split_line[i+1]] += 1
            line = input_stream.readline()

    with open(output_file, 'wb') as output:
        pickle.dump(bigram_count_dict, output, pickle.HIGHEST_PROTOCOL)

def get_unigram_probabilities(gram_dict, threshold=0):

    ''' takes unigram_dict and returns dict of
    unigram probabilities, pass to gram_dict sorter '''

    unigram_prob_dict = collections.defaultdict(float)
    total_token_count = float(get_token_count(gram_dict))

    for token_type in gram_dict:
        if gram_dict[token_type] > threshold:
            prob = float(gram_dict[token_type])/total_token_count
            unigram_prob_dict[token_type] = prob

    return unigram_prob_dict

def get_bigram_probabilities(bigram_dict, threshold=0):

    ''' Takes embedded bigram defaultdict and returns the same
    datat structure filled with the bigram probabilities'''

    bigram_prob_dict = collections.defaultdict(int_dd)
    for previous_token in bigram_dict:
        prev_prob = get_unigram_probabilities(bigram_dict[previous_token],
                                              threshold)
        bigram_prob_dict[previous_token] = prev_prob

    return bigram_prob_dict

def get_pmi(input_bigram='bigram_count_dict.pkl',
            input_unigram='unigram_count_dict.pkl',
            threshold=0):

    ''' description of the function goes here'''

    print 'Loading Objects'
    bigram_count_dict = load_object(input_bigram)
    unigram_count_dict = load_object(input_unigram)

    print 'building probabilities'
    bigram_prob_dict = get_bigram_probabilities(bigram_count_dict, threshold)
    unigram_prob_dict = get_unigram_probabilities(unigram_count_dict)

    print 'Building List'
    pmi_list = list()

    for history in bigram_prob_dict:
        for token in bigram_prob_dict[history]:
            pmi = bigram_prob_dict[history][token]/unigram_prob_dict[token]
            pmi_list.append([pmi, history, token])
            #print history, token
    pmi_list.sort(reverse=True, key=lambda pair: pair[0])
    return pmi_list



def main():

    ### WORD COUNTING & DISTRIBUTION ###

    # QUESTIONS 1 and 2
    file_to_unigram_dict()
    unigram_count_dict = load_object('unigram_count_dict.pkl')
    unique_types = get_type_count(unigram_count_dict)
    unique_tokens = get_token_count(unigram_count_dict)

    print 'The number of unique types is ', str(unique_types)
    print 'The number of unique tokens is ', str(unique_tokens)

    # QUESTION 3
    plot_rank_freq(unigram_count_dict)

    # QUESTION 4
    unigram_list = unigram_list_sorter(unigram_count_dict)
    print "The 20 most common words are: "
    for index in range(20): print unigram_list[index]

    # QUESTIONS 5 & 6
    unigram_list_no_stopwords = remove_stopwords_from_list(unigram_list)
    print "The 20 most common words after stopword removal are: "
    for index in range(20): print unigram_list_no_stopwords[index]

    ### WORD ASSOCIATION METRICS ###
    file_to_bigram_dict()

    pmi_list_thresh_0 = get_pmi()
    print "The 30 highest PMI pairs with threshold 0 are: "
    for index in range(30): print pmi_list_thresh_0[index]


    pmi_list_thresh_100 = get_pmi(threshold=100)
    print "The 30 highest PMI pairs with threshold 100 are: "
    for index in range(30): print pmi_list_thresh_100[index]

    for pmi_itter in pmi_list_thresh_0:
        if pmi_itter[1] == 'NEW' and pmi_itter[2] == 'YORK':
            print pmi_itter



if __name__ == "__main__":
    main()
