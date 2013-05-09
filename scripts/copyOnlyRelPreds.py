#!/usr/bin/python

relevantPredFile="../geo5CK_pred"

#lexiconFile="../am_dcs-1.0/lexiconFiles/dbpWNsyn2Lexicon.dlog"
#outputLexFile="../am_dcs-1.0/lexiconFiles/geo5CKWNsyn2Lexicon.dlog"

lexiconFile="../am_dcs-1.0/lexiconFiles/dbpWackyPred2Lexicon.dlog"
outputLexFile="../am_dcs-1.0/lexiconFiles/geo5CKWacky2Lexicon.dlog"

def readRelPreds(relevantPredFile):
  """Read relevant predicates into a list"""
  relPreds=set()
  with open(relevantPredFile, 'r') as infd:
    for line in infd:
      predicate=line.strip()
      relPreds.add(predicate)
  return relPreds

def createSubsetLexFile(relPreds, inFile, outFile):
  "Create a subset lexicon file based on the relevant predicates only"
  opfd = open(outFile, 'w')
  count=0
  with open(inFile, 'r') as infd:
    for lexTrigLine in infd:
      for relPred in relPreds:
        predform=relPred+"/2"
        if predform in lexTrigLine:
          #print relPred
          #print lexTrigLine
	  opfd.write(lexTrigLine)
          #count+=1
        #if count==10:
        #  break
  opfd.close()

def main():
  relPreds = readRelPreds(relevantPredFile)
  createSubsetLexFile(relPreds, lexiconFile, outputLexFile)

if __name__=="__main__":
    main()
