import json
from datetime import date
import numpy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from Sentence import demontration
from similarityAlgoritms import scipyObjecj, entidades, cossim, jaccard, getWordVector

_today = date.today()

def sumVet(wordList):
    result = numpy.zeros(300, dtype='f')
    for token in wordList:
            try:
                result += numpy.array(getWordVector(str(token).lower()))
            except Exception:
                continue
    return result

def phrasePair(phrase1, phrase2, new, cossen, jacca, gauss):

    setList = []
    setList.append({'simCoss': cossen,'simJaccard':jacca,'simGauss':gauss,'phrase1': phrase1,'phrase2':phrase2})
    new["news"].append({
        "set": setList
    })

def cleanText(phrase) :
    text=str(phrase)
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]

    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    words = [word for word in stripped if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    return(words)

def phraseCount(data):
    n=0
    for news in data["news"]:
        n+=1
    return(int(n/2))


def findParaphrase():

    f = open("phraseList_2021-07-08.json", "r", encoding='utf8')
    data = json.load(f)
    new = {}
    new["date"] = str(_today)
    new["news"] = []

    nPar = 1
    iPar = 1
    for i in range(phraseCount(data)):
        for phrase1 in data["news"]["phrases."+str(nPar)+"-"+str(iPar)]:

            words = cleanText(phrase1)
            vet1=sumVet(words)
            iPar=2

            frase1=scipyObjecj(phrase1)
            ent1=entidades(frase1)

            for phrase2 in data["news"]["phrases."+str(nPar)+"-"+str(iPar)]:
                try:
                    gauss = demontration(phrase1, phrase2)
                except (ZeroDivisionError):
                    continue
                if gauss > 0.8:
                    try:
                        frase2 = scipyObjecj(phrase2)
                        ent2 = entidades(frase2)
                        jac = jaccard(ent1, ent2)
                    except (ZeroDivisionError):
                        continue
                    if jac > 0.24:
                        words = cleanText(phrase2)
                        vet2 = sumVet(words)
                        cos=cossim(vet1,vet2)
                        print(cos)

                        if cos > 0.75 and cos < 0.98:
                            phrasePair(phrase1, phrase2, new, cos, jac, gauss)

                            print(str(cos)+" "+str(jac)+" "+str(gauss)+"\n"+phrase1+"\n"+phrase2)
                            print("\n")
        nPar+=1
    with open("paraPhrases_%s" % _today, "w", encoding='utf8') as f:
        f.write(json.dumps(new, indent=4))
    print(new)