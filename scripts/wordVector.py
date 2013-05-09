#!/usr/bin/python
#Create a distributional semantic vector for a word (based on wackypedia)

import re
import string
import operator

vectorLen=25

def getPredicates(dbFile):
  """Read predicates from the database"""
  predPattern='^(\w+)\('
  with open(dbFile,'r') as dbfd:
    for line in dbfd:
      predicate=re.findall(predPattern, line)
      if(len(predicate)>0):
        predicatSet.add(predicate[0])

def readStopwords(stopwordFile):
  """Read stopwords into a list"""
  stopwords=set()
  stopwords.add('.')
  with open(stopwordFile, 'r') as infd:
    for line in infd:
      words = line.split(',')
      stopwords = stopwords.union(words)
  return stopwords

class distVector:

  def __init__(self):
    self.stopwords=set(readStopwords("/scratch/cluster/pichotta/ajh/stopwords"))
    #self.stopwords=set(readStopwords("stopwords"))
    self.predicateSet=set()
    self.wordVectors={}

  def getWordVector(self, word):
    """Return the distributional vector for the 
       given word based on context words in the datafile"""
    #dataFile="../distsim/wackypedia.sent"
    dataFile="/scratch/cluster/pichotta/distsim/wackypedia.sent"
    vector = self.wordVectors.get(word)
    if vector is not None:
      return vector
    wordVector={}
    count=0
    with open(dataFile, 'r') as dfile:
      for line in dfile:
        if " "+word+" " in line:
          context = line.lower().rstrip('.')
          #context = context.translate(None, string.punctuation)
          context = context.split()
  	  for relword in context:
  	    if relword not in self.stopwords:
  	      if wordVector.get(relword) is None:
  	        wordVector[relword]=0
  	      wordVector[relword]+=1
              #below for debug
              #count+=1
          #if count>50:
          #  wordVector = sorted(wordVector.iteritems(), key=operator.itemgetter(1))
          #  self.wordVectors[word]= wordVector[-50:]
          #  return self.wordVectors[word]
    wordVector = sorted(wordVector.iteritems(), key=operator.itemgetter(1), reverse=True)
    self.wordVectors[word]= wordVector[:vectorLen]
    return self.wordVectors[word]

  def printVectors(wordVector):
    for word in wordVector:
      print word, str(wordVector[word])

def main():
  dv = distVector()
  riverVec = dv.getWordVector('river')
  print riverVec

if __name__=="__main__":
  main()
