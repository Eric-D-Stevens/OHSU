#!/usr/bin/env python
# model1.py: Model 1 translation table estimation
# Steven Bedrick <bedricks@ohsu.edu> and Kyle Gorman <gormanky@ohsu.edu>


import numpy as np
from collections import defaultdict

def bitext(source, target):
    """
    Run through the bitext files, yielding one sentence at a time
    """
    for (s, t) in zip(source, target):
        yield ([None] + s.strip().split(), t.strip().split())
        # by convention, only target-side tokens may be aligned to a null
        # symbol (here represented with None) on the source side


class Model1(object):
    """
    IBM Model 1 translation table
    """

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __init__(self, source, target):

        print('--------------- Building Object ---------------')
        print('Source File:', source)
        print('Target File:', target)
        print()

        # add filenames to class
        self.source = source
        self.target = target

        # storage arrays
        self.P = defaultdict(lambda: defaultdict(np.float64))

        i = 0

        # initalize P with counts
        with open(self.source) as S_src:
            with open(self.target) as  T_src:
                #for s in S
                gen = bitext(S_src,T_src)
                for S,T in gen:
                    i += 1 # track progress
                    if not i % 10000: print('At pair:',i)
                    for s in S:
                        for t in T:
                            self.P[s][t] += 1.0
        print('Total:',i,'pairs\n')

        # Normalization of P for probabilities
        Plen = len(self.P)
        print('Normalizing over',Plen,'source words.')
        for s in self.P:
            count = sum(self.P[s].values())
            for t in self.P[s]:
                self.P[s][t] /= count
        print('Initalization Complete')



    def train(self, n):
        """
        Perform n iterations of EM training
        """
        print('--------------- Begin Training ---------------\n')
        for _ in range(n):
            print('########## Iteration:',_+1, '##########')

            # reinitialize each epoch (match slide simple example)
            self.a = defaultdict(lambda: defaultdict(np.float64))
            self.T = defaultdict(np.float64)

            # use file streams
            with open(self.source) as S_src:
                with open(self.target) as  T_src:

                    # generator object
                    gen = bitext(S_src,T_src)

                    # track progress
                    i=0

                    # for Source Target sentences in the files
                    for S,T in gen:
                        i += 1 # track progress
                        if not i % 10000: print('At pair:',i)

                        # build up a and T
                        for s in S:
                            for t in T:
                                self.a[s][t] += self.P[s][t]
                                self.T[t] += self.P[s][t]


            # set P(t|s) = a(s,t)/T(t)
            print('\nUpdating P(t|s)')
            for s in self.a:
                for t in self.a[s]:
                    self.P[s][t] = self.a[s][t]/self.T[t]
            print('Normalizing over P(t|s)')
            for s in self.P:
                count = sum(self.P[s].values())
                for t in  self.P[s]:
                    self.P[s][t] /= count
            print()
        print('--------------- Training Complete ---------------')


    def get_word_translation(self, word):
        ''' returns the translation of 'word' '''
        key_max = max(self.P[word].keys(), key=(lambda k: self.P[word][k]))
        return key_max



if __name__ == '__main__':
    import doctest
    doctest.testmod()

