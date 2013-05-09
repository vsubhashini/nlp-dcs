#! /usr/bin/python


import bz2
import sys

def main(argv):

    #f = bz2.BZ2File("infoboxes.bz2", 'r') 
    f = bz2.BZ2File("enwiki-latest-pages-articles.xml.bz2", 'r')
    for i in range(0, 10000):
        x = f.readline()
        print x

    f.close()

if __name__ == "__main__":
   main(sys.argv[1:])

