
# coding: utf-8

# # CS 560: Homework 8
# ### Eric Stevens
# ### December 2, 2018



# In[68]:


from hw4standard import *

NumActions = 0
Action = {}

class Action:
    all = []
    def __init__(self,head,pre,add,dele):
        self.head = head
        self.pre = pre
        self.add = add
        self.dele = dele
        Action.all.append(self)

        vars = findvariables(head,[])
        vars = findvariables(pre,vars)
        self.vars = vars

    def __str__(self):
        s = "Action %s\n" % prettyexpr(self.head)
        s += "  Preconditions:"
        for i in self.pre:
            s += " %s" % prettyexpr(i)
        s += "\n"
        s += "  Add list:     "
        for i in self.add:
            s += " %s" % prettyexpr(i)
        s += "\n"
        s += "  Delete list:  "
        for i in self.dele:
            s += " %s" % prettyexpr(i)
        s += "  Variables are"
        for i in self.vars:
            s += " " + i
        return s

# pickup block on block
Action(['pickup', 'Obj', 'X'], 
       [['on','Obj','X'],['empty'],['block','Obj'],['block','X'],['clear','Obj']],
       [['holding','Obj'],['clear','X']],
       [['empty'],['on','Obj','X'],['clear','Obj']])

# pickup block on table
Action(['pickup', 'Obj', 'X'], 
       [['on','Obj','X'],['empty'],['block','Obj'],['table','X'],['clear','Obj']],
       [['holding','Obj']],
       [['empty'],['on','Obj','X'],['clear','Obj']])

# putdown block on block
Action(['putdown', 'Obj', 'X'], 
       [['holding','Obj'],['block','X'],['clear','X']],
       [['empty'],['on','Obj','X'],['clear','Obj']],
       [['holding','Obj'],['clear','X']])

# putdown block on table
Action(['putdown', 'Obj', 'X'], 
       [['holding','Obj'],['table','X']],
       [['empty'],['on','Obj','X'],['clear','Obj']],
       [['holding','Obj']])

for a in Action.all:
    print(a.__str__())
    print(' ')


# ### Question 13


Constants = ['a','b','c','t']
Primitives = ['on','clear','empty','holding']

Initial = [['block','a'],['block','b'], ['block','c'], ['table','t'],
           ['on','a','b'],['on','b','c'],['on','c','t'],
           ['clear','a'],['empty']]

Goal = [['on','c','b'],['on','b','a'],['on','a','t'] ]


# ### Question 14
# 
# The only thing added to the prove function is checking to see if the Goal is in topWorld.
# 
# **MY CODE DOES NOT WORK**


def subset(sub,set):
    for i in sub:
        if not i in set:
            return False
    return True

def remove(sub,set):
    newset = []
    for i in set:
        if not i in sub:
            newset.append(i)
    return newset

def printWorld(world,indent):
    str = indent
    for p in world:
        if p[0] in Primitives:
            str += " " + prettyexpr(p)
    print(str)

def printPlan(plan,indent):
    str = indent
    for p in plan:
        str += " " + prettyexpr(p)
    print(str)

def prove():
    worldcnt = 0
    # each item on frontier is a tuple of plan + world that results from executing plan
    frontier = [[[],Initial]]

    while frontier:
        topPlan,topWorld = frontier[0]

        print("Current plan:")
        printPlan(topPlan,"   ")

        print("Current world (primitives):")
        printWorld(topWorld,"   ")

        # check if the topWolrd has goal true in it
        # if so, say that the goal was found and return true

        # YOUR CODE HERE
        if subset(Goal, topWorld): return True

        # Your code should be able to find the plan after exploring all plans of length 6
        # I put in this stop code in case your code has a bug, so that you won't keep going forever
        print("")
        if len(topPlan) > 6:
            print("Could not find plan in 8 steps")
            return False

        neighbors = []

        for action in Action.all:

            # We could use a theorem prover to find variable instantiaions that make the
            # the preconditions true.
            # Instead, let's enumerae over all variable instantiations

            #--------------------
            # The code between the two sets of dashes iterates all variable instantiations
            # One of the questions asks you to explain how it works

            vars = action.vars
            numvars = len(vars)
            numconstants = len(Constants)
            cnt = int(pow(numconstants,numvars))
            for i in range(cnt):
                subs = {}
                j = i
                for v in vars:
                    c = j % numconstants
                    subs[v] = Constants[c]
                    j = (j - c)//numconstants
                #-----------------

                head = substitute(action.head,subs)
                pre  = substitute(action.pre,subs)
                add  = substitute(action.add,subs)
                dele = substitute(action.dele,subs)

                if subset(pre,topWorld):
                    worldcnt += 1
                    print("%d: Found applicable action" % worldcnt)
                    print(action)

                    # Create the new world and the new plan
                    # And add them to the neighbors

                    # YOUR CODE HERE

                    print("    New world:")
                    printWorld(newWorld,"     ")
                    print("    New plan :")
                    printPlan(newPlan,"     ")
                    print("")

        frontier = frontier[1:]+ neighbors

    print("No world with goal true was found")




