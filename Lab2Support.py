from numpy import *
import os
import re
from operator import itemgetter

def sortMap(wordMap):
	return sorted(wordMap.items(), key=itemgetter(1), reverse=True)

def calculateDistance(word1, word2):
	x = zeros( (len(word1)+1, len(word2)+1) )
	for i in range(0,len(word1)+1):
		x[i,0] = i
	for i in range(0,len(word2)+1):
		x[0,i] = i

	for j in range(1,len(word2)+1):
		for i in range(1,len(word1)+1):
			if word1[i-1] == word2[j-1]:
				x[i,j] = x[i-1,j-1]
			else:
				minimum = x[i-1, j] + 1
				if minimum > x[i, j-1] + 1:
					minimum = x[i, j-1] + 1
				if minimum > x[i-1, j-1] + 1:
					minimum = x[i-1, j-1] + 1
				x[i,j] = minimum

	return x[len(word1), len(word2)]

def readFile(filename):
	f = open(filename, 'r')
	try:
	    content = f.read()
	finally:
	    f.close()
	return content

def buildCategories(wordBase):
	d = dict()
	for word in wordBase:
		code = word # Now, each word is its own category
	        d.setdefault(code, []).append(word)
	return d
	
def saveToFile(data, filename):
	d = dict()
	string = ''
	array = []
	s = set(array)	
	f = open(filename, 'w')
	try:
	    if type(data) == type(string):
	    	f.write(data)
	    if type(data) == type(array):
	    	for d in data:
			f.write(str(d) + '\n')
	    if type(data) == type(s):
		data = list(data)	    	
		for d in data:
			f.write(str(d) + '\n')
	    if type(data) == type(d):
		sortedData = sorted(data.items(), key=itemgetter(0))
		for sd in sortedData:
			f.write(str(sd) + '\n')
	finally:
	    f.close()
	



