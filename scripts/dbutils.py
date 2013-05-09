#!/usr/bin/python
# some useful utilities

def writeToFile(dataList, outputFile):
  ofid = open(outputFile, 'w+')
  for data in dataList:
    ofid.write(data + "\n")
  ofid.close() 

