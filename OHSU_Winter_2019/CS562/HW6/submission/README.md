
# CS 562 Homework 6: The Probabilistic CKY Parsing Algorithm
### Eric D. Stevens
### March 4, 2019


```python
import tree
from importlib import reload
from collections import defaultdict
import numpy as np
from IPython.display import HTML, display
```

## 1. PCFG Generation

### 1.1 Program

For this entire assignment I found it easier and more elegant to modify the `Tree` class rather than making indeppendent code. Since it is sesired to check the logic of the PCFG generation against the provided example before moving on to creating a larger PCFG from an eitire corpus, two methods are implemnted in this section. The first is an implementation of the PCFG builder as a member function '`Tree`. This can be called on any `Tree` object with now arguments. The second version is class method that will create the PCFG from a file stream using the `from_stream` functions implemented in HW5. Both of these methods will return an object of type `defalutdict{defaultdict{non-terminal: daughters}}`.

#### 1.1.1 Member function for single tree to PCFG


```python
''' This code should not be run in the notebook. The code
here is just a compiled version of my work, seperated form 
the rest of the code for easy viewing. See how the code is
utilized in the following section.'''


    def MLE_PCFG(self):
        '''
        This method allows operates on a Tree object and returns
        the MLE PCFG that is generated form the UC CNF from of the
        tree.
        '''

        def recur_bigram_cnt(self, def_dict):
            '''
            This locally defined method operates on a tree.
            It creates the counts for the PCFG recursivly.
            After this function is called the probabilites
            can be derived from the returned embedded dd.
            '''

            '''If a daughter is terminal all it is the only daughter
            in CNF so store increment the the value with the terminal
            string as the key'''


            if Tree.terminal(self.daughters[0]):
                for d in self.daughters:
                    def_dict[self.label][d] += 1.0
                return def_dict

            else:
                dots = tuple(d.label for d in self.daughters)
                def_dict[self.label][dots] += 1.0
                for d in self.daughters:
                    recur_bigram_cnt(d, def_dict)
                return def_dict

        # 2nd order default dict: data structure to be passed to the function above

        def_dict = defaultdict(lambda: defaultdict(float))

        # call above defined recursive function and store values in dict
        recur_bigram_cnt(self, def_dict)

        # sum the counts each branch and use that to divide them into probs
        for prior in def_dict:
            total = sum(def_dict[prior].values())
            for term in def_dict[prior]:
                def_dict[prior][term] /= total
                # print the values
                #print(prior,'->', term, def_dict[prior][term])#, total)

        # def_dict is now a PCFG for the Tree object
        return def_dict



```

#### 1.1.2 Class method for stream to PCFG


```python
''' This code should not be run in the notebook. The code
here is just a compiled version of my work, seperated form 
the rest of the code for easy viewing. See how the code is
utilized in the following section.'''

    @classmethod
    def MLE_PCFG_from_stream(cls, handle, modified=False):
        '''
        This method takes as an input the file name of a .psd
        file to generate an MLE PCFG from. the 'modified' 
        paramater is set to true if it is desired to use the
        modified stream to Tree function form assignment 5.
        '''


        def recur_bigram_cnt(self, def_dict):
            '''see implementation notes in the MLE_PCFG function'''

            if Tree.terminal(self.daughters[0]):
                for d in self.daughters:
                    def_dict[self.label][d] += 1.0
                return def_dict
            else:
                dots = tuple(d.label for d in self.daughters)
                def_dict[self.label][dots] += 1.0
                for d in self.daughters:
                    recur_bigram_cnt(d, def_dict)
                return def_dict


        # declare a dict for results to be stored in
        def_dict = defaultdict(lambda: defaultdict(float))

        # open file stream
        with open(handle) as stream:
            if modified:
                gen = Tree.from_stream_modified(stream)
            else:
                gen = Tree.from_stream(stream)
            for tr in gen:
                tr.collapse_unary().chomsky_normal_form()

                # call above defined recursive function and store values in dict
                recur_bigram_cnt(tr, def_dict)

        # sum the counts each branch and use that to divide them into probs
        for prior in def_dict:
            total = sum(def_dict[prior].values())
            for term in def_dict[prior]:
                def_dict[prior][term] /= total

        return def_dict
```

### 1.2 Usage

#### 1.2.1 Using the member function for tree to PCFG converstion

First we need to generate a tree. We will do so from the string provided with the asignment description.


```python

# irst we need to generate a tree.
tree_string = """
(TOP
    (NP
      (DT the)
      (NN teacher)
    )
    (VP
      (MD will)
      (VP
        (VB lecture)
        (NP
          (NN today)
                  (PP
          (IN in)
          (NP
            (DT the)
            (NN lecture)
            (NN hall)
          )
        )


        )
      )
    )
    (. .)
)
"""

tree_object = tree.Tree.from_string(tree_string)
print(tree_object)
```

    (TOP
        (NP
            (DT the)
            (NN teacher)
        )
        (VP
            (MD will)
            (VP
                (VB lecture)
                (NP
                    (NN today)
                    (PP
                        (IN in)
                        (NP
                            (DT the)
                            (NN lecture)
                            (NN hall)
                        )
                    )
                )
            )
        )
        (. .)
    )


Now, to build the PCFG we can simply call the member function on the tree object.


```python
PCFG_from_treee = tree_object.MLE_PCFG()
PCFG_from_treee
```




    defaultdict(<function tree.Tree.MLE_PCFG.<locals>.<lambda>()>,
                {'TOP': defaultdict(float, {('NP', 'TOP|<VP&.>'): 1.0}),
                 'NP': defaultdict(float,
                             {('DT', 'NN'): 0.3333333333333333,
                              ('NN', 'PP'): 0.3333333333333333,
                              ('DT', 'NP|<NN&NN>'): 0.3333333333333333}),
                 'DT': defaultdict(float, {'the': 1.0}),
                 'NN': defaultdict(float,
                             {'teacher': 0.25,
                              'today': 0.25,
                              'lecture': 0.25,
                              'hall': 0.25}),
                 'TOP|<VP&.>': defaultdict(float, {('VP', '.'): 1.0}),
                 'VP': defaultdict(float, {('MD', 'VP'): 0.5, ('VB', 'NP'): 0.5}),
                 'MD': defaultdict(float, {'will': 1.0}),
                 'VB': defaultdict(float, {'lecture': 1.0}),
                 'PP': defaultdict(float, {('IN', 'NP'): 1.0}),
                 'IN': defaultdict(float, {'in': 1.0}),
                 'NP|<NN&NN>': defaultdict(float, {('NN', 'NN'): 1.0}),
                 '.': defaultdict(float, {'.': 1.0})})



#### 1.2.2  Using the file stream to PCFG class method

Assuming you have access to a file that is formatted in the proper way, it is even easier to use the PCFG from stream class method. The only parameter needed is the file name.


```python
WSJ_normalized_PCFG = tree.Tree.MLE_PCFG_from_stream('wsj-normalized.psd', modified=True)
```

    reached end of file


The `modified` keyword in above tells the system to use the more efficent version of `Tree.from_stream()` that I worte for assignment 5. If it is not set then the original `Tree.from_stream()` will be used. 

Now we can examine some of results form creating the PCFG from this large of a file.


```python
WSJ_normalized_PCFG['TOP|<VP&.>']
```




    defaultdict(float,
                {('VP', '.'): 0.9341827625385489,
                 ('VP', "TOP|<.&''>"): 0.062408699886382084,
                 ('VP', 'TOP|<.&-RRB->'): 0.0033273819185197207,
                 ('VP', 'TOP|<.&``>'): 8.115565654926148e-05})




```python
WSJ_normalized_PCFG['CC']
```




    defaultdict(float,
                {'and': 0.7119595732734418,
                 'but': 0.16591802358225716,
                 'or': 0.06386861313868614,
                 '&': 0.046743402582818644,
                 'nor': 0.0030881527231892197,
                 'v.': 0.00014037057832678272,
                 'yet': 0.0022459292532285235,
                 'both': 0.001403705783267827,
                 'neither': 0.0007018528916339135,
                 'either': 0.0016844469399213925,
                 'plus': 0.0012633352049410444,
                 'times': 0.00014037057832678272,
                 "'n": 0.00014037057832678272,
                 'whether': 0.00028074115665356543,
                 'vs.': 0.0004211117349803481})



### 1.3 Methodology 

This it seemed elegant to use extend the tree class rather than build a free standing method. Since the PCFG generations will rely so heavily on the `Tree` class anyway. I am using my own code from assignment number 5 under the possibly false assumption that it is working correctly. 

For the PCGE gereration, it seemed that recursivly traversing the tree until hitting terminals was the way to go. The data structure used to hold the probabilites is a double embedded default dict. In the recursive iterations a count is incremented at each occourance. After the tree has been traversed across completly, the counts are devided by their totals to make the values represent the probabilities of thier occourance given that higher order nonterminal. 

### 1.4 Counts

To count the total number of rules, we loop through each nonterminal in the grammer and count all the rewrites that can be derived from it. Summing these values together will be the total number of rewrite rules in the grammer.


```python
counts = 0

# loop through each non terminal and count its rules
for NT in WSJ_normalized_PCFG:
    counts += len(WSJ_normalized_PCFG[NT])

counts
```




    30363



##### Number of total rules: 30,363



## 2. Probabilistic CKY

### 2.1 Program

The implementation of the Probabalistic CKY algorithm was done with the use of a new class, also sitting in my `tree.py` file. 


```python
''' This code should not be run in the notebook. The code
here is just a compiled version of my work, seperated form 
the rest of the code for easy viewing. See how the code is
utilized in the following section.'''

class prob_CKY():

    def __init__(self, sentence, grammer):

        # localize variables
        self.sentence = sentence
        self.grammer = grammer

        # init word list
        self.word_list = sentence.split(' ')
        num_words = len(self.word_list)

        # declare probability table and backtrace table
        self.table = [[defaultdict(float) for i in range(num_words)] for j in range(num_words)]
        self.back_trace = [[defaultdict(str) for i in range(num_words)] for j in range(num_words)]

        # initalize diagonal of probability table
        for diag in range(num_words):
            for ctx in grammer:
                if grammer[ctx][self.word_list[diag]] > 0:
                    self.table[diag][diag][ctx] = grammer[ctx][self.word_list[diag]]
                    self.back_trace[diag][diag][ctx] = self.word_list[diag]

        # traverse table left to right but up the columns first
        for j in range(1,num_words):
            for i in reversed(range(j)):

                # k will be the offset for examining other branching cells
                for k in range(i,j):

                    # for every nonterminal in the grammer
                    for A in dict(grammer):

                        # for every two way branch in  each grammer
                        for tup in dict(grammer[A]):
                            if type(tup) == tuple and len(tup)==2:
                                (B,C) = tup

                                #print(self.table[i][k][B], self.table[k][j][C], (i,j,k))
                                if self.table[i][k][B] > 0 and self.table[k+1][j][C] > 0:
                                    #print('gtz met')
                                    #print(self.table[i][k][B], self.table[k+1][j][C], )
                                    if self.table[i][j][A] < grammer[A][(B,C)]*self.table[i][k][B]*self.table[k+1][j][C]:
                                        #print('conditions met')
                                        self.table[i][j][A] = grammer[A][(B,C)]*self.table[i][k][B]*self.table[k+1][j][C]
                                        #print(B,C)
                                        self.back_trace[i][j][A] = (k+1,(B,C))
```

The class constructor takes a string to parse and a grammer in PCFG as inputs. It uses the grammer to generate a memoization array and a backtrace array. After the arrays are created, member functions can be called to actually perform the backtrace and output the parse as a tree. This function is a member function called `to_tree()`.


```python
''' This code should not be run in the notebook. The code
here is just a compiled version of my work, seperated form 
the rest of the code for easy viewing. See how the code is
utilized in the following section.'''

    def parse_successful(self):
        num_words = len(self.word_list)
        if self.table[0][num_words-1]['TOP'] > 0:
            return self.table[0][num_words-1]['TOP']
        else:
            return False


    def trace_to_tree(self, symbol, position):
        #print(back_trace_table)
        try:
            (k,(B,C)) = self.back_trace[position[0]][position[1]][symbol]
            L = self.trace_to_tree(B,(position[0],k-1))
            R = self.trace_to_tree(C,(k,position[1]))
            parse_tree = Tree(symbol,[L,R])
        except:
            word = self.back_trace[position[0]][position[1]][symbol]
            parse_tree = Tree(symbol,[word])

        return parse_tree

    def to_tree(self):
        size = len(self.back_trace)
        parse_tree = self.trace_to_tree('TOP', (0,size-1))
        return parse_tree
```

As can be seen above there are three member functions of interest there. The `parse_successful()` function returns the probability of the parse if there is one and returns `False` if a parse is not found. The `trace_to_tree()` function is a helper to the `to_tree()` function for recursive constuction of a parse tree form the backtrace array. Calling `to_tree()` on a `prob_CKY` object will return a `Tree` class object that is the parse of the input sentence.

Finally a print function was implemented that outputs the memoization table and/or the backtrace array in an HTML table. This allows for easy viewing of where things are going wrong. I used it to understand the algorithm better.

''' This code should not be run in the notebook. The code
here is just a compiled version of my work, seperated form 
the rest of the code for easy viewing. See how the code is
utilized in the following section.'''   
    
    def print_table(self, back = False, only=False):

        if not only:
            display(HTML(
               '<table><tr>{}</tr></table>'.format(
                   '</tr><tr>'.join(
                       '<td>{}</td>'.format('</td><td>'.join(str(dict(_)) for _ in row)) for row in self.table)
                   )
            ))

        if back:
            display(HTML(
               '<table><tr>{}</tr></table>'.format(
                   '</tr><tr>'.join(
                       '<td>{}</td>'.format('</td><td>'.join(str(dict(_)) for _ in row)) for row in self.back_trace)
                   )
            ))





### 2.2 Usage

#### 2.2.1 Usage on small provided example for demonstration of concept

Lets demonstrate the functionality on the small example we were provided with. Remember that we currently have `PCFG_from_tree` that we generated from the string `tree_object` which in turn came from `tree_sting`. Lets show these again for the sake of the demonstrateion.


```python
tree_object
```




    (TOP
        (NP
            (DT the)
            (NN teacher)
        )
        (TOP|<VP&.>
            (VP
                (MD will)
                (VP
                    (VB lecture)
                    (NP
                        (NN today)
                        (PP
                            (IN in)
                            (NP
                                (DT the)
                                (NP|<NN&NN>
                                    (NN lecture)
                                    (NN hall)
                                )
                            )
                        )
                    )
                )
            )
            (. .)
        )
    )




```python
PCFG_from_treee
```




    defaultdict(<function tree.Tree.MLE_PCFG.<locals>.<lambda>()>,
                {'TOP': defaultdict(float, {('NP', 'TOP|<VP&.>'): 1.0}),
                 'NP': defaultdict(float,
                             {('DT', 'NN'): 0.3333333333333333,
                              ('NN', 'PP'): 0.3333333333333333,
                              ('DT', 'NP|<NN&NN>'): 0.3333333333333333}),
                 'DT': defaultdict(float, {'the': 1.0}),
                 'NN': defaultdict(float,
                             {'teacher': 0.25,
                              'today': 0.25,
                              'lecture': 0.25,
                              'hall': 0.25}),
                 'TOP|<VP&.>': defaultdict(float, {('VP', '.'): 1.0}),
                 'VP': defaultdict(float, {('MD', 'VP'): 0.5, ('VB', 'NP'): 0.5}),
                 'MD': defaultdict(float, {'will': 1.0}),
                 'VB': defaultdict(float, {'lecture': 1.0}),
                 'PP': defaultdict(float, {('IN', 'NP'): 1.0}),
                 'IN': defaultdict(float, {'in': 1.0}),
                 'NP|<NN&NN>': defaultdict(float, {('NN', 'NN'): 1.0}),
                 '.': defaultdict(float, {'.': 1.0})})



I have also added a small member function to the `Tree` class that extracts the origional string form the parse tree.


```python
original_string = tree_object.to_string()
print(original_string)
```

    the teacher will lecture today in the lecture hall .


Now we can feed the string and the grammer into the `prob_CKY()` constructor, and test whether it was parsed succesfully.


```python
PCKY = tree.prob_CKY(original_string, PCFG_from_treee)
PCKY.parse_successful()
```




    3.616898148148148e-05



The fact that a value was returned from the `parse_successful()` function means that a result was found. We can now have a look at the resulting parse tree.


```python
PCKY.to_tree()
```




    (TOP
        (NP
            (DT the)
            (NN teacher)
        )
        (TOP|<VP&.>
            (VP
                (MD will)
                (VP
                    (VB lecture)
                    (NP
                        (NN today)
                        (PP
                            (IN in)
                            (NP
                                (DT the)
                                (NP|<NN&NN>
                                    (NN lecture)
                                    (NN hall)
                                )
                            )
                        )
                    )
                )
            )
            (. .)
        )
    )



It is the same as our input because the only grammer rules were very specific and forced the sentence back into the shape of the small grammer. 

Now, using the `print_table()` function we can examine our memoization table and our backtrace table.

#### Memoization Table


```python
PCKY.print_table()
```


<table><tr><td>{'DT': 1.0, 'NP': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.08333333333333333, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'TOP': 3.616898148148148e-05}</td></tr><tr><td>{}</td><td>{'NN': 0.25, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0}</td></tr><tr><td>{}</td><td>{}</td><td>{'MD': 1.0, 'PP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'VP': 0.001736111111111111, 'PP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0, 'NP': 0.0, 'DT': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'VP': 0.00043402777777777775, 'PP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0, 'NP': 0.0, 'DT': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'TOP|<VP&.>': 0.00043402777777777775, 'PP': 0.0, 'NN': 0.0}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{'NN': 0.25, 'VB': 1.0, 'VP': 0.0, 'NP': 0.0, 'DT': 0.0, 'MD': 0.0, 'IN': 0.0}</td><td>{'NP|<NN&NN>': 0.0625, 'VP': 0.0, 'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'VP': 0.0, 'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'VP': 0.0, 'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'VP': 0.003472222222222222, 'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'VP': 0.0008680555555555555, 'NP': 0.0, 'DT': 0.0, 'NN': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'TOP|<VP&.>': 0.0008680555555555555, 'VP': 0.0}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'NN': 0.25, 'PP': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NP': 0.0, 'NN': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NP': 0.0, 'NN': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.006944444444444444, 'PP': 0.0, 'NN': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.001736111111111111, 'PP': 0.0, 'NN': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NP': 0.0, 'NN': 0.0}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'IN': 1.0, 'PP': 0.0, 'NN': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0}</td><td>{'PP': 0.0, 'NN': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.08333333333333333, 'NN': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.020833333333333332, 'NN': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NN': 0.0}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'DT': 1.0, 'NP': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.08333333333333333, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.020833333333333332, 'DT': 0.0, 'NN': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NP': 0.0}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'NN': 0.25, 'VB': 1.0, 'NP|<NN&NN>': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'IN': 0.0}</td><td>{'NP|<NN&NN>': 0.0625, 'NN': 0.0, 'NP': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'NN': 0.0, 'NP|<NN&NN>': 0.0}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'NN': 0.25, 'PP': 0.0, 'NP': 0.0, 'TOP|<VP&.>': 0.0, '.': 0.0, 'DT': 0.0, 'VP': 0.0, 'MD': 0.0, 'VB': 0.0, 'IN': 0.0}</td><td>{'PP': 0.0, 'NP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0, '.': 0.0}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'.': 1.0, 'PP': 0.0, 'NN': 0.0, 'TOP|<VP&.>': 0.0}</td></tr></table>


#### Backtrace Table


```python
PCKY.print_table(back=True, only=True)
```


<table><tr><td>{'DT': 'the'}</td><td>{'NP': (1, ('DT', 'NN'))}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'TOP': (2, ('NP', 'TOP|<VP&.>'))}</td></tr><tr><td>{}</td><td>{'NN': 'teacher'}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td><td>{'MD': 'will'}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'VP': (3, ('MD', 'VP'))}</td><td>{'VP': (3, ('MD', 'VP'))}</td><td>{'TOP|<VP&.>': (9, ('VP', '.'))}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{'NN': 'lecture', 'VB': 'lecture'}</td><td>{'NP|<NN&NN>': (4, ('NN', 'NN'))}</td><td>{}</td><td>{}</td><td>{'VP': (4, ('VB', 'NP'))}</td><td>{'VP': (4, ('VB', 'NP'))}</td><td>{'TOP|<VP&.>': (9, ('VP', '.'))}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'NN': 'today'}</td><td>{}</td><td>{}</td><td>{'NP': (5, ('NN', 'PP'))}</td><td>{'NP': (5, ('NN', 'PP'))}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'IN': 'in'}</td><td>{}</td><td>{'PP': (6, ('IN', 'NP'))}</td><td>{'PP': (6, ('IN', 'NP'))}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'DT': 'the'}</td><td>{'NP': (7, ('DT', 'NN'))}</td><td>{'NP': (7, ('DT', 'NP|<NN&NN>'))}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'NN': 'lecture', 'VB': 'lecture'}</td><td>{'NP|<NN&NN>': (8, ('NN', 'NN'))}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'NN': 'hall'}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'.': '.'}</td></tr></table>



#### 2.2.2 General usage with large grammers

Now in the instance we want to use a large grammer to parse a sentence that we do not have a parse for yet, we can do essentially the same exact thing, feeding a larger grammer into the `prob_CKY()` constructor.

Remember earlier we created a grammer from the `wsj-normalized.psd` file `WSJ_normalized_PCFG`. Lets use this grammer to build a parse tree for some input sentence.

Now lets use this grammer to build a parse tree for some input sentence.


```python
input_string = 'this effort was a great success .'
new_CKY = tree.prob_CKY(input_string, WSJ_normalized_PCFG)
new_CKY.parse_successful()
```




    2.671988966174452e-17



As we can see our `parse_successful()` function returned a probability, and therfore our parse was a success. Lets perform the backtrace to and get our tree.


```python
parsed_sentence = new_CKY.to_tree()
parsed_sentence
```




    (TOP
        (NP-SBJ
            (DT this)
            (NN effort)
        )
        (TOP|<VP&.>
            (VP
                (VBD was)
                (NP
                    (DT a)
                    (NP|<JJ&NN>
                        (JJ great)
                        (NN success)
                    )
                )
            )
            (. .)
        )
    )



As we can see, this effort was a great success.

### 2.3  Methodolgy

I found the implementation of the of the CKY algorithm very difficult to understand. I know there are currently some inefficiences in my implementation but I am afraid to alter my seemingly working implementation. I think that these inefficencies come from the fact that the implementation that if followed did not assume the availability of a default dict. In a situation where you are using arrays of objects, it takes the same amount of time to search as it would to itterate over each object in the array and take action on that object if needed. Since dictonaries are hashmaps, implementaion could have possibly been sped up by only searching through the nonterminals contained in the (k,j) and (i,k) indecies, rather than iterating over all of the nonterminals in the vocab.

I believe that this distinction causes massive slow downs due to the way a default dict works. Each time an item is queried that does not currently exist in a default dict, it creates an entry for that query and sets it to zero. you can see this demonstrated below.


```python
# build the default dict
the_default_dict = defaultdict(float)
the_default_dict['hello'] = 1.11
the_default_dict['world']= 2.22
```


```python
# view the size of the default dict
len(the_default_dict)
```




    2




```python
# query for value that does not exist
the_default_dict['its me!']
```




    0.0




```python
# notice new lenght of default dict
len(the_default_dict)
```




    3



This is an unneccecary performance darain on our system. It will cost a huge ammount of memory for large grammers since hashmaps are implemented using concecutive memory as far as I know, this is causing massive massive delays for continual resizing. This could be avoided if I did not query the (k,j) and (i,k) indecies of the memoization table for all nonterminals in the grammer, but instead searched each nonterminal for a tuple made up of every combination of values in the (k,j) and (i,k) indecies. 

### 2.4 Counting successful parses of 'end_of_wsj.txt' using 'bigger_treebank_2.txt' grammer

For this section I will need to write some code. The opeartion of the code will be explained in comments within the code. This codeblock can be run from this notebook.



```python
# build the treebaknk grammer
TB_grammer = tree.Tree.MLE_PCFG_from_stream('bigger_treebank_2.txt')

# use the 'from_stream()' function from the tree class to pull trees from the 'end_of_wsj.txt' file
with open('end_of_wsj.txt') as stream:
    wsj = tree.Tree.from_stream(stream)
    
    # for every sample tree in the file
    for sample in wsj:
        i+=1
        # turn the tree into a string
        sample_string = sample.to_string()
        
        # perform Prb_CKY using TB_grammer
        cky = tree.prob_CKY(sample_string, TB_grammer)
        
        # show probabilities and boolean value to be written to file
        print(float(cky.parse_successful()), int(not (bool(cky.parse_successful()))))
        
        # write to file '0' if parse was a success, '1' if parsing failed
        with open('end_of_wsj_RESULTS.txt', 'a') as the_file:
            the_file.write(str(int(not (bool(cky.parse_successful()))))+'\n')
```

    0.0 1
    7.604384618538641e-30 0
    3.955329279632346e-62 0
    0.0 1
    0.0 1
    0.0 1
    0.0 1
    0.0 1
    0.0 1
    0.0 1
    2.5410182990623344e-18 0
    0.0 1
    3.269638248326755e-48 0
    0.0 1
    0.0 1
    0.0 1
    0.0 1
    0.0 1
    0.0 1
    0.0 1


As we can see, only 4 of the 21 or so provided trees actually parsed. A file called `end_of_wsj_RESULTS.txt` was written to as requested by the assignment.  It took over half of an hour for this to run.
