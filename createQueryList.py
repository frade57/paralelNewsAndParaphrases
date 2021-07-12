from datetime import date
import os
import requests
import json
import string
from nltk.corpus import stopwords
from apiKeys import _apiKey

apiKey=_apiKey
_today = date.today()

def removeEmptyLines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)

def cleanQuerylist(tokens):

    tokens = [w.lower() for w in tokens]

    table = str.maketrans('', '', string.punctuation)

    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    return (words)

def stripTopHeadlinesToQ():

    f = open('queryList.txt', "w")

    url = ('https://newsapi.org/v2/top-headlines?'
            'country=us&'
            'pageSize=100&'
            'from='+str(_today)+'&'
            'to='+str(_today)+'&'
            'apiKey='+_apiKey+''
           )

    response = requests.get(url)
    JsonLoad = json.loads(response.text)

    for article in JsonLoad['articles']:

        URL=article['url']

        strip1 = URL.split('/')[-1]
        strip1 = strip1.replace('.html','')
        strip1 = strip1.replace('index','')
        strip1 = strip1.replace('\n','')
        strip1 = strip1.split('-')
        words = cleanQuerylist(strip1)

        listaQ = '+AND+'.join(words)

        f.write(listaQ+'\n')
    f.close()

    removeEmptyLines('queryList.txt')

