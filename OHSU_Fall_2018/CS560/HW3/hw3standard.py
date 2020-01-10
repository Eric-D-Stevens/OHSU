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

def test(A,B):
    res = unify(A,B)
    if res == 0:
        print("%s and %s do not unify" % (prettyexpr(A),prettyexpr(B)))
    else:
        str = "%s and %s unify with" % (prettyexpr(A),prettyexpr(B))
        for v in res:
            str += " %s/%s" % (v,prettyexpr(res[v]))
        print(str)
