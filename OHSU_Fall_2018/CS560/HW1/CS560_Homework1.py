

# ***
# ***
# ## Question 5

# In[5]:


# function to parse input knowledge bases
def parse(atom): 
    seen = set()
    while atom != []:
        
        # print the current state of atom before altering
        print("Currently processing %s" % atom)
        
        # seperate 'first' element in atom from the 'rest' of the atom
        first = atom[0]
        rest = atom[1:]

        # if 'first' is a list set atom =to contents of 'first' + 'rest'
        if(type(first)==list): 
            atom = first[:]+rest[:]
        
        # if 'first' is not a list, check case of first letter
        else: 
            # if uppercase add to 'seen' and set 'atom' =to 'rest'
            if(first[0].isupper()):
                seen.add(first)
                atom = rest
            # if lowercase only set 'atom' =to 'rest
            else:
                atom = rest

    # now print out all of the variables
    for var in seen:
        print("Variable %s" % var)


# Now we run the code above on an input atom:

# In[6]:


atom = ["p", "a", ["b", "X"], ["d", "e", "X", ["b", "c"], "Y"]]
parse(atom)


# ***
# ## Question 6
# 
# ##### Part 1: Build the parse() function

# In[45]:


# random library for predicate resolution
import random
import time

# seed with time for non dupliate runs
random.seed(time.time())

# prove(query, kb) is a function that performs a top-down proof of a query
# with randomly selected choices of next steps.
#
#  Inputs:
#    query: a string of the form "?a" for example
#    kb: the knowledgebase of the form[[h1,b11,b12],[h2,b21]...ect]
#
#  Return: (boolean)
#    True - the operation was successful in validating the query
#    False - the operation faild to validate the query
#
def prove(query, kb):
    
        
    # check query input format and parse
    if query[0] != "?": 
        print("Input not a query, use ?<predicate>")
        exit()
    else:
        current_clause = ["yes", query[1:]]
        
    # display the inital clause that results from the querey    
    print("current clause: ", current_clause)
        
    # MAIN LOOP
    # continues replacing 'current_clause' body parts that have heads in the knowledge
    # base with the corresponding body in the knowledge base until either there is no
    # body left in 'current_clause' (success) or there is no option to replace the body
    # parts in 'current clause' (failure).
    while current_clause[1:]:
        
        # stores clauses whos head matches left most body element of current
        matches = []

        # search kb for clauses and append to 'matches'
        for clause in kb:
            if clause[0] == current_clause[1]:
                matches.append(clause)

        # if empty fail
        if not matches: 
            print("failed at", current_clause)
            
            # Trigger failure return
            return False

        # if option(s) exists, remove matched body part.
        # select option randomly and append to 'current_clause'.
        else:
            current_clause.pop(1)
            match =random.choice(matches)[1:]
            current_clause += match[:]
            print("current clause: ", current_clause)
        
    # completion of the while loop without failure, succesfull
    return True 

        


# ##### Part 2: Extend the parse() function to 100 iterations with the multiparse() function

# In[62]:


import sys
save_stdout = sys.stdout

# multprove(query, kb) is a function that performs 100 top-down proof attempts
# unless it runs into a succesful one before the 100 mark.
#
#  Inputs:
#    query: a string of the form "?a" for example
#    kb: the knowledgebase of the form[[h1,b11,b12],[h2,b21]...ect]
#
#  Return: (boolean)
#    True - the operation was successful in validating the query
#    False - the operation faild to validate the query
#
def multiprove(query, kb):
    
    # allow for 100 attempts at proving the query
    for x in range(100):
        
        # DISREGUARD: Format output for HW submission
        if x < 5: print("\n\nAttempt ", x+1, "\n")
        if x == 5: sys.stdout = open('trash', 'w')  
        if x == 97: 
            sys.stdout = save_stdout
            print("\n\n\t...\n\t...\n\t...\n\n")
            print("\n\nAttempt ", x+1, "\n")
        if x > 97: print("\n\nAttempt ", x+1, "\n") 
            
        # perform top down proof and see if it is succesful.
        success = prove(query, kb)
        
        # if there is a success in any of the iterations the 
        # query is proven and the function can retern true.
        if success: return True
        
    # if all iterations have resulted in failures then the 
    # query has not been resolved and the function returns false.
    return False


# ##### Part 3: Prove '?a'

# In[58]:


kb = [["a", "b", "c"],
      ["b", "d"],
      ["b", "e"],
      ["c"],
      ["d", "h"],
      ["e"],
      ["f", "g", "b"],
      ["g", "c", "k"],
      ["j", "a", "b"]]
        

multiprove("?a",kb)


        


# ##### Part 4: Prove '?f'

# In[63]:


multiprove("?f",kb)

