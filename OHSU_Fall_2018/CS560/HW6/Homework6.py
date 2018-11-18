
# ### Helper Functions

# In[158]:


from hw4standard import *

def PrettyCNF(expr):
    #print(expr,"\n\n")
    s = ""
    for literal in expr:
        if s != "": s += " v "
        #print(type(literal))
        if type(literal) is list:
            if literal[0] == "not":
                s += "!"
                atom = literal[1]
            else:
                atom = literal
        s += prettyexpr(atom)
    return s

def PrettyConsequence(consequence):
    '''prints an entire consequenct set'''
    for i in consequence:
        print(PrettyCNF(i))

def PrettyResolution(unit, clause, result):
    print("Resolving", PrettyCNF(clause), "with", PrettyCNF(unit))
    print("Result:", PrettyCNF(result))

def sameclause(a,b):
    subs = {}
    ret = unify(a,b,subs)
    if ret == False or subs == {}:
        return ret
    # same clause if bottom just has variables and each is different
    seen = []
    for bottom in ret.values:
        if not isVar(bottom):
            return False
        if bottom in seen:
            return False
        seen.append(bottom)
    return True


def negate(literal):
    if type(literal) is list and literal[0] == "not":
        return literal[1]
    return ['not',literal]


def resolve(unit, clause):
    '''Takes in a unit clause and a disjunct clause and returns a resolution of the two'''

    # negate the unit clause for resolution
    neg_unit = negate(unit)

    # look for matching disjunct in clause
    for disjunct in clause:

        subs = {}
        # find one and get subs
        if unify(neg_unit, disjunct, subs):
            sub_clause = substitute(clause, subs)
            sub_neg_unit = substitute(neg_unit, subs)

            # remove instance that was resolved
            sub_clause.remove(sub_neg_unit)

            # return new clause
            return sub_clause
# TEST
#print(resolve(['canary','tweety'],[['normal','X'],['not',['canary','X']]]))

def can_resolve(unit, clause):
    '''Checks to see if a resolution is possible'''
    neg_unit = negate(unit)
    for disjunct in clause:
        if unify(neg_unit,disjunct,{}):
            return True
    return False
# TEST
#can_resolve(['canary','tweety'],[['normal','X'],['not',['canary','X']]])


def already_in_c_set(resolution, c_set):
    ''' See if a clause is already in a set'''
    for disjunct in c_set:
        if sameclause(resolution, disjunct):
            return True
    return False
#TEST
#print(alread_in_c_set([['canary','tweety']],kb))
#print(alread_in_c_set([['canary','SHOULD FAIL']],kb))

def merge_sets(s1, s2):
    '''Merges to sets without overlap'''
    new_set = s1.copy()

    for expression in s2:
        if not already_in_c_set(expression, new_set):
            new_set.append(expression)
    return new_set
# TEST
#print(merge_sets(kb[:3],kb[1:5]))


# ### Prove Function

# In[159]:


def prove(kb, query):

    # declare consequence set
    consequence = kb.copy()

    # negate query
    neg_query = negate(query)

    # add query negation to consequence set
    consequence.append([neg_query])

    #PrettyConsequence(consequence)

    # loop 
    while 1:

        temp_set = [] # new resolutions before adding to consequence

        # look for units and try to resolve
        for unit in consequence:
            if len(unit) == 1:

                # unit clause found, give fresh variables
                unit_clause = freshvariables(unit[0])

                # look at every expression in the current consequence set
                for expression in consequence:

                    # if it can be resolved do so and add the result to the temp set
                    if can_resolve(unit_clause, expression):
                        new_clause = resolve(unit_clause, expression)
                        PrettyResolution([unit_clause], expression, new_clause)
                        print("\n")
                        # success if empty disjunct 
                        if new_clause == []:
                            return True

                        # otherwise check to see if resolution is in temp or consequence.
                        # add to temp set if it is not.
                        else:
                            if not already_in_c_set(new_clause, temp_set) and not already_in_c_set(new_clause, consequence):
                                temp_set.append(new_clause)
                                PrettyConsequence(merge_sets(consequence,temp_set))
                                print("\n")

        # if no further possible resolutions, fail
        if temp_set == []:
            return False
        # otherwise, merge temp and consequence and run again
        else:
            consequence = merge_sets(consequence, temp_set)


# ### Demo 1

# In[160]:


kb = [[['ostrich','sam']],
[['canary','tweety']],
[['bird','X'],['not',['ostrich','X']]],
[['bird','X'],['not',['canary','X']]],
[['fly','X'],['not',['bird','X']],['not',['normal','X']]],
[['not',['normal','X']],['not',['ostrich','X']]],
[['normal','X'],['not',['canary','X']]]]


print(prove(kb,['fly','tweety']))


# ## Demo 2

# In[162]:


print(prove(kb,['fly','sam']))


# ### Demo 3

# In[161]:


print(prove([[['boy',['goo','X','Y']], ['boy',['foo','X','Y']]]], ['boy', 'X']))



