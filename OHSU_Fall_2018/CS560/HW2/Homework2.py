

# ## Question 10:

# In[51]:


def substitute(expr,subs):
    
    # declare the substituted list
    newexpr = [expr[0]]
    
    # loop through input arguments
    for arg in expr[1:]:
        
        # if argument exeist in substitution list then sub it
        if arg in subs: newexpr.append(subs[arg])
            
        # if the argument is not in the sub list then let it pass through
        else: newexpr.append(arg)
            
    return newexpr


def test(atom,subs):
    result = substitute(atom,subs)
    str = "Substitution of %s with" % prettyexpr(atom)
    for v in subs:
        str += " %s/%s" % (v,prettyexpr(subs[v]))
    print("%s\n %s" % (str,prettyexpr(result)))

def doall():
    # here is a variant of Exercise 2.9 part a)
    test(["fun", "A", "X", "Y", "X", "Y"], {"A" : "X", "Z" : "b", "Y" : "c"})

doall()


# ## Question 11:
# 
# I have elected to use a slightly different strategy for the 'substitute()' than in the provided code. The 'test()' function is also heavily modified as required by the assignment. The prettyexpr is exactly the same. The altered code is heavily commented for ease of understanding. 

# In[52]:


def substitute(expr,subs):
    
    # deal with single variable
    if type(expr[0]) is str:
        if expr[0][0].isupper(): return [subs[expr[0]]]
        # this is hacky, I am doing this because this is what the assignment
        # requests but I think that the program should fail here. From what 
        # I know of Datalog, terms cannot exist outside of predicates. I think 
        # this situation shold return an 'invalid expression' warning.
    
    # list to hold the substituted output string
    newexpr = [expr[0]]
    
    # loop through each areument in input list
    for arg in expr[1:]:
        
        # If item is a list, recursivly call 'substitute()'
        if type(arg) is list: newexpr.append(substitute(arg,subs))
 
        #  if the argument is in the sub list then sub it
        elif arg in subs: newexpr.append(subs[arg])
            
        # otherwise, let it pass through    
        else: newexpr.append(arg)
            
    return newexpr


def test(atom,subs):
    result = substitute(atom,subs)
    str = "Substitution of %s with" % prettyexpr(atom)
    for v in subs:
        str += " %s/%s" % (v,prettyexpr(subs[v]))
    print("%s\n %s" % (str,prettyexpr(result)))

def doall():
    
    # set part b attributes
    b_head = ["yes", "F", "L"]
    b_body = ["append", "F", ["c", "L", "nil"], ["c", "l", ["c", "i", ["c", "s", ["c", "t", "nil"]]]]]
    b_subs = {"F":["c", "l", "X1"], "Y1":["c","L","nil"], "A1":"l", "Z1":["c", "i", ["c", "s", ["c", "t", "nil"]]]}
    
    # set part c attributes
    c_head = ["append",["c", "A1", "X1"], "Y1", ["c", "A1", "Z1"]]
    c_body = ["append", "X1", "Y1", "Z1"]
    c_subs = {"F":["c", "l", "X1"], "Y1":["c","L","nil"], "A1":"l", "Z1":["c", "i", ["c", "s", ["c", "t", "nil"]]]}
    
    # Run test on head of part b
    print("\n\n(b) head:")
    test(b_head, b_subs)
 
    # Run test on head of part b
    print("\n\n(b) body:")
    test(b_body, b_subs)
    
    # Run test on head of part b
    print("\n\n(c) head:")
    test(c_head, c_subs)
 
    # Run test on head of part b
    print("\n\n(c) body:")
    test(c_body, c_subs)
    
    # Run test on head of part b
    print("\n\nSingle Variable:")
    test(["X"], {"X":"Y"})
    
    
doall()

