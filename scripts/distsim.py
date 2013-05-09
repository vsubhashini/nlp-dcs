#! /usr/bin/python

import bz2
import sys
import re
import operator

def main(argv):

    pred = sys.argv[1]

    f1 = "data/dbpedia.types.db2"
    f2 = "../distsim/wackypedia.sent"
    f3 = "stopwords"
    f1 = open(f1, 'r')
    f2 = open(f2, 'r')
    f3 = open(f3, 'r')

    stopwords = f3.readline().strip()
    stopwords = stopwords.split(',')
    stopwords += ['.']
    print stopwords
    

    outf1 = open("typesim", 'w')

    types = [pred] 
    values = set() 
    preds = set(types)
    #print types
   
    line = f1.readline()
    pattern_pred = '[^(]*'
    pattern_value = '\'.*\''
    i = 0
    while line != "" and i < 1000:
        match = re.findall(pattern_pred, line)[0]
        #print match
        if match in types:
            value = re.findall(pattern_value, line)[0]
            #outf1.write(line)
            value = value.strip('\'')
            paren = value.find('(')
            if paren != -1:
                value = value[0:paren]
            values.add(value) 
            #print value 
            #print line 
        line = f1.readline()
        #i+=1
    print values

    words = {}

    i=0
    line = f2.readline()
    while line != "" and i < 10000:
        #print line
        for value in values:
            #print value
            if value not in stopwords and value + " " in line:
                #print line
                #print value
                w = line.lower()
                w = w.split()
                for word in w:
                    if word not in stopwords:
                        if word in words:
                            words[word] += 1
                        else:
                            words[word] = 1
        line = f2.readline()
        #i+=1

    words = sorted(words.iteritems(), key=operator.itemgetter(1))
    words = words[-50:]

    for word in words:
        print word 
    
                       
    f1.close()
    f2.close()
    outf1.close()

if __name__ == "__main__":
   main(sys.argv[1:])

