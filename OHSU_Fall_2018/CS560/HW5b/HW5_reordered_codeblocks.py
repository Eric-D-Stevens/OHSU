
# coding: utf-8

# # CS 560: Homework 5(b)
# ### Eric Stevens



# ## Question 5
# 
# The below code does not function properly. It appears to be function properly until the point where an atom is resolved that causes one of the delayed `notequal` atoms atoms to be grounded to a constant that will make it evealuate to false. I have run out of time to solve this problem.


from hw4standard import *

def prove(query,kb):

    vars = findvariables(query,[])
    print("Vars in query are %s" % vars)
    answer = [['yes']+vars]+query
    print("Initial answer clause is %s" % prettyclause(answer))
    
    # the initial frontier is a list whose only element is the initial
    # answer clause
    frontier = [answer]
    
    while frontier:
        # give answer clause fresh variables
        answer = frontier[0]
        if len(answer) == 1:
            yesatom = answer[0]
            str = "Proof:"
            for var, val in zip(vars,yesatom[1:]):
                str += " %s=%s" % (var,prettyexpr(val))
            print(str)
            return True

        print("Trying to prove : %s" % prettyclause(answer))
        # give it fresh variables
        answer = freshvariables(answer)
        print("\n after fresh vars : %s" % prettyclause(answer))

        neighbors = []
        
        i=1
        while delay(answer[i]): 
            print(i)
            i+=1
            if i > 1000: break
                
        print("\n\n EVALUATING ANSWER ATOM: ", answer[i],"\n\n")
                
        if answer[i][0] == 'notequal':
            
            if notequal(answer[i]):
                print(" \n using notequal rule\n" )
                # create answer clause
                answercopy = answer[0:i]+answer[i+1:] # changed answer index
                # apply substitution
                answercopy = substitute(answercopy,subs)
                print(" result: "+prettyclause(answercopy))
                neighbors.append(answercopy)
            else:
                return False
        
        else:
            for rule in kb:
                subs = {}
                if not unify(rule[0],answer[i],subs): #changed answer index
                    print('FAILED TO UNIFY ',rule[0], answer[i])
                    continue
                print('UNIFYing ',rule[0], answer[i])
                print(" \n using rule %s\n" % prettyclause(rule))
                print(" proven by %s with %s\n" % (rule[0],subs))
                # create answer clause
                answercopy = answer[0:i]+rule[1:]+answer[i+1:] # changed answer index
                # apply substitution
                answercopy = substitute(answercopy,subs)
                print(" result: "+prettyclause(answercopy))
                neighbors.append(answercopy)
                break
        frontier = neighbors+frontier[1:]
        #print('New Front: %s' % prettyclause([frontier]))
        print('\n\n')
    return False

def notequal(predicate):
    if predicate[0] == 'notequal':
        if not unify(predicate[1],predicate[2],{}): return True
        if predicate[1] == predicate[2]: return False
    return True
    
def delay(predicate):
    if predicate[0] == 'notequal':
        if not unify(predicate[1],predicate[2],{}): return False
        if predicate[1] == predicate[2]: return False
        else: return True    
    # predicate is not 'notequal'
    return False



kb = [
    [['block', 'red1']],
    [['block', 'red2']],
    [['block', 'red3']],
    [['block', 'red4']],
    [['block', 'red5']],
    [['block', 'red6']],
    [['block', 'red7']],
    [['block', 'gre1']],
    [['block', 'gre2']],
    [['block', 'gre3']],
    [['block', 'blu1']],
    [['block', 'blu2']],
    [['block', 'yel1']],
    [['block', 'bla1']],
    [['color', 'red1', 'red']],
    [['color', 'red2', 'red']],
    [['color', 'red3', 'red']],
    [['color', 'red4', 'red']],
    [['color', 'red5', 'red']],
    [['color', 'red6', 'red']],
    [['color', 'red7', 'red']],
    [['color', 'gre1', 'green']],
    [['color', 'gre2', 'green']],
    [['color', 'gre3', 'green']],
    [['color', 'blu1', 'blue']],
    [['color', 'blu2', 'blue']],
    [['color', 'yel1', 'yellow']],
    [['color', 'bla1', 'black']],
    

    [['mct', ['s','0'], ['p','Block','nil']], ['block', 'Block']],
    
    [['mct', ['s','X'],'NewTower'], 
        ['notequal', 'X','0'],
        ['mct', 'X', 'Tower'],
        ['unify', 'Tower', ['p','Top','US']],
        ['notequal', 'TopColor', 'BlockColor'],
        ['differentfromlist', 'Block', 'Tower'],
        ['color', 'Top', 'TopColor'],
        ['block', 'Block'],
        ['color', 'Block', 'BlockColor'],
        ['unify','NewTower',['p','Block','Tower']] 
    ],
    
    [['differentfromlist', 'X', ['p','Y','nil']],
        ['notequal', 'X','Y']
    ],
    
    [['differentfromlist', 'X', ['p','Top','Rest']],
        ['notequal', 'X','Top'],
        ['differentfromlist','X','Rest']
    ],
    
    
    
    [['unify', 'X', 'X']],
    
]

prove([['mct',['s',['s',['s',['s',['s','0']]]]],'List']],kb)
