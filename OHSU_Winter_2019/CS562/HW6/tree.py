#!/usr/bin/env python -O
# tree.py: n-ary branching tree, reading trees from text, and transforms
# Kyle Gorman <gormanky@ohsu.edu>

from re import escape, finditer, findall
from collections import namedtuple, defaultdict

# left and delimiters on trees
LDEL = '('
RDEL = ')'
LDELE = escape(LDEL)
RDELE = escape(RDEL)
DELIMITERS = r'({})|({})'.format(LDELE, RDELE)

# labels are a sequence of non-whitespace, non-delimiter characters used
# both for terminals and non-terminals
LABEL = r'[^\s{}{}]+'.format(LDELE, RDELE)

# a "token" consists of:
# * a left delimiter
# * possibly some whitespace (though not usually)
# * one of:
#   - a label for a head (possibly null)
#   - a right delimiter
#   - a label for a terminal
TOKEN = r'({0})\s*({2})?|({1})|({2})'.format(LDELE, RDELE, LABEL)

# characters for naming heads introduced by tree transformation; should
# not overlap LDEL or RDEL if you are writing to text files
CU_JOIN_CHAR = '+'
MARKOVIZE_CHAR = '|'
CNF_JOIN_CHAR = '&'
CNF_LEFT_DELIMITER = '<'
CNF_RIGHT_DELIMITER = '>'


class Tree(object):
    """
    A n-ary branching tree with string(-like) objects as labels both on
    terminals and non-terminals. 

    For the purpose of variable names, X' is the "mother" of X, and X the 
    "daughter" of X', iff X' immediately dominates X. Furthermore, X and
    Y are "sisters" if they are immediately dominated by the same mother.

    We assume throughout that terminals are only daughters (i.e., have no
    sisters).
    """

    def __init__(self, label, daughters=None):
        self.label = label
        self.daughters = daughters if daughters else []

    # construct trees from string and file objects

    @classmethod
    def from_string(cls, string):
        r"""
        Read a single Treebank-style tree from a string. Example:

        >>> s = '(ADVP (ADV widely) (CONJ and) (ADV friendly))'
        >>> Tree.from_string(s)
        (ADVP
            (ADV widely)
            (CONJ and)
            (ADV friendly)
        )

        It doesn't break just because there are weird newlines, either:

        >>> str(Tree.from_string(s)) == \
        ... str(Tree.from_string(s.replace(' ', '\n')))
        True

        A few types of errors are known:

        >>> Tree.from_string(s[:-1])
        Traceback (most recent call last):
        ...
        ValueError: End-of-string, need /\)/
        >>> Tree.from_string(s[1:])
        Traceback (most recent call last):
        ...
        ValueError: Need /\(/
        >>> s_without_head = s[6:-1]
        >>> Tree.from_string(s_without_head)
        Traceback (most recent call last):
        ...
        ValueError: String contains 3 trees
        """
        # initialize stack to "empty"
        stack = [(None, [])]
        for m in finditer(TOKEN, string):
            token = m.group()
            if m.group(1):  # left delimiter
                stack.append((m.group(2), []))
            elif m.group(3):  # right delimiter
                # if stack is "empty", there is nothing in need of closure
                if len(stack) == 1:
                    raise ValueError('Need /{}/'.format(LDELE))
                (mother, children) = stack.pop()
                stack[-1][1].append(cls(mother, children))
            elif m.group(4):  # leaf
                stack[-1][1].append(m.group(4))
            else:
                raise ValueError('Parsing failure: {}'.format(m.groups()))
        # check to make sure the stack is "empty"
        if len(stack) > 1:
            raise ValueError('End-of-string, need /{}/'.format(RDELE))
        elif len(stack[0][1]) == 0:
            raise ValueError('End-of-string, need /{}/'.format(LDELE))
        elif len(stack[0][1]) > 1:
            raise ValueError('String contains {} trees'.format(
                len(stack[0][1])))
        return stack[0][1][0]

    @classmethod
    def from_stream(cls, handle):
        r"""
        Given a treebank-style data *.psd file, yield all its Trees, using
        `from_string` above

        Mock up a real file using cStringIO

        >>> from io import StringIO
        >>> s = u'(ADVP (ADV widely) (CONJ and) (ADV friendly))'
        >>> source = StringIO(s.replace(' ', '\n\n\n') + s)
        >>> (one, two) = Tree.from_stream(source)
        >>> str(one) == str(two)
        True
        """
        # TODO I am deeply unhappy with this solution. It would be nicer
        # to use the cleverer logic found in Tree.from_string instead.
        stack = 0
        start = 0
        string = handle.read()
        for m in finditer(DELIMITERS, string):
            # left bracket
            if m.group(1):
                stack += 1
            # right bracket
            else:
                stack -= 1
                # if brackets match, parse it
                if stack == 0:
                    end = m.end()
                    yield Tree.from_string(string[start:end])
                    start = end

    @classmethod
    def from_stream_modified(cls, handle):

        # initalize an empty stack
        stack = [(None, [])]

        # loop through readline operations
        while(1):

            # string will be a single line form the .psd formatted file
            string = handle.readline()
            if string == '':
                print('reached end of file')
                break # exit if end of file is reached

            # for token matches in each new line
            for m in finditer(TOKEN, string):
                token = m.group()
                if m.group(1):  # left delimiter
                    stack.append((m.group(2), []))
                elif m.group(3):  # right delimiter
                    # if stack is "empty", there is nothing in need of closure
                    if len(stack) == 1:
                        raise ValueError('Need /{}/'.format(LDELE))
                    (mother, children) = stack.pop()
                    stack[-1][1].append(cls(mother, children))
                elif m.group(4):  # leaf
                    stack[-1][1].append(m.group(4))
                else:
                    raise ValueError('Parsing failure: {}'.format(m.groups()))

            # if a matching closing deliminator has not been found, continue
            # reading lines until one is found.
            if len(stack) > 1:
                continue

            elif len(stack[0][1]) == 0:
                raise ValueError('End-of-string, need /{}/'.format(LDELE))
            elif len(stack[0][1]) > 1:
                raise ValueError('String contains {} trees'.format(
                    len(stack[0][1])))

            # since a closing deliminator has been found, yeild the stack and
            # then clear it for the next round of line reads. 
            yield stack[0][1][0]
            stack = [(None, [])]




    # magic methods for access, etc., all using self.daughters

    def __iter__(self):
        return iter(self.daughters)

    def __getitem__(self, i):
        return self.daughters[i]

    def __setitem__(self, i, value):
        self.daughters[i] = value

    def __len__(self):
        return len(self.daughters)

    def pop(self, i=None):
        return self.daughters.pop() if i is None else self.daughters.pop(i)

    def append(self, other):
        self.daughters.append(other)

    # static methods for traversal (etc.)

    @staticmethod
    def terminal(obj):
        return not hasattr(obj, 'label')

    @staticmethod
    def unary(obj):
        return len(obj) == 1

    # string representations

    def __repr__(self):
        return self.pretty()

    def pretty(self, indent=0, step=4):
        """
        Serialize tree into human-readable multiline string

        >>> s = '(TOP (S (VP (TO to) (VP (VB play)))))'
        >>> t = Tree.from_string(s)
        >>> t
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
        """
        string = LDEL + self.label
        i = indent + step
        is_tree = None
        for daughter in self:
            is_terminal = Tree.terminal(daughter)
            if is_terminal:
                string += ' ' + daughter
            else:
                # recursively print with increased indent
                string += '\n' + (' ' * i) + daughter.pretty(i)
        # add a newline and spaces after last non-terminal at this depth
        if not is_terminal:
            string += '\n' + (' ' * indent)
        string += RDEL
        return string

    # tree transform instance methods

    def collapse_unary(self, join_char=CU_JOIN_CHAR):
        """
        Return a copy of the tree in which unary productions (i.e.,
        productions with one daughter) have been removed. 

        There are two classes of unary production that we do *not* want to collapse:
        
        * In Penn Treebank style, the root is often a unary production,
          but it is not collapsed. This allows for a special root label
          (e.g., "TOP") to be used to indicate successful parsing.
        * In Penn Treebank style, each POS tag node is an only child 
          produced by a "syntactic" mother. We do not want to collapse these nodes either, 
          since we want to be able to use them as inputs for chart parsing.

        A mother is therefore collapsible into its daughter if it is not 
        the root note, the daughter is an "only child", and the daughter
        is neither terminal nor "pre-terminal" (the motehr of a terminal).

        Algorithmically, this is as follows:
        
        * For each head immediately below the root:
            - If head is terminal, continue
            - Recursively apply the function
            - If head is non-unary, continue
            - If head's only daughter is terminal, continue
            - If head's only granddaughter is unary and terminal, continue
            - Merge the only daughter's label and promote its daughters

        Some examples follow.

        Simple merge, with root and POS "distractors":

        >>> s = '(TOP (S (VP (TO to) (VP (VB play)))))'
        >>> t = Tree.from_string(s)
        >>> t.collapse_unary()
        (TOP
            (S+VP
                (TO to)
                (VP
                    (VB play)
                )
            )
        )

        Double merge, with both types of distractors:

        >>> s = '(TOP (S (SBAR (VP (TO to) (VP (VB play))))))'
        >>> t = Tree.from_string(s)
        >>> t.collapse_unary()
        (TOP
            (S+SBAR+VP
                (TO to)
                (VP
                    (VB play)
                )
            )
        )

        A long one:

        >>> s = '''(TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP 
        ...        (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's)) 
        ...        (NN trading) (NN room))))) (, ,) (NP (DT the) 
        ...        (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP 
        ...        (RB little)) (ADJP (RB right)))) (. .)))'''
        >>> t = Tree.from_string(s)
        >>> t.collapse_unary()
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
        """

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


    def chomsky_normal_form(self, markovize_char=MARKOVIZE_CHAR,
                            join_char=CNF_JOIN_CHAR,
                            left_delimiter=CNF_LEFT_DELIMITER,
                            right_delimiter=CNF_RIGHT_DELIMITER):
        """
        Convert tree so that it can be generated by a Chomsky Normal Form 
        (CNF) grammar. In CNF grammars, every production rule either 
        produces two non-terminals or one terminal. In trees generated by
        CNF grammars, each non-terminal has either two non-terminal 
        daughters, or one terminal daughter. This tree transformation is 
        accomplished by binarizing the tree by introducing non-terminals.

        Note that the requirement that any rule which produces 
        non-terminals produces exactly two non-terminals is satisfied by
        a grammar/tree in which unary productions have been collapsed.
        Therefore, we assume here that this has already been done.

        Two questions remain. First, are the terminals introduced to the 
        left or the right? Here we assume right, which is arguably the 
        more appropriate assumption for English, since English is largely
        head-initial (and therefore right-branching). Secondly, how are 
        these new nodes labeled? Here we create new labels using the 
        name of the mother and the two new sisters.

        >>> s = '''(TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP 
        ...        (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's)) 
        ...        (NN trading) (NN room))))) (, ,) (NP (DT the) 
        ...        (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP 
        ...        (RB little)) (ADJP (RB right)))) (. .)))'''
        >>> Tree.from_string(s).collapse_unary().chomsky_normal_form()
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
        """

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

    # should return a tree that results form the string
    def to_string(self):

        # recursive function to return terminal as string
        def terminal_finder(tree_obj, word_list=[]):
            if Tree.terminal(tree_obj):
                word_list.append(tree_obj)
            else:
                for daughter in tree_obj.daughters:
                    terminal_finder(daughter,word_list)

            return word_list

        wl = []
        return ' '.join(terminal_finder(self, wl))



    def productions(self):
        """
        Generate all productions in this tree

        >>> s = '''(TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP 
        ...        (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's)) 
        ...        (NN trading) (NN room))))) (, ,) (NP (DT the) 
        ...        (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP 
        ...        (RB little)) (ADJP (RB right)))) (. .)))'''
        >>> t = Tree.from_string(s).collapse_unary().chomsky_normal_form()
        >>> for (mother, daughters) in t.productions():
        ...     print('{: <20} -> {}'.format(mother, ' '.join(daughters)))
        TOP                  -> S
        S                    -> S+VP S|<,&NP>
        S+VP                 -> VBN S+VP|<ADVP&PP>
        VBN                  -> Turned
        S+VP|<ADVP&PP>       -> ADVP PP
        ADVP                 -> RB
        RB                   -> loose
        PP                   -> IN NP
        IN                   -> in
        NP                   -> NP NP|<NN&NN>
        NP                   -> NNP NP|<NNP&POS>
        NNP                  -> Shane
        NP|<NNP&POS>         -> NNP POS
        NNP                  -> Longman
        POS                  -> 's
        NP|<NN&NN>           -> NN NN
        NN                   -> trading
        NN                   -> room
        S|<,&NP>             -> , S|<NP&VP>
        ,                    -> ,
        S|<NP&VP>            -> NP S|<VP&.>
        NP                   -> DT NP|<NN&NNS>
        DT                   -> the
        NP|<NN&NNS>          -> NN NNS
        NN                   -> yuppie
        NNS                  -> dealers
        S|<VP&.>             -> VP .
        VP                   -> AUX NP
        AUX                  -> do
        NP                   -> NP ADJP
        NP                   -> RB
        RB                   -> little
        ADJP                 -> RB
        RB                   -> right
        .                    -> .
        """

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



    def MLE_PCFG(self):
        '''
        This method allows operates on a Tree object and returns
        the MLE PCFG that is generated form the UC CNF from of the
        tree.
        '''
        
        self.collapse_unary().chomsky_normal_form()

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

from IPython.display import HTML, display

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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
