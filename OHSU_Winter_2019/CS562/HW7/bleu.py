#!/usr/bin/env python3 -O
# basic BLEU score implementation

from __future__ import division

from math import exp, log, pow
from collections import Counter


MAX_GRAM_SIZE = 4



# helpers

def ngrams(tokens, order):
    """
    Generate n-grams of order `order`, with no padding
    """
    for i in range(len(tokens) - order + 1):
        yield tuple(tokens[i:i + order])

def bitext(source, target):
    """
    Run through the bitext files, yielding one sentence at a time
    """
    for (s, t) in zip(source, target):
        yield (s.strip().split(), t.strip().split())
        # this time, we don't want a null symbol


def BLEU(hypothesis, reference, n=MAX_GRAM_SIZE):
    """
    Compute BLEU for a hypothesis/reference sentence pair
    """
    print("--------------- BLEU TRANSLATION SCORE ---------------\n")
    print("Candidate file:",hypothesis)
    print("Reference file:",reference)
    print()

    out_f_name = hypothesis+'.to.'+reference+'.bleu_scores'
    with open(out_f_name, 'w+') as out_file:
        out_file.write("--------------- BLEU TRANSLATION SCORE ---------------\n\n")
        out_file.write("Candidate file: "+hypothesis+"\n")
        out_file.write("Reference file: "+reference+"\n\n")


        with open(hypothesis) as cnd:
            with open(reference) as ref:
                gen = bitext(cnd, ref)

                sentence = 0
                for c, r in gen:

                    # sentence number
                    sentence+=1

                    # holds list
                    pn_list = []

                    # all grams for all ns in r
                    for nn in range(1,n+1):

                        # counters for grams
                        c_counts = Counter()
                        r_counts = Counter()

                        # count target grams
                        grm_gen = ngrams(r,nn)
                        for gm in grm_gen:
                            r_counts[gm] += 1

                        # modified count of source grams
                        grm_gen = ngrams(c,nn)
                        for gm in grm_gen:
                            if c_counts[gm]<r_counts[gm]:
                                c_counts[gm] += 1

                        # calc Pn from n-gram
                        pn_list.append(float(sum(c_counts.values()))/float(len(c)))


                    # geometric mean of 1-gram to n-gram
                    geo_mean = 1.0
                    for x in pn_list:
                        geo_mean *= x
                    geo_mean = pow(geo_mean, 1.0/float(MAX_GRAM_SIZE))

                    # final computation
                    BP = 1.0
                    if len(c) <= len(r):
                        BP = exp(1-(float(len(r))/float(len(c))))


                    print('Sentence', sentence, ':', BP*geo_mean)
                    out_file.write('Sentence'+str(sentence)+':'+str(BP*geo_mean)+'\n')
