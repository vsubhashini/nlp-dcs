#! /usr/bin/python


import bz2
import sys
import re

def main(argv):

    fi = "mappingbased_properties_en.nt.bz2"
    bfi = bz2.BZ2File(fi, 'r')

    #outf = bz2.BZ2File("dbpedia.infoboxes.bz2", 'w')
    outf = open("dbpedia.infoboxes.db", 'w')
    print_flag = False 

    line = bfi.readline()
    counter=0;
    pattern_property = '/(\w+)>'
    pattern_value = '"(\w+.*)"'
    while line != "":
        matches = re.findall(pattern_property, line)
        values = re.findall(pattern_value, line)
        print line;
	"""for m in matches:
	  print m;
	print values;
	"""
	#create db format
	dbline = matches[1] + "(" + matches[0] + ", "
	if len(matches)<3:
	  addline = values[0] + ")."+"\n"
	else:
	  addline = matches[2] + ")."+"\n"
	dbline+=addline;
	#print dbline
	outf.write(dbline)
	if counter<=20:
          line = bfi.readline()
	  counter+=1
	else:
	  break;
 

    bfi.close()
    outf.close()

if __name__ == "__main__":
   main(sys.argv[1:])

