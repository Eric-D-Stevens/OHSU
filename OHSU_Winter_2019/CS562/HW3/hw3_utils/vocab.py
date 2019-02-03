from collections import defaultdict
from itertools import count
import torch

BOS_SYM = '<BOS>'
EOS_SYM = '<EOS>'

def build_vocab(corpus):
    """
    Build an exhaustive character inventory for the corpus, and return dictionaries
    that can be used to map characters to indicies and vice-versa.
    
    Make sure to include BOS_SYM and EOS_SYM!
    
    :param corpus: a corpus, represented as an iterable of strings
    :returns: two dictionaries, one mapping characters to vocab indicies and another mapping idicies to characters.
    :rtype: dict-like object, dict-like object
    """

    char_to_index = {BOS_SYM:0, EOS_SYM:1}
    index_to_char = {0:BOS_SYM, 1:EOS_SYM}

    curr_ind = 2

    for doc in corpus:
        for character in list(doc):
            if character not in char_to_index:
                char_to_index[character] = curr_ind
                index_to_char[curr_ind] = character
                curr_ind += 1

    return char_to_index, index_to_char


def sentence_to_vector(s, vocab, pad_with_bos=False):
    """
    Turn a string, s, into a list of indicies in from `vocab`. 
    
    :param s: A string to turn into a vector
    :param vocab: the mapping from characters to indicies
    :param pad_with_bos: Pad the sentence with BOS_SYM/EOS_SYM markers
    :returns: a list of the character indicies found in `s`
    :rtype: list
    """

    if pad_with_bos:
        no_OS = [vocab[character] for character in s]
        return [vocab[BOS_SYM]]+no_OS+[vocab[EOS_SYM]]

    return [vocab[character] for character in s]


def sentence_to_tensor(s, vocab, pad_with_bos=False):
    """
    :param s: A string to turn into a tensor
    :param vocab: the mapping from characters to indicies
    :param pad_with_bos: Pad the sentence with BOS_SYM/EOS_SYM markers
    :returns: (1, n) tensor where n=len(s) and the values are character indicies
    :rtype: torch.Tensor
    """

    vect = sentence_to_vector(s, vocab, pad_with_bos)
    return torch.tensor([vect])

def build_label_vocab(labels):
    """
    Similar to build_vocab()- take a list of observed labels and return a pair of mappings to go from label to numeric index and back.
    
    The number of label indicies should be equal to the number of *distinct* labels that we see in our dataset.
    
    :param labels: a list of observed labels ("y" values)
    :returns: two dictionaries, one mapping label to indicies and the other mapping indicies to label
    :rtype: dict-like object, dict-like object
    """

    lab_to_index = {}
    index_to_lab = {}
    curr_ind = 0

    for lab in labels:
        if lab not in lab_to_index:
            lab_to_index[lab] = curr_ind
            index_to_lab[curr_ind] = lab
            curr_ind += 1

    return lab_to_index, index_to_lab


