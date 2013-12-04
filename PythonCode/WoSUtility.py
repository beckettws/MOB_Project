#! /usr/bin/env python

""" 
   Author : Sebastian Grauwin (http://www.sebastian-grauwin.com/)
   Copyright (C) 2012
   All rights reserved.
   BSD license.
"""
#Acronym definition: WoS/wos refers to Web of Science files generically, ignoring
#                    how a short record file is output from Web of Knowledge, while
#                    a full record file comes from Web of Science


#Contains:
#CLASS wosLine      --  For parsing the columns of a single line in a Web of Science file,
#                       either short (Web of Knowledge) or full (Web of Science) format
#CLASS wosFile      --  Reads an entire WoS file and applies an user specified function
#                       to each line. (Depends on wosLine.)
#CLASS wosCalculate --  

import os
import sys
import glob
import numpy
import argparse
import Utility

## ##################################################
## ##################################################
## ##################################################

class wosLine:
    
    def __init__(self):
        self.fileformat = ""
        self.PT = "" ## Publication Type (J=Journal; B=Book; S=Series)
        self.AU = "" ## Authors
        self.BA = "" ## Book Authors
        self.BE = "" ## Book Editor
        self.GP = "" ## Book Group Authors
        self.AF = "" ## Author Full Name
        self.CA = "" ## Group Authors
        self.TI = "" ## Document Title
        self.SO = "" ## Publication Name
        self.SE = "" ## Book Series Title
        self.LA = "" ## Language
        self.DT = "" ## Document Type
        self.CT = "" ## Conference Title 
        self.CY = "" ## Conference Date 
        self.CL = "" ## Conference Location 
        self.SP = "" ## Conference Sponsors 
        self.FO = "" ## Funding Organization
        self.DE = "" ## Author Keywords
        self.ID = "" ## Keywords Plus
        self.AB = "" ## Abstract
        self.C1 = "" ## Author Address
        self.RP = "" ## Reprint Address
        self.EM = "" ## E-mail Address
        self.FU = "" ## Funding Agency and Grant Number
        self.FX = "" ## Funding Text
        self.CR = "" ## Cited References
        self.NR = "" ## Cited Reference Count
        self.TC = "" ## Times Cited
        self.Z9 = "" ## 
        self.PU = "" ## Publisher
        self.PI = "" ## Publisher City
        self.PA = "" ## Publisher Address
        self.SN = "" ## ISSN
        self.BN = "" ## ISBN
        self.J9 = "" ## 29-Character Source Abbreviation
        self.JI = "" ## ISO Source Abbreviation
        self.PD = "" ## Publication Date
        self.PY = 0  ## Year Published
        self.VL = "" ## Volume
        self.IS = "" ## Issue
        self.PN = "" ## Part Number
        self.SU = "" ## Supplement
        self.SI = "" ## Special Issue
        self.BP = "" ## Beginning Page
        self.EP = "" ## Ending Page
        self.AR = "" ## Article Number
        self.DI = "" ## Digital Object Identifier (DOI)
        self.D2 = "" ## 
        self.PG = "" ## Page Count
        self.P2 = "" ## 
        self.WC = "" ## Web of Science Category
        self.SC = "" ## Subject Category
        self.GA = "" ## Document Delivery Number
        self.UT = "" ## Unique Article Identifier

    def parseLine(self, fileformat, line, defCols, numCols):

        self.fileformat = fileformat
        if(fileformat == "short"):
            self.parseShortLine(line, defCols, numCols)
        elif(fileformat == "full"):
            self.parseFullLine(line, defCols, numCols)
        else:
            print("Specifed file format not recognized:",fileformat)
            print("Proceeding using short record format")
            self.parseShortLine(line,defCols,numCols)

    def parseFullLine(self, line, defCols, numCols):
        """
        parse a line of the WoS txt output file for full record
        """
        s = line.split("\t")
        if len(s)==numCols:
            if(s[defCols['PT']]=='J'): self.PT = 'Journal' ## Publication Type (J=Journal; B=Book; S=Series)
            if(s[defCols['PT']]=='B'): self.PT = 'Book' 
            if(s[defCols['PT']]=='S'): self.PT = 'Series' 
            self.AU = s[defCols['AU']] ## Authors
            self.TI = s[defCols['TI']] ## Document Title
            self.SO = s[defCols['SO']] ## Publication Name
            self.DT = s[defCols['DT']] ## Document Type
            self.DE = s[defCols['PT']] ## Author Keywords
            self.ID = s[defCols['ID']] ## Keywords Plus
            self.C1 = s[defCols['C1']] ## Author Address
            self.CR = s[defCols['CR']] ## Cited References
            self.TC = s[defCols['TC']] ## Times Cited
            self.J9 = s[defCols['J9']] ## 29-Character Source Abbreviation
            self.PD = s[defCols['PD']] ## Publication Date
            if s[defCols['PY']].isdigit(): self.PY = int(s[defCols['PY']])
            else:               self.PY = 0  ## Year Published
            self.VL = s[defCols['VL']] ## Volume
            self.IS = s[defCols['IS']] ## Issue
            self.BP = s[defCols['BP']] ## Beginning Page
            self.WC = s[defCols['WC']] ## Web of Science Category
            self.UT = s[defCols['UT']] ## Unique Article Identifier

    def parseShortLine(self, line, defCols, numCols):
        """
        parse a line of the WoS txt output file for short record
        """
        s = line.split("\t")
        if len(s)==numCols:
            if(s[defCols['PT']]=='J'): self.PT = 'Journal' ## Publication Type (J=Journal; B=Book; S=Series)
            if(s[defCols['PT']]=='B'): self.PT = 'Book' 
            if(s[defCols['PT']]=='S'): self.PT = 'Series' 
            self.AU = s[defCols['AU']] ## Authors
            self.TI = s[defCols['TI']] ## Document Title
            self.SO = s[defCols['SO']] ## Publication Name
            self.TC = s[defCols['TC']] ## Times Cited
            self.PD = s[defCols['PD']] ## Publication Date
            if s[defCols['PY']].isdigit(): self.PY = int(s[defCols['PY']])
            else:               self.PY = 0  ## Year Published
            self.VL = s[defCols['VL']] ## Volume
            self.IS = s[defCols['IS']] ## Issue
            self.BP = s[defCols['BP']] ## Beginning Page
            self.UT = s[defCols['UT']] ## Unique Article Identifier

## ##################################################
## ##################################################

class wosFile:
#Opens a Web of Science file, processes each line, and prints the results.
#Takes a general operator function for each line as an argument, along
#with a general printing function.
    
    def __init__(self,result):
        self.result = result

    def defColumns(self,line):

        # initialize
        Cols = ['PT', 'AU', 'TI', 'SO', 'DT', 'DE', 'ID', 'C1', 'CR', 'TC', 'J9', 'PD', 'PY', 'VL', 'IS', 'BP', 'WC', 'UT'];
        defCols = dict();

        # match columns number in "line"
        foo = line.replace('\xef\xbb\xbf','').split('\t')
        for i in range(len(foo)):
            if foo[i] in Cols: 
                defCols[foo[i]] = i
        numCols = len(foo)

        return (defCols, numCols)
            
    def processFile(self,inputFile,operator,fileformat,fileEncoding="utf-8-sig"):
        try:
            # open
            fd = open(inputFile,encoding=fileEncoding)

            aux = 0
            numRecords = 0            
            for line in fd.readlines():
                line = line.strip() # removes \n

                if (line != ""):
                    if (aux == 1): # do not take 1st line into account! 
                        wline = wosLine()
                        wline.parseLine(fileformat, line, defCols, numCols)

                        if(operator.datatest(wline)):
                            self.result = operator.function(self.result,wline)
                            numRecords += 1

                        operator.debugger(numRecords,wline)
                        
                    if (aux == 0): # define columns thanks to 1st line
                        (defCols, numCols) = self.defColumns(line)
                        aux = 1

            # close  
            if inputFile != 'stdin':
                fd.close()
        except IOError:
                print("file does not exist")                      

    def outputResults(self,outputFile,printFunction,param):
        try:
            file = open(outputFile, 'w')
            outputData = printFunction(file,self.result,param)
            file.close()

        except IOError:
            print("could not open file")
        
## #################################################################
## #################################################################
            
class wosLineOperator:
#is passed to wosFile object. Key contents: a function to be executed at each line,
#a variable to contain the results, and a function for printing the formatted output

#BUG: currently does not verify that input functions take correct arguments as needed by processFile

    def defaultDebugger(numRecords,wline):
        #needs to come before __init__ member function
        return True

    def __init__(self,function,datatest,debugger=defaultDebugger):
        self.function = function
        self.debugger = debugger
        self.datatest = datatest

class wosCalculate:
#Used for running an operation on each line of a Web of Science file.
#Creates a wosFile object and passes a wosLineOperator defined using
#local class methods

    def __init__(self,fileformat):
        self.fileformat = fileformat
        
    def runCalculation(self,inputFile,outputFile,
                       function,datatest,result,printFunction,printParam):

        myOperator = wosLineOperator(function, datatest)

        myFile = wosFile(result)
        myFile.processFile(inputFile,myOperator,self.fileformat)
        myFile.outputResults(outputFile,printFunction,printParam)

    def countCitedJournals(self,result,wline):
    #Takes cited reference data from each article record in a Web of Science file
    #and counts frequency of journals over all citations
        citations = wline.CR.split('; ')
        i = 0
        for record in citations:
            entries = record.split(', ')
            try:
                if(len(entries) < 3):
                #assumes last entry is source if some data is missing
                    source = entries[len(entries)-1]
                else:
                    source = entries[2]
                    
                Utility.addToHistogram(result,source,"capitalized")
            except IndexError:
                print("Processing Error. See data:")
                if(i>0):
                    print(citations[i-1],"||-||")
                print(record,"||-||")
                if(i+1 < len(citations)):
                    print(citations[i+1])
                
            i += 1
        return result

    def countJournals(self,result,wline):
    #Takes a Web of Science file and counts the journal of each article record
        return Utility.addToHistogram(result,wline.SO,"capitalized")

## ##################################################
## ##################################################
## ##################################################

if __name__ == "__main__":
    main()

## ##################################################
## ##################################################
## ##################################################

