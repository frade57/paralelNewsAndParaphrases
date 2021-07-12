from bs4 import BeautifulSoup
import traceback
from apiKeys import _apiKeys
import json
import requests
from datetime import date

_currentApiKeyIndex = 1
_apiKey = _apiKeys[_currentApiKeyIndex]
_today = date.today()
_PageSize = 100

def changeApiKey():

    global _apiKey
    global _currentApiKeyIndex

    _apiKey = _apiKeys[(_currentApiKeyIndex + 1) % len(_apiKeys)]
    _currentApiKeyIndex = (_currentApiKeyIndex + 1) % len(_apiKeys)

def getNews():

    f1 = open("queryList.txt", "r")

    new = {}
    new["date"] = str(_today)
    new["news"] = []

    for line in f1:
        query=line.replace('\n','')
        if query == '':
            continue

        setList = []

        for currentPage in range(10):
            currentPage+=1
            for text in getNewsInfo(query, currentPage, _PageSize):
                setList.append(text)

        if setList != []:
            new["news"].append({
            "title": query,
            "set": setList })

    print(new)
    with open("news_%s.json" % _today, "w", encoding='utf8') as f:
            f.write(json.dumps(new, indent=4))

def getNewsInfo(query, pageNumber, pagesize):

    JsonInfo = executeHttpRequest(pageNumber, pagesize, query)
    setList = []

    try:

        Resultados = (json.dumps(JsonInfo['totalResults']))
        if int(Resultados) < 2:
            return ()

        for articles in JsonInfo['articles']:

            URL = articles['url']
            noticia = extractParagraphs(URL)
            if noticia == ():
                continue

            setList.append({'url': URL, 'value': noticia})

    except Exception:
        return()

    return(setList)

def executeHttpRequest(pageNumber, pagesize, query):
    url = 'https://newsapi.org/v2/everything?q=' + query + '&page=' + str(pageNumber) + '&pageSize=' + str(
        pagesize) + '&apiKey=' + _apiKey
    response = requests.get(url)
    JsonInfo = response.json()

    if JsonInfo['status'] == 'error' and JsonInfo['code'] == 'rateLimited':
        print('Rate Limit! ' + _apiKey)
        changeApiKey()
        JsonInfo = executeHttpRequest(pageNumber, pagesize, query)

    return JsonInfo

def extractParagraphs(URL):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;'
            ' Intel Mac OS X 10_10_1) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:

        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        p_tags = soup.find_all('p')

        p_tags_texto = [tag.get_text().strip() for tag in p_tags]

        frase_lista = [frase for frase in p_tags_texto if not '\n' in frase]
        frase_lista = [frase for frase in frase_lista if '.' in frase]

        noticia = '\n'.join(frase_lista)

    except Exception:

        traceback.print_exc()
        print('notfound! - ' + URL)
        return()

    return(noticia)