
# Question 7

import random
from hw4standard import *

# time seed random variable
from datetime import datetime
random.seed(datetime.now())

def prove(query,kb):

    #******************************************************************#
    answer = query.copy() # Make a copy of query so query is not altered.
    answer.insert(0,findvariables(query,[])) # add variables from query
    answer[0].insert(0,'yes') # add 'yes'
    #******************************************************************#

    print("Initial answer clause is %s \n\n" % prettyclause(answer))

    while len(answer) > 1:
        #give answer clause fresh variables
        answer = freshvariables(answer)
        matches = []
        for r in kb:
            #unify right most atom for scripting ease
            if unify(answer[-1],r[0],{}):
                matches.append(r)


        if matches == []:
            print("No rules match %s" % prettyexpr(answer[-1]))
            return False

        #******************************************************************#
        print(prettyclause(answer)) # output formatting

        # Unification
        a = answer[-1] # right-most atom
        b = matches[random.randint(0,len(matches)-1)] # random match
        sub = {} # get subs
        unify(a,b[0],sub)

        # Substitution 
        resolution = substitute(b,sub) # sub for match to be used in resolution
        answer = substitute(answer,sub) # sub current answer clause

        # output formatting
        print("Resolve with: ",prettyclause(b))
        print("Substitution: " ,sub, "\n\n")

        # Replace 
        answer = answer[:-1] # cut right-most atom
        for a in resolution[1:]: answer.append(a) # add resolution body
        #******************************************************************#


    print(prettyclause(answer))
    return True

def multiprove(query,kb):
    proved = False
    for n in range(100):
        print("------------------------------------------------------------------------------")
        print("Iteration ", n,"\n")
        if prove(query,kb):
            print("Proved on iteration %d" % n)
            print("------------------------------------------------------------------------------\n")
            return True
    print("Could not prove")
    print("------------------------------------------------------------------------------\n")
    return False





kb = [[['animal','X'],['dog','X']],
    [['gets_pleasure','X','feeding'],['animal','X']],
    [['likes','X','Y'],['animal','Y'],['owns','X','Y']],
    [['does','X','Y','Z'],['likes','X','Y'],['gets_pleasure','Y','Z']],
    [['dog','fido']],
    [['owns','mary','fido']]]

query=[['does','mary','X','Y']]

multiprove(query,kb)



# ## Question 8:




kb2 = [
    [['has_tree','T','T']],
    [['has_tree','T',['n','N','LT','RT']],['has_tree','T','LT']],
    [['has_tree','T',['n','N','LT','RT']],['has_tree','T','RT']]
    ]


query2 = [['has_tree',['n','X',['e', 'e4'],'Y'],['n','n1',['n','n2',['e', 'e1'],['e', 'e2']],['n','n3',['e', 'e3'],
        ['n','n4',['e', 'e4'],['e', 'e5']]]]]]

# call 
multiprove(query2,kb2)

# selecting submission output of smaller number of iterations.
# somtimes it took 80 iterations to resolve, other times it
# happened on the first iteration.


# ## Question 9:
# 
# **This code does not work.** Below are two different attempts that I made to solve this problem. The first tries to call a function recursivly and hold the frontier in the recursion. The second tries to maintain the frontier in a list in the the for loop of the program. I have not had success. These functions are both capable of solving the first query as the output demonstrates, but are unable to solve the second query. Something is wrong with the way they move from child back up to parent nodes. They either get stuck in an infinite loop or terminate without completing the proof. I ran out of time to solve the problem.

# In[54]:


def depth_first(answerclause,kb):
    
    answer = answerclause.copy()
    

    # fresh
    answer = freshvariables(answer)

    
    # get list of matches for right most pred
    matches = []
    for r in kb:
        if unify(answer[-1],r[0],{}):
            matches.append(r)
    
    if matches == []: return False
    for m in matches:
        print(prettyclause(answer))
        a = answer[-1]
        b = m
        sub = {}
        unify(a,b[0],sub)
        
        resolution = substitute(b,sub)
        answer = substitute(answer,sub)
        #print("matches: ", matches[0])
        print("Resolve with: ",prettyclause(b))
        print("Substitution: " ,sub, "\n\n")
        
        
        answer = answer[:-1]
        
        if len(resolution) > 0:
            for z in resolution[1:]: answer.append(z)
        else:
            answer.append(resolution)
        
        if len(answer)==1:
            
            print(prettyclause(answer))
            return True
        if depth_first(answer,kb): return True

    return False

def dfr(query,kb):
    print("QUERY: ", prettyclause(query),"\n\n")
    # add yes to answer clause
    answer = query.copy() 
    answer.insert(0,findvariables(query,[])) # add variables from query
    answer[0].insert(0,'yes') # add 'yes'
    return depth_first(answer,kb)


# In[55]:


dfr(query,kb)


# In[56]:


# Question 7

import random
from hw4standard import *

# time seed random variable
from datetime import datetime
random.seed(datetime.now())

def deep(query,kb,front):
    
    #******************************************************************#
    answer = query.copy() # Make a copy of query so query is not altered.
    answer.insert(0,findvariables(query,[])) # add variables from query
    answer[0].insert(0,'yes') # add 'yes'
    #******************************************************************#
    
    print("Initial answer clause is %s \n\n" % prettyclause(answer))
   
    while len(answer) > 1:
        #give answer clause fresh variables
        answer = freshvariables(answer)
        matches = []
        for r in kb:
            #unify right most atom for scripting ease
            if unify(answer[-1],r[0],{}):
                matches.append(r)
                front.append(r)


        if matches == []:
            if front == []:
                print("No rules match %s" % prettyexpr(answer[0]))
                return False
            else:
                front.pop()
                deep(front[-1],kb,front)
        #******************************************************************#
        print(prettyclause(answer)) # output formatting
        
        # Unification
        a = answer[-1] # right-most atom
        b = front.pop() # random match
        sub = {} # get subs
        unify(a,b[0],sub)
        
        # Substitution 
        resolution = substitute(b,sub) # sub for match to be used in resolution
        answer = substitute(answer,sub) # sub current answer clause
        
        # output formatting
        print("Resolve with: ",prettyclause(b))
        print("Substitution: " ,sub, "\n\n")
        
        # Replace 
        answer = answer[:-1] # cut right-most atom
        for a in resolution[1:]: answer.append(a) # add resolution body
        #******************************************************************#


    print(prettyclause(answer))
    return True


# In[57]:


deep(query,kb,[])

