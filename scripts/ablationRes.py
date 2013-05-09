#i!/usr/bin/python
# consolidating ablation test results and plotting graphs

import os
import re
import matplotlib.pyplot as mpl

class Results:
  """Consolidates the results of the ablation tests"""
  class Experiment:
    """represents experiment run with some lexicon - ours,  bridge, general, both"""
    def __init__(self, lextype):
      """lextype (string) defines the type of lexicon used"""
      self.lextype=lextype
      self.trainOracle={} #dictionary of {1: accuracy, 2:accuracy, ..., 12:accuracy}
      self.trainPred={} #dictionary of {1: accuracy, 2:accuracy, ..., 12:accuracy}
      self.testOracle={} #dictionary of {1: accuracy, 2:accuracy, ..., 12:accuracy}
      self.testPred={} #dictionary of {1: accuracy, 2:accuracy, ..., 12:accuracy}
      """self.lexModeBegin=0
      self.lexModeEnd=0
      if(lextype=="ours"):
        self.lexModeBegin=1
        self.lexModeEnd=12
      elif(lextype=="bridge"):
        self.lexModeBegin=13
        self.lexModeEnd=24
      elif(lextype=="general"):
        self.lexModeBegin=25
        self.lexModeEnd=36
      elif(lextype=="both"):
        self.lexModeBegin=37
        self.lexModeEnd=48
      else:
        print "Error in lextype. Case sensitive values: ours, bridge, general, or both."""

  def __init__(self):
    """results initialization"""
    #self.path="/u/ameliaj/nlp_proj/dcs-1.0/state/execs"
    self.path="/home/vsubhashini/courses/nlp/project/am_dcs-1.0/state/execs"
    self.numExp=12  #number of wacky words in experiment 1-12
    self.ours=self.Experiment("ours")
    self.bridge=self.Experiment("bridge")
    self.general=self.Experiment("general")
    self.both=self.Experiment("both")

  def getLexMode(self, currentPath):
    """get lexMode option 1-48, when inside some x.exec directory"""
    modePattern="lexMode=(\d+)"
    fullpath=currentPath+"/options.map"
    with open(fullpath,'r') as opfd:
      for line in opfd:
        if "lexMode" in line:
          mode=re.findall(modePattern,line)[0]
          return mode
    return 0 #error case

  def readAccuracy(self, currentPath):
    """read the train and test oracle and predicted accuracies"""
    acc_pattern="0.(\d+)"
    accuracy={}  #dictionary: tro, trp, teo, tep - train/test oracle/predicate accuracies
    fullpath=currentPath+"/record"
    for line in reversed(open(fullpath,"r").readlines()):
      if "testPredAccuracy" in line:
        accuracy["tep"]=re.findall(acc_pattern, line)[0]
      elif "testOracleAccuracy" in line:
        accuracy["teo"]=re.findall(acc_pattern, line)[0]
      elif "trainPredAccuracy" in line:
        accuracy["trp"]=re.findall(acc_pattern, line)[0]
      elif "trainOracleAccuracy" in line:
        accuracy["tro"]=re.findall(acc_pattern, line)[0]
        break  #read only last iteration and exit
    return accuracy

  def getLexType(self, lexMode):
    if(lexMode>=1 and lexMode<=12):
      return "ours"
    if(lexMode>=13 and lexMode<=24):
      return "bridge"
    if(lexMode>=24 and lexMode<=36):
      return "general"
    if(lexMode>=36 and lexMode<=48):
      return "both"

  def getLexExperiment(self, lexMode):
    """return the experiment corresponding to the lexMode"""
    if(lexMode>=1 and lexMode<=12):
      return self.ours
    if(lexMode>=13 and lexMode<=24):
      return self.bridge
    if(lexMode>=24 and lexMode<=36):
      return self.general
    if(lexMode>=36 and lexMode<=48):
      return self.both

  def fillAccuracy(self, experiment, runkey, accuracyVals):
    """adds the accuracy value to the right experiment's dictionary"""
    experiment.trainOracle[runkey]=(float("0."+accuracyVals["tro"])*100.0)
    experiment.trainPred[runkey]=(float("0."+accuracyVals["trp"])*100.0)
    experiment.testOracle[runkey]=(float("0."+accuracyVals["teo"])*100.0)
    experiment.testPred[runkey]=(float("0."+accuracyVals["tep"])*100.0)

  def readExecs(self):
    """read all execution outputs in the execs folder
       save all accuracies results"""
    for execdir in os.walk(self.path).next()[1]:
      currentPath=self.path+"/"+execdir
      mode=self.getLexMode(currentPath)
      lexMode=int(mode)
      lexType=self.getLexType(lexMode)
      experiment=self.getLexExperiment(lexMode)
      accuracyVals=self.readAccuracy(currentPath)
      runkey= int(lexMode) % self.numExp
      if runkey==0:
        runkey=12
      self.fillAccuracy(experiment, runkey, accuracyVals)

  def printAccuracy(self, lexType, accType):
    """print out the accuracies for a particular experiment and a set of accuracies"""
    experiment=self.both
    if lexType=="ours":
      experiment=self.ours
    elif lexType=="bridge":
      experiment=self.bridge 
    elif lexType=="general":
      experiment=self.general 

    accVals=experiment.testPred
    if accType=="tro":
      accVals=experiment.trainOracle
    elif accType=="trp":
      accVals=experiment.trainPred
    elif accType=="teo":
      accVals=experiment.testOracle

    print "Results for -"+lexType+"- printing accuracy: "+accType
    for key in accVals:
      #value="0."+accVals[key]
      #val=float(value)*100.0
      #accVals[key]=val
      print str(key)+" \t "+str(accVals[key])

  def plotTestGraph(self):
    """Plot the ablation graph"""
    mpl.clf()
    mpl.plot(self.ours.testPred.keys(), self.ours.testPred.values(), marker='x', label='ours')
    mpl.plot(self.bridge.testPred.keys(), self.bridge.testPred.values(), marker='s', label='+bridge')
    mpl.plot(self.general.testPred.keys(), self.general.testPred.values(), marker='^', label='+general')
    mpl.plot(self.both.testPred.keys(), self.both.testPred.values(), marker='o', label='all')
    mpl.xlim(0,14)
    mpl.ylim(0,100)
    mpl.xlabel('Number of triggers per predicate')
    mpl.ylabel('Test Predicate Accuracy')
    mpl.title('Lexical trigger set performance')
    mpl.legend(loc=2)
    mpl.savefig('ablation-test.png')

  def plotTrainGraph(self):
    """Plot the ablation graph"""
    mpl.clf()
    mpl.plot(self.ours.trainPred.keys(), self.ours.trainPred.values(), marker='x', label='ours')
    mpl.plot(self.bridge.trainPred.keys(), self.bridge.trainPred.values(), marker='s', label='+bridge')
    mpl.plot(self.general.trainPred.keys(), self.general.trainPred.values(), marker='^', label='+general')
    mpl.plot(self.both.trainPred.keys(), self.both.trainPred.values(), marker='o', label='all')
    mpl.xlim(0,14)
    mpl.ylim(0,100)
    mpl.xlabel('Number of triggers per predicate')
    mpl.ylabel('Test Predicate Accuracy')
    mpl.title('Lexical trigger set (train) performance')
    mpl.legend(loc=2)
    mpl.savefig('ablation-train.png')

def main():
  res=Results()
  res.readExecs()
  res.printAccuracy("ours","tep")
  res.printAccuracy("bridge","tep")
  res.printAccuracy("general","tep")
  res.printAccuracy("both","tep")
  res.plotTestGraph()
  res.plotTrainGraph()

if __name__=="__main__":
    main()
