#! /usr/bin/python
# Get the relations from the database and use these predicates as lexical triggers

import re

#create a dictionary of predicates and their arities
def getPredArity(geoQueryFile):
  """return a dictionary of lexical triggers for each predicate"""
  predTriggers={} # {predicate : set([possible arities]), ...}
  predPattern='^([a-zA-Z0-9_]+)\('
  contentPattern='\(([a-zA-Z,()_]+)\)'
  with open(geoQueryFile,'r') as dbfd:
    for line in dbfd:
      predicate=re.findall(predPattern, line)
      contents=re.findall(contentPattern, line)
      if(len(predicate)>0 and len(contents)>0):
        if predTriggers.get(predicate[0]) is None:
          predTriggers[predicate[0]]=set()
        arity = contents[0].count(',')+1
        #print predicate[0], arity
        predTriggers[predicate[0]].add(arity)
  return(predTriggers)

#extract arity from lexicon.dlog
def getLexPredArity(lexiconFile):
  """return a dictionary of lexical triggers for each predicate"""
  predTriggers={} # {predicate : set([possible arities]), ...}
  predPattern='\'([a-zA-Z_]+/\d)\''
  with open(lexiconFile,'r') as dbfd:
    for line in dbfd:
      predicateFull=re.findall(predPattern, line)
      if(len(predicateFull)>0):
        predicate, arity = predicateFull[0].split("/")
        #print predicate, arity
        if predTriggers.get(predicate) is None:
          predTriggers[predicate]=set()
        #print predicateFull[0]#, arity
        predTriggers[predicate].add(arity)
  return(predTriggers)

def getAllPredArity():
  geoQueryFile="../am_dcs-1.0/domains/dbquery/geoquery/1/geoquery.dlog"
  predTrigs1=getPredArity(geoQueryFile)
  lexiconFile="../am_dcs-1.0/domains/dbquery/general/lexicon.dlog"
  predTrigs2=getLexPredArity(lexiconFile)
  allPredTrigs=dict(predTrigs1.items() + predTrigs2.items())
  for predicate in allPredTrigs:
    allPredTrigs[predicate]=min(allPredTrigs[predicate])
  allPredTrigs['density']-=1
  allPredTrigs['city']-=1
  allPredTrigs['low_point']+=1
  allPredTrigs['high_point']+=1
  return allPredTrigs

def printPredArity(predTriggers):
  for predicate in predTriggers:
    #print predicate, min(predTriggers[predicate])
    print predicate, predTriggers[predicate]

def main():
  geoQueryFile="../dcs-1.0/domains/dbquery/geoquery/1/geoquery.dlog"
  #predTriggers=getPredArity(geoQueryFile)
  #printPredArity(predTriggers)
  lexiconFile="../dcs-1.0/domains/dbquery/general/lexicon.dlog"
  #predTrig2=getLexPredArity(lexiconFile)
  predTrigs=getAllPredArity()
  printPredArity(predTrigs)

if __name__=="__main__":
  main()
