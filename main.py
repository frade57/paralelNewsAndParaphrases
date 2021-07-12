from createQueryList import stripTopHeadlinesToQ
from getNewsFromUrl import getNews
from findParalelNews import simNews
from findParaphrases import findParaphrase
from separatePhrases import createPhraseList


def main():
    stripTopHeadlinesToQ()
    print("Lista de queries criada")
    getNews()
    print("Noticias recolhidas")
    simNews()
    print("Notícias paralelas guardadas")
    createPhraseList()
    print("Lista de frases criada")
    findParaphrase()
    print("Paráfrases guardadas")

if __name__ == "__main__":
    print("Started")
    main()




