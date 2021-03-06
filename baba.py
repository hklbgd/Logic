# -*- coding: utf-8 -*-


# GNU All-Permissive License
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.


# Consider we following formal theory:
# The alphabet is {a, b}.
# Formulas are all nonempty words over this alphabet.
# The set of axioms is {a. bb}.
# Derivation rules are X->ax, X->Xa, X->bXb.
# This is implementation of functions related to this theory.


# Is x letter of our alphabet? Our alphabet is {a, b}.
def letter(x):
    return x == 'a' or x == 'b'

# Is x formula of our system? Formulas of our system are all nonempty words.
def formula(x):
    if x == '':
        return False
    for l in x:
        if letter(l) == False:
            return False
    return True

# Is x an axiom of our system? Our axioma are a and bb.
def axiom(x):
    return x == 'a' or x == 'bb'

# Is y direct consequence of x by rule1? It is iff y is concatenation of a and x.
def rule1(x, y):
    if formula(x) == False or formula(y) == False:
        return False
    return y == 'a'+x

# Is y direct consequence of x by rule1? It is iff y is concatenation of x and a.
def rule2(x, y):
    if formula(x) == False or formula(y) == False:
        return False
    return y == x+'a'

# Is y direct consequence of x by rule1? It is iff y is concatenation of a, x and a.
def rule3(x, y):
    if formula(x) == False or formula(y) == False:
        return False
    return y == 'b'+x+'b'

# Is X an proof?
def proof(X):
    if len(X) == 0:
        return False
    i = 0
    while i < len(X):
        if formula(X[i]) == False:
            return False
        if axiom(X[i]) == False:
            j = 0
            found = False
            while j < i:
                if rule1(X[j], X[i]) or rule2(X[j], X[i]) or rule3(X[j], X[i]):
                    found = True
                    break
                j = j+1
            if found == False:
                return False
        i = i+1
    return True

# Is X an proof of theorem y?
def proves(X, y):
    return proof(X) and y == X[-1]

# Is x an theorem?
def theorem(x):
    if formula(x) == False:
        return False
    counter = 0
    for l in x:
        if l == 'b':
            counter = counter + 1
    return counter%2 == 0

# Return proof x if it is a theorem or return False if x is not a theorem.
def prove(x):
    if formula(x) == False:
        return False
    if x == 'a' or x == 'bb':
        return [x]
    if len(x) > 1 and x[0] == 'a':
        p = prove(x[1:])
        if p == False:
            return False
        p.append(x)
        return p
    if len(x) > 1 and x[-1] == 'a':
        p = prove(x[:-1])
        if p == False:
            return False
        p.append(x)
        return p
    if len(x) > 2 and x[0] == 'b' and x[-1] == 'b':
        p = prove(x[1:-1])
        if p == False:
            return False
        p.append(x)
        return p
    return False

# Return proof of y from list of hypoteses X
def proveHyp(X, y):
    if formula(y) == False:
        return False
    for z in X:
        if formula(z) == False:
            return False
    if axiom(y) or y in X:
        return [y]
    if y[0] == 'a' and len(y) > 1:
        p = proveHyp(X, y[1:])
        if p != False:
            p.append(y)
            return p
    if y[-1] == 'a' and len(y) > 1:
        p = proveHyp(X, y[:-1])
        if p != False:
            p.append(y)
            return p
    if y[0] == 'b' and y[-1] == 'b' and len(y) > 2:
        p = proveHyp(X, y[1:-1])
        if p != False:
            p.append(y)
            return p
    return False

# Is the x syntactic consequence of list of hypoteses X?
def consequence(X, y):
    return proveHyp(X, y) != False

if formula("bbb") and proves([], "bbb") == False:
    print "The theory is consistent."

if formula("bbb") and proves([], "bbb") == False and formula("b") and consequence(["bbb"], "b") == False:
    print "The theory is incomplete."

print prove("baba")
