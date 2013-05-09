#! /usr/bin/python


import bz2
import sys
import re

def main(argv):

    fi = "mappingbased_properties_en.nt.bz2" 
    bfi = bz2.BZ2File(fi, 'r')

    outf = bz2.BZ2File("infoboxes.bz2", 'w')

    x = bfi.readline()
    i = 0
    while x != "" and i < 100:

        print x
        p1 = re.findall('\".*\"', x)
        assert len(p1) <= 1
        if len(p1) == 1:
           p1 = re.findall('[^\"]*', p1[0]) 
        tmp = re.findall('/[^/]*>', x) 
        p2 = []
        for s in tmp:
             p2 += [re.findall('[^/^>]*', s)[1]]

        if len(p1) == 1:
             dbline = p2[1] + "(" + p2[0] + ", " + p1[1] + ")."
        else:
             dbline = p2[1] + "(" + p2[0] + ", " + p2[2] + ")."

        print dbline
        print '\n\n'   
        x = bfi.readline()
        i += 1

    bfi.close()
    outf.close()

if __name__ == "__main__":
   main(sys.argv[1:])

