#! /usr/bin/env python

#Reads two column, tab-delimited files with keyword"\t"value structure
#Merges data from multiple files.

import os
import sys
import glob
import WoSUtility
import Utility

class HistogramTable:

    def __init__(self):
        self.table = dict()
        self.colHeaders = []

    def readFile(self,inputFile,index,colNum):
    #BUG: doesn't handle empty lines or other inputs intelligently
        try:
            file = open(inputFile,encoding="utf-8-sig")
            for line in file.readlines():
                line = line.strip()
                entries = line.split("\t")
                sourceName = entries[0].lower() #sets all names to lower case
                if(sourceName not in self.table):
                    self.table[sourceName] = [0]*colNum ##add a list of colNum zeroes to dict under sourceName
                try:
                    self.table[sourceName][index] += int(entries[1]) ##update the col value at [index] for that list in dict
                    if(sourceName == "systematic zoology"):
                        print(self.table[sourceName],entries[1],index)
                except IndexError:
                    print("Table accessed incorrectly at column number", index, "for journal", sourceName,"while reading file",inputFile)
        except IOError:
            print ("could not open file",inputFile)

    def makeTable(self,filedir,inputFileList,columnNames):
    #BUG: will screw up if makeTable is called twice on different files
        self.colHeaders = columnNames

        index = 0
        numFiles = len(inputFileList)
        for item in inputFileList:
            self.readFile(filedir+item,index,numFiles)
            index += 1

    def printTable(self,outputFile,spacer="\t",sortingMethod = "ascending_key"):
        try:
            file = open(outputFile, mode='w')
            #print column headers to first line of file separated by spacer string (default to tab)
            #first column is reserved for source names of journals
            file.write(spacer + spacer.join(self.colHeaders) + "\n")

            sortedTable = Utility.sortDictionary(self.table,sortingMethod)
            #returns a list

            for item in sortedTable:
                file.write(item[0] + spacer + spacer.join(map(str,item[1])) + "\n")
                #writes the row name and turns each item in the list to a string before joining

            file.close()
        except IOError:
            print("Could not open file",outputFile)




## ##################################################
## ##################################################
## ##################################################

#if __name__ == "__main__":
