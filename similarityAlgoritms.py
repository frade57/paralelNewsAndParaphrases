import numpy
import spacy
from scipy import spatial
import sqlite3
from math import exp, log
from nltk.tokenize import word_tokenize

con = sqlite3.connect('GNewsW2Vsingle.db')
w2v= {}
neutral= [0 for i in range(300)]

def sumVet(wordList):
    result = numpy.zeros(300, dtype='f')
    for token in wordList:
            try:
                result += numpy.array(getWordVector(str(token).lower()))
            except Exception:
                continue
    return result

def scipyObjecj(noticia):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(noticia)
    return(doc)

def getWordVector(word):
    cur = con.cursor()
    cur.execute("select v from words where word= ?", (word,))
    result = cur.fetchone()[0]
    con.commit()
    return (eval(result))

def line2WVector(line):
    vs= line.split()
    v= [float(x) for x in vs[1:]]
    return vs[0], v

def cossim(v1,v2): return 1 - spatial.distance.cosine(v1, v2)

def sumVerbs(doc):
    result = numpy.zeros(300, dtype='f')
    for token in doc:
        if token.pos_ == 'VERB':
            try:
                result += numpy.array(getWordVector(str(token.text).lower()))
            except Exception:
                continue
    return result

def entidades(doc): return set([(e.text) for e in doc.ents])

def jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def sqr(x:float) -> float: return x*x

def tokenize(s, lower=True):
    if lower:
        l = word_tokenize(s.lower())
    else:
        l = word_tokenize(s)
    n = len(l)
    nalpha = 0
    for i in range(n):
        if not l[i].isalnum():
            l[i] = '_'
        else:
            nalpha += 1
    return l, n, nalpha

def computeConnections(sa, sb):
    la, nla, na = tokenize(sa)
    lb, nlb, nb = tokenize(sb)

    s = {}
    for i in range(nla):
        if la[i] == '_': continue
        for j in range(nlb):
            if lb[j] == '_': continue
            if not j in s.keys() and la[i] == lb[j]:
                s[j] = i
                break
    lista = []
    for j in s.keys(): lista.append( (s[j],j,lb[j]) )

    return lista, na, nb

def simGaussEntropy(sa, sb) -> float:
    conections, na, nb = computeConnections(sa,sb)
    n = len(conections)
    p = n/min(na,nb)
    q = n/max(na,nb)
    x = p**0.7 * q**0.3
    f = exp(-sqr(x-0.5)/0.05)
    if x == 0 or x == 1:
        g = 0
    else:
        g = -x*log(x,2)-(1-x)*log(1-x,2)
    y = 0.4*f + 0.6*g
    return y

def demontration(sa,sb): return simGaussEntropy(sa,sb)
