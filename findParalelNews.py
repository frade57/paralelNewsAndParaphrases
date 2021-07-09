import sqlite3
import json
from datetime import date
from similarityAlgoritms import scipyObjecj, sumVerbs, entidades, cossim, jaccard

_today = date.today()
con = sqlite3.connect('GNewsW2Vsingle.db')



def simNews():

    f = open("news_%s.json" % _today, "r", encoding='utf8')
    data = json.load(f)
    new = {}
    new["date"] = str(_today)
    new["news"] = []

    for sets in data["news"]:

        newsCount = 0
        for news1 in sets["set"]:
            newsCount += 1
            newsSetCount = 0
            doc1 = scipyObjecj(news1["value"])
            v1 = sumVerbs(doc1)

            for newsCompare in sets["set"]:
                newsSetCount += 1

                if (newsSetCount < newsCount + 1):  # para não reptir noticias no set
                    continue

                doc2 = scipyObjecj(newsCompare["value"])
                v2 = sumVerbs(doc2)

                if str(v1) != str(v2):
                    cossen = cossim(v1, v2)
                    try:
                        jacca = jaccard(entidades(doc1), entidades(doc2))

                    except ZeroDivisionError:
                        continue
                    if cossen > 0.8 and cossen < 0.97 and jacca > 0.1:
                        url1 = str(news1["url"])
                        url2 = str(newsCompare['url'])
                        newsPairs(news1, newsCompare, cossen, jacca, url1, url2, new)

                else:
                    continue
    with open("newsPairs_%s.json" % _today, "a", encoding='utf8') as f:
        f.write(json.dumps(new, indent=4))


def newsPairs(news1, newsCompare, cossen, jacca, url1, url2, new):

    setList = []
    setList.append({'simCoss': cossen,'simJaccard':jacca,'url': url1, 'value 1': news1, 'url': url2, 'value 2': newsCompare})
    new["news"].append({
        "set": setList
    })