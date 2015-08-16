# -*- coding: utf-8 -*-


# GNU All-Permissive License
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.


# Is x letter of our alphabet? Our alphabet is {a, b}.
def letter(x):
    return x == 'a' or x == 'b'

# Is x formula of our sзystem? Formulas of our system are all nonempty words.
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
        if axiom(X[i]) == False:
            j = 0
            found = False
            while j < i:
                if rule1(X[j], X[i]) or rule2(X[j], X[i]) or rule3(X[j], X[i]):
                    found = True
                    break
                j = j+1
            if found == False:
                print X[i]
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
