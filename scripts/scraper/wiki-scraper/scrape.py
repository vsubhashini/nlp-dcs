#! /usr/bin/python


import bz2
import sys

def main(argv):

    fi = "enwiki-latest-pages-articles.xml.bz2"
    bfi = bz2.BZ2File(fi, 'r')

    outf = bz2.BZ2File("infoboxes.bz2", 'w')
    print_flag = False 

    x = bfi.readline()
    while x != "":
        if x.find("{{ Infobox") != -1 or print_flag:
            print_flag = True 
            outf.write(x) 
            if x == "}}\n":
               print_flage = False
        x = bfi.readline()
 

    bfi.close()
    outf.close()

if __name__ == "__main__":
   main(sys.argv[1:])

