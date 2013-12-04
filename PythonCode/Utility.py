#! /usr/bin/env python

import os
import sys

def sortDictionary(d,method="ascending_key"):
    #returns a list [(key1,value1),(key2,value2),...] sorted according to method
    if(method == "ascending_key"):
        return sorted(d.items())
    elif(method == "descending_key"):
        return sorted(d.items(),reverse=True)
    elif(method == "ascending_value"):
        return sorted(d.items(),key=lambda x:x[1])
    elif(method == "descending_value"):
        return sorted(d.items(),key=lambda x:x[1],reverse=True)
    elif(method == "unsorted"):
        return d
    else:
        print("Sorting method not recognized:", method)
        return d
    
def printDictionary(file,result,param):
#takes open file plus dictionary, prints in different orders according to param
        sortedResult = sortDictionary(result,param)
        for item in sortedResult:
            file.write(item[0] + "\t" + str(item[1]) + "\n") 
    
def addToHistogram(histogram, newdata, keyformat="capitalized"):
#NOTE: automatically formats dict keys as "First Letter Capitalized"
    if(newdata != ""):
        if(keyformat == "capitalized"):
            newdata = " ".join(w.capitalize() for w in newdata.split())
        elif(keyformat == "lowercase"):
            newdata = newdata.lower()
        elif(keyformat == "uppercase"):
            newdata = newdata.upper()
        #pass any other value for keyformat, like "none" to have no change
            
        try:
            if(newdata in histogram):
                histogram[newdata] += 1
            else:
                histogram[newdata] = 1
        except TypeError:
            print("Result object is not a dictionary: ",type(histogram))

    return histogram
