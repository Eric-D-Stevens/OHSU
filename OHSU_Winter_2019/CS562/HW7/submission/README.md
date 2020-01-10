
# CS 562: Homework 7
### Eric D. Stevens
### March 14, 2019


```python
import model1
import bleu
```

## Part 1: IBM Model 1

### Code


```python
''' This code should not be run in the notebook, this is here only for demonstration purposes. 
Please use the modle1.py file to run this code '''

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


```


### Building the model

Here we call the model constructor with the file names of the parrallel text as parameters. Durring the initialization step, maximum likelihood estimation 'P(target_word|source_word)' is calculated. 


```python
Fr2Eng = model1.Model1('hansards.36.ca.f.tok','hansards.36.ca.e.tok')
```

    --------------- Building Object ---------------
    Source File: hansards.36.ca.f.tok
    Target File: hansards.36.ca.e.tok
    
    At pair: 10000
    At pair: 20000
    At pair: 30000
    At pair: 40000
    At pair: 50000
    At pair: 60000
    At pair: 70000
    At pair: 80000
    At pair: 90000
    At pair: 100000
    At pair: 110000
    At pair: 120000
    At pair: 130000
    At pair: 140000
    At pair: 150000
    At pair: 160000
    At pair: 170000
    At pair: 180000
    At pair: 190000
    At pair: 200000
    Total: 207688 pairs
    
    Normalizing over 50652 source words.
    Initalization Complete


### Training the model

Here we call the memberfunction 'train' with the number of epochs as a parameter.


```python
Fr2Eng.train(5)
```

    --------------- Begin Training ---------------
    
    ########## Iteration: 1 ##########
    At pair: 10000
    At pair: 20000
    At pair: 30000
    At pair: 40000
    At pair: 50000
    At pair: 60000
    At pair: 70000
    At pair: 80000
    At pair: 90000
    At pair: 100000
    At pair: 110000
    At pair: 120000
    At pair: 130000
    At pair: 140000
    At pair: 150000
    At pair: 160000
    At pair: 170000
    At pair: 180000
    At pair: 190000
    At pair: 200000
    
    Updating P(t|s)
    Normalizing over P(t|s)
    
    ########## Iteration: 2 ##########
    At pair: 10000
    At pair: 20000
    At pair: 30000
    At pair: 40000
    At pair: 50000
    At pair: 60000
    At pair: 70000
    At pair: 80000
    At pair: 90000
    At pair: 100000
    At pair: 110000
    At pair: 120000
    At pair: 130000
    At pair: 140000
    At pair: 150000
    At pair: 160000
    At pair: 170000
    At pair: 180000
    At pair: 190000
    At pair: 200000
    
    Updating P(t|s)
    Normalizing over P(t|s)
    
    ########## Iteration: 3 ##########
    At pair: 10000
    At pair: 20000
    At pair: 30000
    At pair: 40000
    At pair: 50000
    At pair: 60000
    At pair: 70000
    At pair: 80000
    At pair: 90000
    At pair: 100000
    At pair: 110000
    At pair: 120000
    At pair: 130000
    At pair: 140000
    At pair: 150000
    At pair: 160000
    At pair: 170000
    At pair: 180000
    At pair: 190000
    At pair: 200000
    
    Updating P(t|s)
    Normalizing over P(t|s)
    
    ########## Iteration: 4 ##########
    At pair: 10000
    At pair: 20000
    At pair: 30000
    At pair: 40000
    At pair: 50000
    At pair: 60000
    At pair: 70000
    At pair: 80000
    At pair: 90000
    At pair: 100000
    At pair: 110000
    At pair: 120000
    At pair: 130000
    At pair: 140000
    At pair: 150000
    At pair: 160000
    At pair: 170000
    At pair: 180000
    At pair: 190000
    At pair: 200000
    
    Updating P(t|s)
    Normalizing over P(t|s)
    
    ########## Iteration: 5 ##########
    At pair: 10000
    At pair: 20000
    At pair: 30000
    At pair: 40000
    At pair: 50000
    At pair: 60000
    At pair: 70000
    At pair: 80000
    At pair: 90000
    At pair: 100000
    At pair: 110000
    At pair: 120000
    At pair: 130000
    At pair: 140000
    At pair: 150000
    At pair: 160000
    At pair: 170000
    At pair: 180000
    At pair: 190000
    At pair: 200000
    
    Updating P(t|s)
    Normalizing over P(t|s)
    
    --------------- Training Complete ---------------


### Performing translation

Here we use the member function 'get_word_translation()' with a source word as a parameter. This function will return the translation of the source word based on the model. If the modle has been initalized but not been trained, the function will return the maximum likelihood estimation.

The usage of the function on its own is as follows:


```python
Fr2Eng.get_word_translation('COMITÉ')
```




    'COMMITTEE'



The following small script reads in a file of source words that are in a single word per line format. The script translates these words, wirtes the pairs of words to std out, and writes the pairs to the file 'f2ewords.txt'.


```python
# Turn file into word list (one word per line).
french_word_list = [line.rstrip() for line in open('fwords.txt')]

# Make translated word list using member function
english_word_list = [Fr2Eng.get_word_translation(fr_word) for fr_word in french_word_list]

# Print translations and write to file
with open('f2ewords.txt', 'w+') as f2e:
    for i in range(len(french_word_list)):
        two_words = '{:20s}{:20s}'.format(french_word_list[i], english_word_list[i])
        print(two_words)
        f2e.writelines('%s\n'%two_words)
    
```

    AFFAIRES            AFFAIRS             
    AMENDEMENT          AMENDMENT           
    AUTOCHTONES         ABORIGINALS         
    CHAMBRE             HOUSE               
    CHEF                CHIEF               
    COMITÉ              COMMITTEE           
    COMMERCE            TRADE               
    COMMUNES            COMMONS             
    DROITS              RIGHTS              
    DÉCLARATION         STATEMENT           
    DÉFENSE             DEFENCE             
    DÉVELOPPEMENT       DEVELOPMENT         
    ENFANTS             CHILDREN            
    FINANCES            FINANCE             
    FÉDÉRAL             FEDERAL             
    GENS                PEOPLE              
    GOUVERNEMENT        GOVERNMENT          
    GUERRE              WAR                 
    HISTOIRE            HISTORY             
    INTERNATIONALE      INTERNATIONALE      
    JUGE                JUDGE               
    MINISTÈRE           DEPARTMENT          
    MONDE               WORLD               
    NATIONALE           NATIONAL            
    PARLEMENT           PARLIAMENT          
    PAROLE              SPEAK               
    PARTIE              PART                
    PREMIER             PRIME               
    PREMIÈRE            FIRST               
    PROGRAMME           PROGRAM             
    PROJET              PROJECT             
    PROVINCE            PROVINCE            
    PRÉSIDENT           PRESIDENT           
    QUÉBEC              QUEBEC              
    RAISON              REASON              
    RAPPORT             REPORT              
    RESPONSABILITÉ      RESPONSIBILITY      
    RÉGIME              REGIME              
    RÉGION              REGION              
    RÉPONSE             ANSWER              
    SECTEUR             SECTOR              
    SERVICES            SERVICES            
    SOCIÉTÉ             SOCIETY             
    SÉCURITÉ            SECURITY            
    SÉNAT               SENATE              
    SÉNATEUR            SENATOR             
    TRAVAIL             LABOUR              
    ÉGALEMENT           EQUALLY             
    ÉTATS-UNIS          U.S.                
    ÉTUDE               STUDY               


### Thoughts

I am very impressed at how well this method works for single word translations. I found it to be simple and elegant. My approach involved using default dicts to build weighted counts and the normalizing those counts on each training epoch.

## Part 2: Bleu Evaluation

### Code


```python
''' This code should not be run in the notebook, this is here only for demonstration purposes. 
Please use the bleu.py file to run this code '''


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
        out_file.write("--------------- BLEU TRANSLATION SCORE ---------------\n")
        out_file.write("Candidate file: "+hypothesis+"\n")
        out_file.write("Reference file: "+reference+"\n")


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
                    out_file.write('Sentence'+str(sentence)+':'+str(BP*geo_mean))

```

### Running an evaluation on a candidate file and a reference file

To run the evaluation on the a candidate file with a reference file just use the `BLEU` function with the candidate and refence files as parameters respectivly.


```python
bleu.BLEU('gtranslate.tok','e.tok')
```

    --------------- BLEU TRANSLATION SCORE ---------------
    
    Candidate file: gtranslate.tok
    Reference file: e.tok
    
    Sentence 1 : 0.5317417453075524
    Sentence 2 : 0.26770931469758097
    Sentence 3 : 0.0
    Sentence 4 : 0.38071015414152043
    Sentence 5 : 0.3164918233231852
    Sentence 6 : 0.7623917462370566
    Sentence 7 : 0.21188540235493908
    Sentence 8 : 0.36156345106488474
    Sentence 9 : 0.5120035191736744
    Sentence 10 : 0.6017728944812497



```python
bleu.BLEU('systran.tok','e.tok')
```

    --------------- BLEU TRANSLATION SCORE ---------------
    
    Candidate file: systran.tok
    Reference file: e.tok
    
    Sentence 1 : 0.3600776854897997
    Sentence 2 : 0.2691662243112666
    Sentence 3 : 0.0
    Sentence 4 : 0.29730177875068026
    Sentence 5 : 0.24062491113147336
    Sentence 6 : 0.7659756237473674
    Sentence 7 : 0.40745500016423886
    Sentence 8 : 0.3696853394838423
    Sentence 9 : 0.33635856610148585
    Sentence 10 : 0.0


### Thoughts

The Bleu scores came out as expected. All of the scores are in between 1 and 0 as specified in the paper. One interesting outcome of the way that the score is calculated, I found, is that it seems that if there is ever an instance where no ngrams of a high order an be found, it forces the score of the entire gram to zero. This comes form the fact that we are using a geometric mean to average.

With the geometric mean, I found that it became problimatic to use the equation in the paper since there were instances where one would need to evaluate the log of 0. I solved thes by taking the product of all of the modified ngram percisions and taking the value to the power of one over the order of the highest ngram.
