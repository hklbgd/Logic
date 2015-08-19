# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 21:33:57 2015

@author: nedjo
"""


# GNU All-Permissive License
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

def whiteSpace(x):
    return x in [' ', '\t', '\n', '\r']

def letter(x):
    if x == "_":
        return True
    if x >= "0" and x <= "9":
        return True
    if x >= "a" and x <= "z":
        return True
    if x >= "A" and x <= "Z":
        return True
    return False

def proposition(x):
    if len(x) == 0:
        return False
    for c in x:
        if letter(c) == False:
            return False
    return True

def formulaPart(f, n):
    while n < len(f) and whiteSpace(f[n]):
        n += 1
    if n < 0 or n >= len(f):
        return False
    if n+1 <= len(f) and f[n:n+1] == "~":
        g = formulaPart(f, n+1)
        if g == False:
            return False
        return [["not", g[0]], g[1]]
    if n+1 <= len(f) and f[n] == "(":
        g = formulaPart(f, n+1)
        if g == False:
            return False
        n = g[1]
        while n < len(f) and whiteSpace(f[n]):
            n += 1
        name = ""
        m = n
        if n+2 <= len(f) and f[n:n+2] == "/\\":
            name = "and"
            m = n+2
        elif n+2 <= len(f) and f[n:n+2] == "\\/":
            name = "or"
            m = n+2
        elif n+2 <= len(f) and f[n:n+2] == "=>":
            name = "imp"
            m = n+2
        elif n+3 <= len(f) and f[n:n+3] == "<=>":
            name = "equ"
            m = n+3
        if name != "":
            h = formulaPart(f, m)
            if h == False:
                return False
            n = h[1]
            if n >= len(f) or f[n] != ")":
                return False
            return [[name, g[0], h[0]], n+1]
    m = n
    while m < len(f) and (f[m] >= "a" and f[m] <= "z"):
        m += 1
    if m > n:
        return [[f[n:m]], m]
    return False

def formulaFromString(f):
    result = formulaPart(f, 0)
    if result == False:
        return False
    n = result[1]
    while n < len(f) and whiteSpace(f[n]):
        n += 1
    if n < len(f):
        return False
    return result[0]
    
def isFormula(f):
    if len(f) == 1:
        return proposition(f[0])
    if len(f) == 2:
        return f[0] == "not" and isFormula(f[1])
    if len(f) == 3:
        return f[0] in ["and", "or", "imp", "equ"] and isFormula(f[1]) and isFormula(f[2])
    return False

def formulaToString(f):
    if isFormula(f) == False:
        return False
    if len(f) == 1:       
        return f[0]
    if len(f) == 2:
        return "~"+formulaToString(f[1])
    if len(f) == 3:
        return "("+formulaToString(f[1])+{"and":"/\\", "or":"\\/", "imp":"=>", "equ":"<=>"}[f[0]]+formulaToString(f[2])+")"

def toUniform(f):
    if isFormula(f) == False:
        return False
    if len(f) == 1:
        return f
    if len(f) == 2:
        g = f[1]
        if len(g) == 1:
            return f
        if len(g) == 2:
            return toUniform(f[1][1])
        if g[0] == "and":
            return ["or", toUniform(["not", g[1]]), toUniform(["not", g[2]])]
        if g[0] == "or":
            return ["and", toUniform(["not", g[1]]), toUniform(["not", g[2]])]
        if g[0] == "imp":
            return ["and", toUniform(g[1]), toUniform(["not", g[2]])]
        if g[0] == "equ":
            return ["or", toUniform(["and", g[1], ["not", g[2]]]), toUniform(["and", ["not", g[1]], g[2]])]
    if len(f) == 3:
        if f[0] in ["and", "or"]:
            return [f[0], toUniform(f[1]), toUniform(f[2])]
        if f[0] == "imp":
            return ["or", toUniform(["not", f[1]]), toUniform(f[2])]
        if f[0] == "equ":
            return ["and", toUniform(["or", f[1], ["not", f[2]]]), toUniform(["or", ["not", f[1]], f[2]])]
    return False

f = formulaFromString("(~aba<=>~~~b)")
print f
print isFormula(f)
s = formulaToString(f)
print s
u = toUniform(f)
print u
print formulaToString(u)
