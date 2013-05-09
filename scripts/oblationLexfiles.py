#! /usr/bin/python
#  Reads the distributional vectors based on wackypedia to create lexicon files for oblation 

import re
import predArity

predTriggers={}

def readTrigsFromFile(wackyTrigFile):
  """Reads the file containing wacky based triggers, and creates dictionary"""
  pred_pattern="^pred:(\w+)"
  with open(wackyTrigFile, 'r') as infd:
    for line in infd:
      if line.startswith("pred:"):
        preds=re.findall(pred_pattern, line)
        predicate=preds[0]
        if predTriggers.get(predicate) is None:
          predTriggers[predicate]=[]
      else:
        trigger=line.strip()
        predTriggers[predicate].append(trigger)
  return predTriggers

def createLexiconFile(predTriggers, vecCount, outFile, predArity):
  """write out the predicate triggers as in lexicon.dlog file format"""
  with open(outFile, 'w') as opfd:
    firstLine="_include('../../general/lexicon.dlog').\n\n%Lexical triggers\n"
    opfd.write(firstLine)
    beginPhrase="_lex(['"
    #endPhrase="/2
    endPhrase="']).\n"
    for predicate in predTriggers:
      triggerList=""
      count=0
      for trigger in predTriggers[predicate]:
        triggerList=triggerList+trigger+"', '"
        count+=1
        if count==vecCount:
          break
      if(predArity.get(predicate)!=None):
        line=beginPhrase+triggerList[0:-4]+"'], ['"+predicate+"/"+str(predArity[predicate])+endPhrase
        #line=beginPhrase+trigger+"'], ['"+predicate+endPhrase
        opfd.write(line)

def main():
  #wackyTriggersFile="../am_dcs-1.0/lexiconFiles/wacky25geobaseTrigs"
  #baseOut="../am_dcs-1.0/lexiconFiles/LexOblation/geobaseLex/wackygeobaseLex"
  #baseOut="wackygeobaseLex"
  #wackyTriggersFile="../am_dcs-1.0/lexiconFiles/wacky25geoqryTrigs"
  #baseOut="../am_dcs-1.0/lexiconFiles/LexOblation/geoqryLex/wackygeoqryLex"
  wackyTriggersFile="../am_dcs-1.0/lexiconFiles/wacky25geopredsTrigs"
  baseOut="../am_dcs-1.0/lexiconFiles/LexOblation/predLex/wackygeopredLex"
  ext=".dlog"
  predArities=predArity.getAllPredArity()
  predTriggers=readTrigsFromFile(wackyTriggersFile)
  for i in range(1,13):
    outFile=baseOut+str(i)+ext
    createLexiconFile(predTriggers, i, outFile, predArities)


if __name__=="__main__":
  main()
