import os
import sys
import WoSUtility
import Utility

#Script command references

#Count frequency of journals cited by article records in a WOS file
pathToData = "/Users/beckettsterner/Documents/WorkFiles/ResearchProjects/Postdoc/Data/Journals/savedrecs.txt"
pathToOutput = "/Users/beckettsterner/Documents/WorkFiles/ResearchProjects/Postdoc/Data/Journals/processedcitations.txt"
myProcedure = WoSUtility.wosCalculate(fileformat="full")
datatest = lambda x: (x.CR != "")
#x will be a WoSLine object
myProcedure.runCalculation(pathToData,pathToOutput,
                           myProcedure.countCitedJournals,
                           datatest, dict(),
                           Utility.printDictionary,"descending_value")

#Count frequency of source journals within each short format file contained in a directory
pathToData = "/Users/beckettsterner/Documents/WorkFiles/ResearchProjects/Postdoc/Data/KeywordSearches/ByArticle/"
pathToOutput = "/Users/beckettsterner/Documents/WorkFiles/ResearchProjects/Postdoc/Data/KeywordSearches/ByJournal/"
myProcedure = WoSUtility.wosCalculate(fileformat="short")
datatest = lambda x: (x.SO != "")
#x will be a WoSLine object

for filename in os.listdir(pathToData):
    if(filename[0] is not '.'):
    #should exclude '.DS_Store' file
        print(filename)
        output = dict()
        myProcedure.runCalculation(pathToData+filename,pathToOutput+filename,
                                   myProcedure.countJournals,
                                   datatest, output,
                                   Utility.printDictionary, "descending_value")

#Count frequency of source journals in a short format WOS file
pathToData = "/Users/beckettsterner/Documents/WorkFiles/ResearchProjects/Postdoc/Data/Journals/savedrecs.txt"
pathToOutput = "/Users/beckettsterner/Documents/WorkFiles/ResearchProjects/Postdoc/Data/Journals/processedcitations.txt"
myProcedure = WoSUtility.wosCalculate(fileformat="short")
datatest = lambda x: (x.SO != "")
#x will be a WoSLine object

myProcedure.runCalculation(pathToData+filename, myProcedure.countJournals,
                           datatest, dict(),
                           Utility.printDictionary, "descending_value")

#Merge multiple histogram files into single table and print to file
#WARNING: some code in HistogramTable may be out of date
pathToData = "/Users/beckettsterner/Documents/WorkFiles/ResearchProjects/Postdoc/Data/KeywordSearches/ByJournal/"
pathToOutput = "/Users/beckettsterner/Documents/WorkFiles/ResearchProjects/Postdoc/Data/KeywordSearches/"

directoryList = os.listdir(pathToData)
inputFileList = [x for x in directoryList if ".txt" in x]

#inputFileList = ['WoSsearch-cladistic.txt']

myTable = CompareJournals.HistogramTable()
myTable.makeTable(pathToData,inputFileList,inputFileList)
myTable.printTable(pathToOutput+"table.txt")
