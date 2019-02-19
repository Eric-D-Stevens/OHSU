
# CS 562 Homework 5: Tree Transformations
### Eric D. Stevens
### February 19, 2019




```python
from tree import Tree
import tree
from importlib import reload
from random import randint
```


## 1. Collapse unary productions

### 1.1 Program


```python
''' This code should not be run in the notebook. The code
here is just a compiled version of my work, seperated form 
the rest of the code for easy viewing. See how the code is
utilized in the following section.'''


def collapse_unary(self, join_char=CU_JOIN_CHAR):

    # For each head immediately below the root:
    for daughter in self.daughters:

        # If head is terminal, continue
        if Tree.terminal(daughter):
            continue

        # Recursively apply the function
        daughter.collapse_unary()

        # If head is non-unary, continue
        if not Tree.unary(daughter):
            continue

        # If head's only daughter is terminal, continue
        if Tree.terminal(daughter[0]):
            continue

        # If head's only granddaughter is unary and terminal, continue
        if Tree.terminal(daughter[0][0]):
            continue

        # Merge the only daughter's label and promote its daughters
        daughter.label = daughter.label+'+'+daughter[0].label
        daughter.daughters = daughter.daughters.pop()

    return self
```

### 1.2 Sample Outputs


```python
'''This simple script will randomly select an entry from the 
    wsj-normalized.psd corpus three times and output the results 
    of running the intended script on the entry'''

with open('wsj-normalized.psd') as stream:
    wsj = Tree.from_stream(stream)
    for i in range(3):
        for _ in range(randint(1,1000)):
            sample = next(wsj)
        stars = '*'*20
        print('%s EXAMPLE %d: %s \n\nInitial Read: %s' % (stars, (i+1), stars, stars))
        print(sample)
        print('\n\nUnary Collapse:  %s' % stars)
        sample.collapse_unary()
        print(sample)
        print('\n\n')
```

    ******************** EXAMPLE 1: ******************** 
    
    Initial Read: ********************
    (TOP
        (NP-SBJ
            (NNP <NNP>)
        )
        (VP
            (VBD was)
            (ADJP-PRD
                (JJ outraged)
            )
        )
        (. .)
    )
    
    
    Unary Collapse:  ********************
    (TOP
        (NP-SBJ
            (NNP <NNP>)
        )
        (VP
            (VBD was)
            (ADJP-PRD
                (JJ outraged)
            )
        )
        (. .)
    )
    
    
    
    ******************** EXAMPLE 2: ******************** 
    
    Initial Read: ********************
    (TOP
        (NP-SBJ
            (NP
                (NNP <NNP>)
                (POS 's)
            )
            (NNS regulators)
        )
        (VP
            (VBP have)
            (ADVP-TMP
                (IN since)
            )
            (VP
                (VBN tightened)
                (NP
                    (NP
                        (NNS controls)
                    )
                    (PP
                        (IN on)
                        (NP
                            (JJ index-related)
                            (NN stock)
                            (NNS purchases)
                        )
                    )
                )
            )
        )
        (. .)
    )
    
    
    Unary Collapse:  ********************
    (TOP
        (NP-SBJ
            (NP
                (NNP <NNP>)
                (POS 's)
            )
            (NNS regulators)
        )
        (VP
            (VBP have)
            (ADVP-TMP
                (IN since)
            )
            (VP
                (VBN tightened)
                (NP
                    (NP
                        (NNS controls)
                    )
                    (PP
                        (IN on)
                        (NP
                            (JJ index-related)
                            (NN stock)
                            (NNS purchases)
                        )
                    )
                )
            )
        )
        (. .)
    )
    
    
    
    ******************** EXAMPLE 3: ******************** 
    
    Initial Read: ********************
    (TOP
        (NP-SBJ
            (NP
                (DT the)
                (NNP <NNP>)
                (NNP <NNP>)
            )
            (PP
                (IN of)
                (NP
                    (NNP <NNP>)
                    (CC and)
                    (NNP <NNP>)
                )
            )
        )
        (VP
            (VBD ordered)
            (NP
                (NP
                    (DT an)
                    (NN investigation)
                )
                (PP
                    (IN of)
                    (NP
                        (NP
                            (DT the)
                            (JJ competitive)
                            (NN impact)
                        )
                        (PP
                            (IN of)
                            (NP
                                (NP
                                    (NP
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                        (POS 's)
                                    )
                                    (VBN planned)
                                    (NN acquisition)
                                )
                                (PP
                                    (IN of)
                                    (NP
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        (. .)
    )
    
    
    Unary Collapse:  ********************
    (TOP
        (NP-SBJ
            (NP
                (DT the)
                (NNP <NNP>)
                (NNP <NNP>)
            )
            (PP
                (IN of)
                (NP
                    (NNP <NNP>)
                    (CC and)
                    (NNP <NNP>)
                )
            )
        )
        (VP
            (VBD ordered)
            (NP
                (NP
                    (DT an)
                    (NN investigation)
                )
                (PP
                    (IN of)
                    (NP
                        (NP
                            (DT the)
                            (JJ competitive)
                            (NN impact)
                        )
                        (PP
                            (IN of)
                            (NP
                                (NP
                                    (NP
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                        (POS 's)
                                    )
                                    (VBN planned)
                                    (NN acquisition)
                                )
                                (PP
                                    (IN of)
                                    (NP
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                        (NNP <NNP>)
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        (. .)
    )
    
    
    


### 1.3 Summary

To implement the unary collapse function I simply followed the procedure laid out in the document itself. I am very surprised and the elegance and effectiveness of the recursive solution. This function uses a depth first search to look for places where it can collapse the tree. Since we are altering the object itself on the fly, there is really no need to return anything for this function other than for easy output. The accesses methods added to the class make working with the objects very easy in terms of getting elements and iterating through elements.

## 2. Chomsky normal form

### 2.1 Program


```python
''' This code should not be run in the notebook. The code
here is just a compiled version of my work, seperated form 
the rest of the code for easy viewing. See how the code is
utilized in the following section.'''

def chomsky_normal_form(self, markovize_char=MARKOVIZE_CHAR,
                        join_char=CNF_JOIN_CHAR,
                        left_delimiter=CNF_LEFT_DELIMITER,
                        right_delimiter=CNF_RIGHT_DELIMITER):

    # if head is terminal, return
    if Tree.terminal(self):
        return self

    # if there are two or less daughters and the daughters are not
    # terminal then recursivly call the function on each daughter.
    if len(self) <= 2:
        for daughter in self.daughters:
            if not Tree.terminal(daughter):
                Tree.chomsky_normal_form(daughter)

    # if there are more than two daughters, perform node insertion to put
    # tree in chomsky normal form.
    elif len(self) > 2:

        # get the last two daughters
        last_daughters = self.daughters[-2:]


        # create a new lable that is a combination of the lables of the
        # last two daughters of the head.
        ''' hacky regex method to remove extra characters'''
        right_label = findall(r"\|\<(.*?)\&", last_daughters[1].label)
        if right_label:
            new_label = '%s|<%s&%s>' % (self.label, last_daughters[0].label, right_label[0])
        else:
            new_label = '%s|<%s&%s>' % (self.label, last_daughters[0].label, last_daughters[1].label)

        # create tree whos head is the new label and whos daughters are the
        # last daughters of the head we are currently working on.
        node = Tree(new_label, last_daughters)

        # slice off last two daughters from current head and add newly
        # created tree as last daughter.
        self.daughters = self.daughters[:-2]
        self.append(node)

        # pass the current head back into the function incause there were
        # more than three daughters at the start time of operation.
        Tree.chomsky_normal_form(self)

    return(self)


```

## 2.2 Sample Outputs


```python
'''This simple script will randomly select an entry from the 
    wsj-normalized.psd corpus three times and output the results 
    of running the intended script on the entry'''

with open('wsj-normalized.psd') as stream:
    wsj = Tree.from_stream(stream)
    for i in range(3):
        for _ in range(randint(1,1000)):
            sample = next(wsj)
        
        stars = '*'*20
        print('%s EXAMPLE %d: %s \n\nInitial Read: %s' % (stars, (i+1), stars, stars))
        print(sample)
        print('\n\nChomsky Normal Form:  %s' % stars)
        sample.collapse_unary().chomsky_normal_form()
        print(sample)
        print('\n\n')
```

    ******************** EXAMPLE 1: ******************** 
    
    Initial Read: ********************
    (TOP
        (CC but)
        (NP-SBJ
            (NN civilization)
        )
        (VP
            (VBZ has)
            (VP
                (VBN moved)
                (ADVP-DIR
                    (RB forward)
                )
                (PP-TMP
                    (IN since)
                    (NP
                        (RB then)
                    )
                )
            )
        )
        (. .)
    )
    
    
    Chomsky Normal Form:  ********************
    (TOP
        (CC but)
        (TOP|<NP-SBJ&VP>
            (NP-SBJ
                (NN civilization)
            )
            (TOP|<VP&.>
                (VP
                    (VBZ has)
                    (VP
                        (VBN moved)
                        (VP|<ADVP-DIR&PP-TMP>
                            (ADVP-DIR
                                (RB forward)
                            )
                            (PP-TMP
                                (IN since)
                                (NP
                                    (RB then)
                                )
                            )
                        )
                    )
                )
                (. .)
            )
        )
    )
    
    
    
    ******************** EXAMPLE 2: ******************** 
    
    Initial Read: ********************
    (TOP
        (NNP <NNP>)
        (NNPS <NNPS>)
    )
    
    
    Chomsky Normal Form:  ********************
    (TOP
        (NNP <NNP>)
        (NNPS <NNPS>)
    )
    
    
    
    ******************** EXAMPLE 3: ******************** 
    
    Initial Read: ********************
    (TOP
        (S
            (NP-SBJ
                (NN aerospace)
                (NNS earnings)
            )
            (VP
                (VBD sagged)
                (NP-EXT
                    (NP
                        (NP
                            (CD <CD>)
                            (NN %)
                        )
                        (PP-TMP
                            (IN for)
                            (NP
                                (DT the)
                                (NN quarter)
                            )
                        )
                    )
                    (CC and)
                    (NP
                        (NP
                            (CD <CD>)
                            (NN %)
                        )
                        (PP-TMP
                            (IN for)
                            (NP
                                (DT the)
                                (NN year)
                            )
                        )
                    )
                )
                (, ,)
                (ADVP-PRP
                    (RB largely)
                    (JJ due)
                    (PP
                        (TO to)
                        (NP
                            (JJR lower)
                            (NN b-1b)
                            (NN program)
                            (NN profit)
                        )
                    )
                )
            )
        )
        (: ;)
        (S
            (NP-SBJ
                (NP
                    (DT the)
                    (JJ last)
                )
                (PP
                    (IN of)
                    (NP
                        (DT the)
                        (NNS bombers)
                    )
                )
            )
            (VP
                (VBD rolled)
                (ADVP-DIR
                    (IN out)
                )
                (PP-TMP
                    (IN in)
                    (NP
                        (NNP <NNP>)
                        (CD <CD>)
                    )
                )
            )
        )
        (. .)
    )
    
    
    Chomsky Normal Form:  ********************
    (TOP
        (S
            (NP-SBJ
                (NN aerospace)
                (NNS earnings)
            )
            (VP
                (VBD sagged)
                (VP|<NP-EXT&,>
                    (NP-EXT
                        (NP
                            (NP
                                (CD <CD>)
                                (NN %)
                            )
                            (PP-TMP
                                (IN for)
                                (NP
                                    (DT the)
                                    (NN quarter)
                                )
                            )
                        )
                        (NP-EXT|<CC&NP>
                            (CC and)
                            (NP
                                (NP
                                    (CD <CD>)
                                    (NN %)
                                )
                                (PP-TMP
                                    (IN for)
                                    (NP
                                        (DT the)
                                        (NN year)
                                    )
                                )
                            )
                        )
                    )
                    (VP|<,&ADVP-PRP>
                        (, ,)
                        (ADVP-PRP
                            (RB largely)
                            (ADVP-PRP|<JJ&PP>
                                (JJ due)
                                (PP
                                    (TO to)
                                    (NP
                                        (JJR lower)
                                        (NP|<NN&NN>
                                            (NN b-1b)
                                            (NP|<NN&NN>
                                                (NN program)
                                                (NN profit)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        (TOP|<:&S>
            (: ;)
            (TOP|<S&.>
                (S
                    (NP-SBJ
                        (NP
                            (DT the)
                            (JJ last)
                        )
                        (PP
                            (IN of)
                            (NP
                                (DT the)
                                (NNS bombers)
                            )
                        )
                    )
                    (VP
                        (VBD rolled)
                        (VP|<ADVP-DIR&PP-TMP>
                            (ADVP-DIR
                                (IN out)
                            )
                            (PP-TMP
                                (IN in)
                                (NP
                                    (NNP <NNP>)
                                    (CD <CD>)
                                )
                            )
                        )
                    )
                )
                (. .)
            )
        )
    )
    
    
    


### 2.3 Summary

I struggled a bit with this section, mostly on what I assume to be a trivial matter but I am curious if that assumption is correct. First, about my implementation: this is again a depth first recursive method that takes action on replacing nodes with more than two children as shallow as possible. The issue I was having was that when I would look at the labels of nodes that were parents of many levels of lower nodes, the label would contain all the information of the make up of the lower tree. Since this was not the desired label value I used regular expressions to parse out the important information from the label, but I realize that this is not an elegant solution and that there is some way I could alter my recursion to allow me to avoid this. The code is heavily commented and the process can be seen there.

## 3. Generate productions

### 3.1 Program


```python
def productions(self):

    # prods will be a list of tuples, each of which will be a single
    # production.
    prods = []

    # if the current head is not terminal check if daughters are temninal.
    if not Tree.terminal(self):

        # if daughter is terminal, add head lable with the terminal string
        # to prods.
        if Tree.terminal(self.daughters[0]):
            prods.append((self.label, [self.daughters[0]]))

        # if daughter is not terminal, add head lable and a list of
        # daughter lables to prods.
        else:
            prods.append((self.label, [daughter.label for daughter in self.daughters]))

    # Now, for each daughter of the current head, if the daughter is not
    # terminal, recursivly call the function and add its return value to
    # prods.
    for daughter in self.daughters:
        if not Tree.terminal(daughter):
            prods += Tree.productions(daughter)

    # returning of prods allows for the recursiv adding to higher order
    # prods, as well as returning the final prods list to the caller.
    return prods


```

### 3.2 Sample Outputs


```python
'''This simple script will randomly select an entry from the 
    wsj-normalized.psd corpus three times and output the results 
    of running the intended script on the entry'''

with open('wsj-normalized.psd') as stream:
    wsj = Tree.from_stream(stream)
    for i in range(3):
        for _ in range(randint(1,1000)):
            sample = next(wsj)
        
        stars = '*'*20
        print('%s EXAMPLE %d: %s \n\nInitial Read: %s' % (stars, (i+1), stars, stars))
        print(sample)
        print('\n\nProductions:  %s' % stars)
        sample.collapse_unary().chomsky_normal_form()
        for prods in sample.productions():
            mother = prods[0]
            daughters = prods[1]
            print('{: <20} -> {}'.format(mother, ' '.join(daughters)))
        print('\n\n')
```

    ******************** EXAMPLE 1: ******************** 
    
    Initial Read: ********************
    (TOP
        (NP-SBJ
            (DT the)
            (NN truck)
            (NN maker)
        )
        (VP
            (VBD said)
            (SBAR
                (-NONE- 0)
                (S
                    (NP-SBJ
                        (NP
                            (DT the)
                            (JJ significant)
                            (NN drop)
                        )
                        (PP
                            (IN in)
                            (NP
                                (JJ net)
                                (NN income)
                            )
                        )
                    )
                    (VP
                        (MD will)
                        (VP
                            (VB result)
                            (PP-CLR
                                (IN in)
                                (NP
                                    (NP
                                        (JJR lower)
                                        (NNS earnings)
                                    )
                                    (PP
                                        (IN for)
                                        (NP
                                            (DT the)
                                            (JJ fiscal)
                                            (NN year)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        (. .)
    )
    
    
    Productions:  ********************
    TOP                  -> NP-SBJ TOP|<VP&.>
    NP-SBJ               -> DT NP-SBJ|<NN&NN>
    DT                   -> the
    NP-SBJ|<NN&NN>       -> NN NN
    NN                   -> truck
    NN                   -> maker
    TOP|<VP&.>           -> VP .
    VP                   -> VBD SBAR
    VBD                  -> said
    SBAR                 -> -NONE- S
    -NONE-               -> 0
    S                    -> NP-SBJ VP
    NP-SBJ               -> NP PP
    NP                   -> DT NP|<JJ&NN>
    DT                   -> the
    NP|<JJ&NN>           -> JJ NN
    JJ                   -> significant
    NN                   -> drop
    PP                   -> IN NP
    IN                   -> in
    NP                   -> JJ NN
    JJ                   -> net
    NN                   -> income
    VP                   -> MD VP
    MD                   -> will
    VP                   -> VB PP-CLR
    VB                   -> result
    PP-CLR               -> IN NP
    IN                   -> in
    NP                   -> NP PP
    NP                   -> JJR NNS
    JJR                  -> lower
    NNS                  -> earnings
    PP                   -> IN NP
    IN                   -> for
    NP                   -> DT NP|<JJ&NN>
    DT                   -> the
    NP|<JJ&NN>           -> JJ NN
    JJ                   -> fiscal
    NN                   -> year
    .                    -> .
    
    
    
    ******************** EXAMPLE 2: ******************** 
    
    Initial Read: ********************
    (TOP
        (NP-SBJ
            (NNP <NNP>)
            (NNP <NNP>)
        )
        (VP
            (VBZ has)
            (VP
                (VBN called)
                (PP-CLR
                    (IN for)
                    (NP
                        (NP
                            (DT an)
                            (NN agreement)
                        )
                        (PP-TMP
                            (IN by)
                            (NP
                                (NP
                                    (JJ next)
                                    (NNP <NNP>)
                                )
                                (PP-TMP
                                    (IN at)
                                    (NP
                                        (DT the)
                                        (JJS latest)
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        (. .)
    )
    
    
    Productions:  ********************
    TOP                  -> NP-SBJ TOP|<VP&.>
    NP-SBJ               -> NNP NNP
    NNP                  -> <NNP>
    NNP                  -> <NNP>
    TOP|<VP&.>           -> VP .
    VP                   -> VBZ VP
    VBZ                  -> has
    VP                   -> VBN PP-CLR
    VBN                  -> called
    PP-CLR               -> IN NP
    IN                   -> for
    NP                   -> NP PP-TMP
    NP                   -> DT NN
    DT                   -> an
    NN                   -> agreement
    PP-TMP               -> IN NP
    IN                   -> by
    NP                   -> NP PP-TMP
    NP                   -> JJ NNP
    JJ                   -> next
    NNP                  -> <NNP>
    PP-TMP               -> IN NP
    IN                   -> at
    NP                   -> DT JJS
    DT                   -> the
    JJS                  -> latest
    .                    -> .
    
    
    
    ******************** EXAMPLE 3: ******************** 
    
    Initial Read: ********************
    (TOP
        (NP-ADV
            (CC either)
            (NN way)
        )
        (, ,)
        (NP-SBJ
            (DT the)
            (NN ghostbusting)
            (NN business)
        )
        (VP
            (VBZ is)
            (VP
                (VBG going)
                (PP-MNR
                    (IN like)
                    (NP
                        (NNS gangbusters)
                    )
                )
            )
        )
        (. .)
    )
    
    
    Productions:  ********************
    TOP                  -> NP-ADV TOP|<,&NP-SBJ>
    NP-ADV               -> CC NN
    CC                   -> either
    NN                   -> way
    TOP|<,&NP-SBJ>       -> , TOP|<NP-SBJ&VP>
    ,                    -> ,
    TOP|<NP-SBJ&VP>      -> NP-SBJ TOP|<VP&.>
    NP-SBJ               -> DT NP-SBJ|<NN&NN>
    DT                   -> the
    NP-SBJ|<NN&NN>       -> NN NN
    NN                   -> ghostbusting
    NN                   -> business
    TOP|<VP&.>           -> VP .
    VP                   -> VBZ VP
    VBZ                  -> is
    VP                   -> VBG PP-MNR
    VBG                  -> going
    PP-MNR               -> IN NP
    IN                   -> like
    NP                   -> NNS
    NNS                  -> gangbusters
    .                    -> .
    
    
    


### 3.3 Summary

This was the simplest part of the assignment. Again this was a depth first recursive solution where at each step down the branch, the node labels are added to the production chain. By implementing the chain as a list we can simply append single new production additions or entire list of productions. The ability to append an entire production list to another is what makes the recursive solution work. By returning a production list from a lower node and appending it onto a higher nodes production list, we can recursively build a list for the entire tree.

## Extra Credit

## Scratch Paper


```python
s = '(TOP (S (VP (TO to) (VP (VB play)))))'
t = Tree.from_string(s)
print(t)
```

    (TOP
        (S
            (VP
                (TO to)
                (VP
                    (VB play)
                )
            )
        )
    )



```python
p = t[0].pop()
```


```python
p.label = t[0].label+'+'+p.label
print(p)

t[0]=p
print(t)
```

    (S+VP
        (TO to)
        (VP
            (VB play)
        )
    )
    (TOP
        (S+VP
            (TO to)
            (VP
                (VB play)
            )
        )
    )



```python
Tree.unary(t[0][0])
```




    True




```python
def unary_col(tree_in):

    # For each head immediately below the root:
    for daughter in tree_in.daughters:
        
        # If head is terminal, continue
        if Tree.terminal(daughter):
            continue
            
        # Recursively apply the function
        unary_col(daughter)

        # If head is non-unary, continue
        if not Tree.unary(daughter):
            continue

        # If head's only daughter is terminal, continue
        if Tree.terminal(daughter[0]):
            continue

        # If head's only granddaughter is unary and terminal, continue
        if Tree.terminal(daughter[0][0]):
            print('******',daughter[0][0])
            continue

        # Merge the only daughter's label and promote its daughters
        daughter.label = daughter.label+'+'+daughter[0].label
        daughter.daughters = daughter.daughters.pop()
        print('----->>',tree_in.label, daughter.label)
        


```


```python
t = Tree.from_string(s)
print(t)
unary_col(t)
print(t)
```

    (TOP
        (S
            (VP
                (TO to)
                (VP
                    (VB play)
                )
            )
        )
    )
    ****** play
    ----->> TOP S+VP
    (TOP
        (S+VP
            (TO to)
            (VP
                (VB play)
            )
        )
    )



```python
st = '''(TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP 
        (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's)) 
        (NN trading) (NN room))))) (, ,) (NP (DT the) 
        (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP 
        (RB little)) (ADJP (RB right)))) (. .)))'''
```


```python
st
```




    "(TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP \n        (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's)) \n        (NN trading) (NN room))))) (, ,) (NP (DT the) \n        (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP \n        (RB little)) (ADJP (RB right)))) (. .)))"




```python
cnf = Tree.from_string(st)
cnf.collapse_unary()
print(cnf)
```

    (TOP
        (S
            (S+VP
                (VBN Turned)
                (ADVP
                    (RB loose)
                )
                (PP
                    (IN in)
                    (NP
                        (NP
                            (NNP Shane)
                            (NNP Longman)
                            (POS 's)
                        )
                        (NN trading)
                        (NN room)
                    )
                )
            )
            (, ,)
            (NP
                (DT the)
                (NN yuppie)
                (NNS dealers)
            )
            (VP
                (AUX do)
                (NP
                    (NP
                        (RB little)
                    )
                    (ADJP
                        (RB right)
                    )
                )
            )
            (. .)
        )
    )



```python
cnf = Tree.from_string(st)
cnf.collapse_unary().chomsky_normal_form()
#print(cnf)
#cnffunc_change(cnf)
#cnffunc(cnf)
```




    (TOP
        (S
            (S+VP
                (VBN Turned)
                (S+VP|<ADVP&PP>
                    (ADVP
                        (RB loose)
                    )
                    (PP
                        (IN in)
                        (NP
                            (NP
                                (NNP Shane)
                                (NP|<NNP&POS>
                                    (NNP Longman)
                                    (POS 's)
                                )
                            )
                            (NP|<NN&NN>
                                (NN trading)
                                (NN room)
                            )
                        )
                    )
                )
            )
            (S|<,&NP>
                (, ,)
                (S|<NP&VP>
                    (NP
                        (DT the)
                        (NP|<NN&NNS>
                            (NN yuppie)
                            (NNS dealers)
                        )
                    )
                    (S|<VP&.>
                        (VP
                            (AUX do)
                            (NP
                                (NP
                                    (RB little)
                                )
                                (ADJP
                                    (RB right)
                                )
                            )
                        )
                        (. .)
                    )
                )
            )
        )
    )




```python
def cnffunc(in_tree):
    
    if Tree.terminal(in_tree):
        return in_tree
    
    if len(in_tree) < 3:
        for daughter in in_tree.daughters:
            cnffunc(daughter)


    elif len(in_tree) > 2:
        last_daughters = in_tree.daughters[-2:]
        
        # hacky regex method to remove extra characters
        right_label = re.findall(r"\|\<(.*?)\&",last_daughters[1].label)
        if right_label:
            new_label = '%s|<%s&%s>' % (in_tree.label, last_daughters[0].label, right_label[0])
        else:
            new_label = '%s|<%s&%s>' % (in_tree.label, last_daughters[0].label, last_daughters[1].label)
            
        node = Tree(new_label, last_daughters)
        in_tree.daughters = in_tree.daughters[:-2]
        in_tree.append(node)
        cnffunc(in_tree)
            
    return(in_tree)
    
        
```


```python
import re

ins = 'S|<NP&S|<VP&.>>'

re.findall(r"\|\<(.*?)\&",'fail')

```




    []




```python
print(match.group(1))
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-14-90155b479621> in <module>()
    ----> 1 print(match.group(1))
    

    NameError: name 'match' is not defined



```python
bool(['hello'])
```




    True




```python
def prod(in_tree):
    prods = []
    if not Tree.terminal(in_tree):
        if Tree.terminal(in_tree.daughters[0]):
            prods.append((in_tree.label, [in_tree.daughters[0]]))
        else:
            prods.append((in_tree.label, [daughter.label for daughter in in_tree.daughters]))
    for daughter in in_tree.daughters:
        if not Tree.terminal(daughter):
            prods += prod(daughter)
    return prods
```


```python
prod(cnf)
```




    [('TOP', ['S']),
     ('S', ['S+VP', 'S|<,&NP>']),
     ('S+VP', ['VBN', 'S+VP|<ADVP&PP>']),
     ('VBN', ['Turned']),
     ('S+VP|<ADVP&PP>', ['ADVP', 'PP']),
     ('ADVP', ['RB']),
     ('RB', ['loose']),
     ('PP', ['IN', 'NP']),
     ('IN', ['in']),
     ('NP', ['NP', 'NP|<NN&NN>']),
     ('NP', ['NNP', 'NP|<NNP&POS>']),
     ('NNP', ['Shane']),
     ('NP|<NNP&POS>', ['NNP', 'POS']),
     ('NNP', ['Longman']),
     ('POS', ["'s"]),
     ('NP|<NN&NN>', ['NN', 'NN']),
     ('NN', ['trading']),
     ('NN', ['room']),
     ('S|<,&NP>', [',', 'S|<NP&VP>']),
     (',', [',']),
     ('S|<NP&VP>', ['NP', 'S|<VP&.>']),
     ('NP', ['DT', 'NP|<NN&NNS>']),
     ('DT', ['the']),
     ('NP|<NN&NNS>', ['NN', 'NNS']),
     ('NN', ['yuppie']),
     ('NNS', ['dealers']),
     ('S|<VP&.>', ['VP', '.']),
     ('VP', ['AUX', 'NP']),
     ('AUX', ['do']),
     ('NP', ['NP', 'ADJP']),
     ('NP', ['RB']),
     ('RB', ['little']),
     ('ADJP', ['RB']),
     ('RB', ['right']),
     ('.', ['.'])]




```python
Tree.terminal(cnf[0][0][0][0])
type(cnf[0][0][0][0])

```




    str


