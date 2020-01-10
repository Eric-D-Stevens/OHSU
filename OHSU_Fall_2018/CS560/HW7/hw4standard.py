def isVar(thing):
    if type(thing) is list:
        return False
    if type(thing) is int:
        return False
    if thing[0].isupper():
        return True
    if thing[0] == "_":
        return True
    return False

def findvariables(thing,inlist):
    # thing could be an atom or a body or a clause
    # no harm in looking for variables in the first position if it is an atom
    outlist = inlist[:]
    for arg in thing:
        if type(arg) is list:
            outlist = findvariables(arg,outlist)
        elif isVar(arg) and not arg in outlist:
            outlist.append(arg)
    return outlist

def substitute(expr,subs):
    # thing could be clause, atom, or a term (including a variable)
    if not type(expr) is list:
        if expr in subs:
            return subs[expr]
        return expr

    newexpr = []
    for arg in expr:
        newexpr.append(substitute(arg,subs))
    return newexpr

def prettyexpr(expr):
    if not type(expr) is list:
        return expr

    str = expr[0]
    started = False

    for arg in expr[1:]:
        if not started:
            str += "("
            started = True
        else:
            str += ","
        if type(arg) is list:
            str += prettyexpr(arg)
        else:
            str += arg
    if started:
        str += ")"

    return str

def prettyclause(clause):
    str = prettyexpr(clause[0])
    if len(clause) == 1:
        return str

    str += " <= " + prettyexpr(clause[1])
    if len(clause) == 2:
        return str

    for atom in clause[2:]:
        str += " ^ " + prettyexpr(atom)

    return str

def occurscheck(var,term):
    if not (type(term) is list):
        if var == term:
            return False
        return True

    todo = term[1:]
    while not todo == []:
        first = todo[0]
        todo = todo[1:]
        if type(first) is list:
            todo += first[1:]
            continue
        if first == var:
            return False
    return True

def unify(a,b,subs):
    # unify takes subs as input, which is usually an empty dictionary.
    #   it adds substitutions to subs in order to unify a and b.
    # So the subs arguments is being altered by this routine.
    a = substitute(a,subs)
    b = substitute(b,subs)

    # if same constant, same variable, same atom or same function
    # don't need to do anything
    if a == b:
        return True
    # if we have a predicate or function symbol
    if type(a) is list and type(b) is list:
        if a[0] != b[0]:
            return False
        if len(a) != len(b):
            return False
        for (aArg,bArg) in zip(a[1:],b[1:]):
            # each call through might update subs
            # don't want subs to be a global variable
            # so pass subs them back and forth
            if not unify(aArg,bArg,subs):
                return False
        return True

    # if b is a variable, swap a and b, so we can just check if a is a variable
    if isVar(b):
        temp = a
        a = b
        b = temp

    if isVar(a):
        if occurscheck(a,b) == False:
            return False

        for var in subs:
            subs[var] = substitute(subs[var],{a:b})
        subs[a] = b
        return True

    return False

def freshvariables(thing):
    global NextVariable
    subs = {}
    varlist = findvariables(thing,[])
    for v in varlist:
        subs[v] = "_%d" % NextVariable
        NextVariable += 1
    return substitute(thing,subs)

NextVariable = 0


