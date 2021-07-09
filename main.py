from createQueryList import stripTopHeadlinesToQ
from getNewsFromUrl import getNews
from findParalelNews import simNews
from findParaphrases import findParaphrase
from separatePhrases import createPhraseList
import schedule
import time

def main():
#stripTopHeadlinesToQ()
    #getNews()
    #simNews()
    #createPhraseList()
    findParaphrase()

if __name__ == "__main__":
    schedule.every(24).hour.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)




