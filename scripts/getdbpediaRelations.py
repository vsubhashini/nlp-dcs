#!/usr/bin/python
# Get the relations from dbpedia infobox data (e.g Name from Name(.,.))

import re
import dbutils

def getDbRelations(dbpediaFile):
  """Get all relations in the dbpedia database"""
  relSet = set()
  rel_pattern = '(\w+)\('
  with open(dbpediaFile, 'r') as dbfid:
    for line in dbfid:
      rels = re.findall(rel_pattern, line)
      if len(rels)>0:
	relSet.add(rels[0])
  return relSet

def main():
  dbpediaFile="../data/inputFiles/4kdbpedia.infoboxes.db2"
  dbpediatypeFile="../data/inputFiles/4kdbpedia.types.db2"
  relSet = getDbRelations(dbpediaFile)
  dbutils.writeToFile(relSet, "../data/outputFiles/relations_dbinfobox.txt")
  relSet = getDbRelations(dbpediatypeFile)
  dbutils.writeToFile(relSet, "../data/outputFiles/relations_dbtypes.txt")

if __name__=="__main__":
    main()
