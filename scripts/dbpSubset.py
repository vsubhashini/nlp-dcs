#! /usr/bin/python

import bz2
import sys
import re
import operator

def main():

    f1 = "data/dbpedia.infoboxes.db2"
    f1id = open(f1, 'r')
    namePattern="^(name)\("
    itemPattern="\'([\w\s,\-\.]+)\'"
    f2 = "namefrequencies"
    f2id = open(f2, 'w')

    d = {}
    line = f1id.readline()
    count=0
    while line != "":
        line = line.rstrip()
        name=re.findall(namePattern,line)
        if len(name)>0 and name[0]=="name":
          item=re.findall(itemPattern, line)
          if len(item)<=0:
            print line
          #print item[0]
          if len(item)>0:
            d[item[0]] = 0
            count+=1
        line = f1id.readline()   
        #if count==10:
        #  break

    f1id.close()
    f1id = open(f1, 'r')
    line = f1id.readline()
    count=0
    while line != "": 
        line = line.rstrip()
        item=re.findall(itemPattern, line)
        if d.get(item[0]) is not None:
          d[item[0]] += 1
          count+=1
        line = f1id.readline()
        #if count==200:
        #  break
    f1id.close() 

    d = sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)

    for word, freq in d:
       line="'"+word+"'" + "\t" + str(freq) +"\n"
       f2id.write(line)
    f2id.close()

    print "DONE"

if __name__ == "__main__":
   main()

