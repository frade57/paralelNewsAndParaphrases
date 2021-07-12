from similarityAlgoritms import scipyObjecj
import json
from datetime import date

_today = date.today()

def addPhraseToList(doc, new, nPar, iPar):

    nPar = str(nPar)
    iPar = str(iPar)
    toRemove = ['\n', '', ' ']
    assert doc.has_annotation("SENT_START")
    for sent in doc.sents:
        if str(sent) in toRemove:
            continue
        new["news"]['phrases.' + nPar + '-' + iPar + ''].append(str(sent))


def createPhraseList():
    f = open("newsPairs_%s.json" % _today, "r", encoding='utf8')
    data = json.load(f)
    new = {}
    new["date"] = str(_today)
    new["news"] = {}
    nPar=0
    iPar=1
    for sets in data["news"]:
        for news1 in sets["set"]:
            nPar+=1

            new["news"]['phrases.' + str(nPar) + '-' + str(1)] = []
            new["news"]['phrases.' + str(nPar) + '-' + str(2)] = []

            doc1 = scipyObjecj(news1["value 1"]["value"])
            doc2 = scipyObjecj(news1["value 2"]["value"])

            addPhraseToList(doc1, new, nPar, iPar)
            iPar=2

            addPhraseToList(doc2, new, nPar, iPar)
            iPar=1

    with open("phraseList_%s.json" %_today, "a", encoding='utf8') as g:
        g.write(json.dumps(new, indent=4))
