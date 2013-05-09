#!/usr/bin/python
# Extract the same geo data as in geobase.dlog from the dbpedia database (with dbpedia schema)
#  For each line in geobase.dlog, extract 1st item in ' '
#    if it is not a number
#      pull all lines containing that word (ignore case) from dbpedia.infobox

import re
import dbutils

def pullFromDbpedia(wordSet, dbpediaFileList, geodbpediaout):
  """Extract all lines containing any word in the wordList as the main item of the dbpedia db""" 
  outfid = open(geodbpediaout, 'w+');
  #item_pattern = '\((.*),'
  item_pattern = '\'([^\']+)\''
  item_pattern2 = '\'([^\']+),'
  for dbpediaFile in dbpediaFileList:
    with open(dbpediaFile, 'r') as dbfid:
      for line in dbfid:
        db_item = re.findall(item_pattern, line)
        db_item2 = re.findall(item_pattern2, line)
        if len(db_item)<1:
  	  print "db_item < 1 %s" %line
  	#better to convert from unicode
        else:
          item = str(db_item[0]).lower()
          item.replace("_"," ")
          #if any(item in word for word in wordSet):
	  if item in wordSet:
	    outfid.write(line)
          #if any(word in item for word in wordSet):
	  #  outfid.write(line)
        if len(db_item2)>0:
          item = str(db_item2[0]).lower()
          item.replace("_"," ")
	  if item in wordSet:
	    outfid.write(line)
  outfid.close()

def getGeoDbItems(geobaseFile):
  """Get the properNoun items (states, cities, rivers, mountains) from geobase.dlog"""
  wordSet = set()
  geo_pattern = '\'([A-Za-z_\s\.]+)\'' #no numbers
  with open(geobaseFile, 'r') as geofd:
    for line in geofd:
      geo_items = re.findall(geo_pattern, line)
      for geo_item in geo_items:
	if len(geo_item)>2:
          wordSet.add(geo_item)
  return wordSet

def main():
  dbpediaFile="../data/inputFiles/4kdbpedia.infoboxes.db2"
  dbpediatypeFile="../data/inputFiles/4kdbpedia.types.db2"
  geobaseFile="../dcs-1.0/domains/dbquery/geoquery/1/geobase.dlog"
  geodbpedia="../data/outputFiles/dbpediaGeobase.dlog"
  dbpediafileList=[]
  dbpediafileList.append(dbpediaFile);
  dbpediafileList.append(dbpediatypeFile);
  #print dbpediafileList
  wordSet = getGeoDbItems(geobaseFile)
  #for item in wordSet:
  #  print item
  dbutils.writeToFile(wordSet, "../data/outputFiles/geobaseItems.txt")
  pullFromDbpedia(wordSet, dbpediafileList, geodbpedia)

if __name__=="__main__":
    main()
