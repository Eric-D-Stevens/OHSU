from  hw2_utils import constants 
import numpy as np

# deliverable 4.1
def get_token_type_ratio(counts):
    """
    Compute the ratio of tokens to types
    
    :param counts: bag of words feature for a song
    :returns: ratio of tokens to types
    :rtype float
    """

    return float(sum(counts.values()))/float(len(counts))

# deliverable 4.2
def concat_ttr_binned_features(data):
    """
    Add binned token-type ratio features to the observation represented by data
    
    :param data: Bag of words
    :returns: Bag of words, plus binned ttr features
    :rtype: dict
    """
    rat = get_token_type_ratio(data)

    new = {'**TTR_0_1**': 0,
    '**TTR_1_2**': 0,
    '**TTR_2_3**': 0,
    '**TTR_3_4**': 0,
    '**TTR_4_5**': 0,
    '**TTR_5_6**': 0,
    '**TTR_6_INF**': 0}

    data.update(new) 

    if rat > 0 and rat < 1: data['**TTR_0_1**'] = 1
    if rat >= 1 and rat < 2: data['**TTR_1_2**'] = 1
    if rat >= 2 and rat < 3: data['**TTR_2_3**'] = 1
    if rat >= 3 and rat < 4: data['**TTR_3_4**'] = 1
    if rat >= 4 and rat < 5: data['**TTR_4_5**'] = 1
    if rat >= 5 and rat < 6: data['**TTR_5_6**'] = 1
    elif rat >= 6: data['**TTR_6_INF**'] = 1

    return data
