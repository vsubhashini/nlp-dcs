#! /usr/bin/python
# Get the relations from the database and use these predicates as lexical triggers

import re
import predArity
import wordVector
#from nltk.corpus import wordnet

def camelConvert(camelCaseString):
  """Convert camel case string into a list of predicates"""
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camelCaseString)
  s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
  return [word for word in s2.split("_") if len(word)>0]
  #return s2.split("_") 

def camelNumConvert(camelCaseString):
  """Convert camel case string into a list of predicates"""
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camelCaseString)
  s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
  s2_noNum = re.split(r'\d+',s2)
  return [word for unScWord in s2_noNum for word in unScWord.split("_") if (len(word))>0]

#create a dictionary of lexical triggers for each predicate
def getPredicateTriggers(dbFile):
  """return a dictionary of lexical triggers for each predicate"""
  predTriggers={} # {predicate : set([lexical triggers]), ...}
  predPattern='^(\w+)\('
  with open(dbFile,'r') as dbfd:
    for line in dbfd:
      predicate=re.findall(predPattern, line)
      if(len(predicate)>0):
        if predTriggers.get(predicate[0]) is None:
          predTriggers[predicate[0]]=set()
        triggers = camelConvert(predicate[0])
        for trigger in triggers:
          predTriggers[predicate[0]].add(trigger)
  return(predTriggers)

#create dictionary of lexical triggers based on synonyms of predicates
def getSynPredicateTriggers(dbFile):
  """return a dictionary of lexical triggers  based on wordnet synsets for each predicate"""
  synpredTriggers={} # {predicate : set([lexical triggers]), ...}
  predPattern='^(\w+)\('
  with open(dbFile,'r') as dbfd:
    for line in dbfd:
      predicate=re.findall(predPattern, line)
      if(len(predicate)>0):
        if synpredTriggers.get(predicate[0]) is None:
          synpredTriggers[predicate[0]]=set()
        predicateWords = camelConvert(predicate[0])
        for predicateWord in predicateWords:
          synpredTriggers[predicate[0]].add(predicateWord)
          predSyn=wordnet.synsets(predicateWord)
          triggersUnderScored = [l.name for s in predSyn for l in s.lemmas]
          triggers=[trigger.lower().replace("'","") for triggerWord in triggersUnderScored for trigger in triggerWord.split("_")]
          synpredTriggers[predicate[0]]=synpredTriggers[predicate[0]].union(triggers)
  return(synpredTriggers)

#create a dictionary of lexical triggers from predicates.dlog predicates
def getPredPredicateTriggers(dbFile):
  """return a dictionary of lexical triggers for each predicate"""
  synpredTriggers={} # {predicate : set([lexical triggers]), ...}
  predPattern='\'(\w+)\''
  with open(dbFile,'r') as dbfd:
    for line in dbfd:
      predicate=re.findall(predPattern, line)
      if(len(predicate)>0):
        if synpredTriggers.get(predicate[0]) is None:
          synpredTriggers[predicate[0]]=set()
        predicateWords = camelNumConvert(predicate[0])
        for predicateWord in predicateWords:
          synpredTriggers[predicate[0]].add(predicateWord)
          predSyn=wordnet.synsets(predicateWord)
          triggersUnderScored = [l.name for s in predSyn for l in s.lemmas]
          triggers=[trigger.lower().replace("'","") for triggerWord in triggersUnderScored for trigger in triggerWord.split("_")]
          synpredTriggers[predicate[0]]=synpredTriggers[predicate[0]].union(triggers)
  return(synpredTriggers)

#create dictionary of lexical triggers based on distributional vectors of predicates
def getWackyPredTriggers(dbFile, distVector):
  """return a dictionary of lexical triggers  based on wackypedia distributional vectors for each predicate"""
  synpredTriggers={} # {predicate : set([lexical triggers]), ...}
  predPattern='^(\w+)\('
  count=0
  with open(dbFile,'r') as dbfd:
    for line in dbfd:
      predicate=re.findall(predPattern, line)
      if(len(predicate)>0):
        if synpredTriggers.get(predicate[0]) is None:
          synpredTriggers[predicate[0]]=[]
          predicateWords = camelConvert(predicate[0])
          for predicateWord in predicateWords:
            #print predicateWord
            #synpredTriggers[predicate[0]].add(predicateWord)
            predContext=distVector.getWordVector(predicateWord)
            #print "Context:"
            #print predContext
            for conword in predContext:
              #print "Context Word:"
              #print conword
              count+=1
              synpredTriggers[predicate[0]].append(conword[0])
              if count==50:
                break
  return(synpredTriggers)

#create a dictionary of lexical triggers from predicates.dlog predicates using Wacky distribution
def getWackyPredPredicateTriggers(dbFile, distVector):
  """return a dictionary of lexical triggers for each predicate"""
  synpredTriggers={} # {predicate : set([lexical triggers]), ...}
  predPattern='\'(\w+)\''
  with open(dbFile,'r') as dbfd:
    for line in dbfd:
      predicate=re.findall(predPattern, line)
      if(len(predicate)>0):
        if synpredTriggers.get(predicate[0]) is None:
          synpredTriggers[predicate[0]]=[]
          predicateWords = camelNumConvert(predicate[0])
          for predicateWord in predicateWords:
            #synpredTriggers[predicate[0]].add(predicateWord)
            predContext=distVector.getWordVector(predicateWord)
            for conword in predContext:
              synpredTriggers[predicate[0]].append(conword[0])
  return(synpredTriggers)

def writeTrigsToFile(predTriggers, trigOutFile):
  """Write out the predicates and triggers to a file.
       Useful for wackypedia predicates"""
  with open(trigOutFile, 'w') as opfd:
    for predicate in predTriggers:
      line="pred:"+predicate+"\n"
      opfd.write(line)
      for trigger in predTriggers[predicate]:
        trigline=trigger+"\n"
        opfd.write(trigline)

def createLexiconFile(predTriggers, outFile, predArity):
  """write out the predicate triggers as in lexicon.dlog file format"""
  with open(outFile, 'w') as opfd:
    firstLine="_include('../../general/lexicon.dlog').\n\n%Lexical triggers\n"
    opfd.write(firstLine)
    beginPhrase="_lex(['"
    #endPhrase="/2
    endPhrase="']).\n"
    for predicate in predTriggers:
      triggerList=""
      for trigger in predTriggers[predicate]:
        triggerList=triggerList+trigger+"', '"
      if(predArity.get(predicate)!=None):
        line=beginPhrase+triggerList[0:-4]+"'], ['"+predicate+"/"+str(predArity[predicate])+endPhrase
        #line=beginPhrase+trigger+"'], ['"+predicate+endPhrase
        opfd.write(line)
    #include extra lexicon files?
    #extraLines="\n\n%Other lexicon files\n"
    #opfd.write(extraLines)
    #for i in range(1,3):
    #  extraLines="_include('lexicon"+str(i)+".dlog') :- lexmode("+str(i)+").\n"
    #  opfd.write(extraLines)

def main():
  #databaseFile="../data/inputFiles/geo_db_2c"
  #databaseFile="../data/inputFiles/5lines_geo_db"
  #databaseFile="data/geobase.dlog"
  #databaseFile="../am_dcs-1.0/domains/dbquery/geoquery/1/geobase.dlog"
  #databaseFile="../am_dcs-1.0/domains/dbquery/geoquery/1/geoquery.dlog"
  databaseFile="../am_dcs-1.0/domains/dbquery/general/predicates.dlog"
  #databaseFile="../dcs-1.0/domains/dbquery/geoquery/1/geoquery.dlog"
  #databaseFile="../dcs-1.0/domains/dbquery/general/predicates.dlog"
  #outputSynLexFile="../data/outputFiles/genPredSynLexicon.dlog"
  #outputLexFile="../am_dcs-1.0/lexiconFiles/geobaseBaseLexicon.dlog"
  #outputLexFile="../am_dcs-1.0/lexiconFiles/geoqueryBaseLexicon.dlog"
  #outputLexFile="data/geobaseWackyLexicon.dlog"
  #outputLexFile="../am_dcs-1.0/lexiconFiles/geobaseWackyLexicon.dlog"
  #outputLexFile="../am_dcs-1.0/lexiconFiles/geoqryWackyLexicon.dlog"
  #outputLexFile="../am_dcs-1.0/lexiconFiles/geopredWackyLexicon.dlog"
  #wackyVecOut="../am_dcs-1.0/lexiconFiles/wacky25geobaseTrigs"
  #wackyVecOut="../am_dcs-1.0/lexiconFiles/wacky25geoqryTrigs"
  wackyVecOut="../am_dcs-1.0/lexiconFiles/wacky25geopredsTrigs"
  distVector=wordVector.distVector()
  #predTriggers=getWackyPredTriggers(databaseFile, distVector)
  predTriggers=getWackyPredPredicateTriggers(databaseFile, distVector)
  #outputSynLexFile="../data/outputFiles/geobaseSynLexicon.dlog"
  #outputSynLexFile="../data/outputFiles/SynPredicateLexicon.dlog"
  #outputSynLexFile="../data/outputFiles/geoquerySynLexicon.dlog"
  #outputSynLexFile="../data/outputFiles/SynPredicateGeoBaseLexicon.dlog"
  #predTriggers=getPredicateTriggers(databaseFile)
  #synpredTriggers=getSynPredicateTriggers(databaseFile)
  #synpredTriggers=getPredPredicateTriggers(databaseFile)
  predArities=predArity.getAllPredArity()
  writeTrigsToFile(predTriggers,wackyVecOut)
  #createLexiconFile(predTriggers, outputLexFile, predArities)
  #createLexiconFile(synpredTriggers, outputSynLexFile, predArities)

if __name__=="__main__":
  main()
