import numpy
import sqlite3

w2v= {}
con = sqlite3.connect('GNewsW2Vsingle.db')

def line2WVector(line):
    vs = line.split()
    v = [float(x) for x in vs[1:]]
    cur = con.cursor()
    cur.execute("insert into words(word, v) values (?, ?)", (vs[0], str(v)))
    con.commit()

    return vs[0], v

def loadW2VFile():
    tempInsert = []
    i = 0
    f = open('GNewsW2Vsingle.txt', 'r', encoding='utf8')
    for s in f:
        word,lista= line2WVector(s)
        w2v[word]= numpy.array(lista)
        i= i+1
        tempInsert.append((word, w2v[word]))

        if len(tempInsert) > 10:
            tempInsert = []
            print('insert ' + str(i))

    return w2v[word]

def createSqlLiteDB():
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS words
                   (word text, v text)''')

    cur.execute('''CREATE INDEX IF NOT EXISTS idx_word ON words (word)''')

    con.commit()

if __name__ == "__main__":
    createSqlLiteDB()
    print('LOADING WORD EMBEDINGS .....')
    n = loadW2VFile()
    print('OK')
