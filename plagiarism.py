######################
# TTS - Assignment 3 #
# s0808798           #
######################

import os, math, string, md5, cProfile
from Lab2Support import *
from operator import itemgetter
from nltk.corpus import stopwords

swords = stopwords.words('english')
plagiarism = []

def textopener():  
  path = 'train/'
  files = os.listdir(path)
  dict = {}
  for infile in files[1:]: # in OS X the first file is the .DS_Store
	tokens = re.split('[\\s]+',readFile(path+infile))
	sccount = 0
	i = 0
	while (sccount < 1):
		if (tokens[i].count(":") != 0):
			sccount += 1
		i += 1
	text = tokens[i:]
	a = 0
	n = 0
	while n < len(text):
		for p in string.punctuation:
			try:
				s = text[n].split(p)
				if (s[0] != ''):
					text[n] = s[0]
					if (s[1] != ''):
						text.insert(n+1, s[1])
				elif (s[1] != ''):
					text[n] = s[1]
				else:
					text.pop(n)
				#print "removed " + str(p) + " and got: " + text[n]
			except:
				a = 0
		n += 1
	dict[infile.split('.')[0]] = text
  return dict

texts = textopener()

def exactduplicate(text1, text2, lower):
	bool = True
	exactduplicate = False
	if (len(text1) != len(text2)):
		bool = False
	n = 0
	while (bool):
		if lower:
			if (text1[n].lower() != text2[n].lower()):
				bool = False
			else:
				if (len(text1) - 1 == n):
					exactduplicate = True
					bool = False
		else:
			if (text1[n] != text2[n]):
				bool = False
			else:
				if (len(text1) - 1 == n):
					exactduplicate = True
					bool = False
		n += 1
	return exactduplicate
	
def q2(txts):
	keys = txts.keys()
	exactduplicates = []
	i = 0
	while i < len(keys):
		#print str(i) + " out of " + str(len(keys))
		n = i + 1
		while n < len(keys):
			if (exactduplicate(txts[keys[i]], txts[keys[n]], True)):
				plagiarism.append([keys[i], keys[n]])
			n += 1
		i += 1
	
		
#q2(texts)
print "exact duplicates"
print plagiarism

def createhash(txts):
	md5hash = {}
	keys = txts.keys()
	for k in keys:
		for w in txts[k]:
			if (swords.count(w) == 0):
				try:
					if(md5hash[w.lower()] != ''):
						hashash = True
				except:
					md5hash[w.lower()] = bin(int(md5.new(w.lower()).hexdigest(), 16))[2:]
	#print len(md5hash)
	return md5hash
			
#createhash(texts)

def wordfreq(text):
	freq = {}
	distinct = set(text)
	for d in distinct:
		if (swords.count(d) == 0):
			try:
				freq[d.lower()] += text.count(d)
			except:
				freq[d.lower()] = text.count(d)
	#freq = sorted(freq.items(), key=itemgetter(1), reverse=True)
	return freq
	
#print wordfreq(texts[texts.keys()[0]])

def fprints(txts):
	bits = createhash(txts)
	fingerprints = {}
	keys = txts.keys()
	for kys in keys:
		f = wordfreq(txts[kys])
		i = 0
		fprint = []
		while i < 128:
			fprint.append(0)
			i += 1
		fkeys = f.keys()
		for k in fkeys:
			n = 0
			if (len(bits[k]) < 128):
				#print "not long enough: " + str(len(bits[k]))
				while (len(bits[k]) + n < 128):
					fprint[n] -= f[k]
					n += 1
			m = 0
			while m < len(bits[k]):
				if (bits[k][m] == '0'):
					fprint[n-1+m] -= f[k]
				else:
					fprint[n-1+m] += f[k]
				m += 1
		k = 0
		while (k < len(fprint)):
			if (fprint[k] > 0):
				fprint[k] = 1
			else:
				fprint[k] = 0
			k += 1
		#print fprint
		fingerprints[kys] = fprint
	return fingerprints

#print fprints(texts)

def nearduplicate(fprint1, fprint2):
	bool = True
	nearduplicate = False
	s = 0
	n = 0
	while n < len(fprint1):
		s += math.fabs(fprint1[n]-fprint2[n])
		n += 1
	if (s < 6):
		nearduplicate = True
	"""while (bool):
		if (fprint1[n] != fprint2[n]):
			bool = False
		else:
			if (len(fprint1) - 1 == n):
				nearduplicate = True
				bool = False
		n += 1"""
	return nearduplicate

def q3(txts):
	nearduplicates = []
	fingerprints = fprints(txts)
	keys = fingerprints.keys()
	i = 0
	while i < len(keys):
		#print str(i) + " out of " + str(len(keys))
		n = i + 1
		while n < len(keys):
			if (nearduplicate(fingerprints[keys[i]], fingerprints[keys[n]])):
				if ((plagiarism.count([keys[i], keys[n]]) == 0) & (plagiarism.count([keys[n], keys[i]]) == 0)):
					plagiarism.append([keys[i], keys[n]])
			n += 1
		i += 1
	#return nearduplicates
	
#q3(texts)
print "exact + near duplicates"
print plagiarism

def finnplateau(txts):
	resultmap = {}
	keys = txts.keys()
	l = len(keys)
	m = 0
	for k in keys:
		print "text " + str(m) + " out of " + str(l-1)
		text = txts[k]
		n = len(text)
		a = 0
		c = 100
		L = 0
		results = {}
		while (a < n-2):
			fastskip = False
			while ((a < n-2) and not(text[a].isdigit())):
				L += 1
				a += 1
				fastskip = True
			if fastskip:
				i = a
			else:
				i = a+1
			M = 0
			while (i < n):
				if (text[i].isdigit()):
					M += 1
				b = i+1
				R = 0
				firstnextnumber = True
				skip = False
				while (b < n):
					if not(text[b].isdigit()):
						R += 1
					elif firstnextnumber:
						i = b
						skip = True
					b += 1
				sum = L + c*M + R
				if (i+1-a > 1):
					results[(a,i+1)] = sum
				if not(skip):
					i += 1
			a += 1
		results = sorted(results.items(), key=itemgetter(1), reverse=True)[:25]
		resultmap[k] = results
		m += 1
	return resultmap
	
#print finnplateau(texts[texts.keys()[0]])

def q4(txts):
	map = finnplateau(txts)
	copiedparts = []
	keys = map.keys()
	i = 0
	b = plagiarism[:]
	while i < len(keys):
		n = i+1
		while n < len(keys):
			for part1 in map[keys[i]]:
				for part2 in map[keys[n]]:
					matching = exactduplicate(txts[keys[i]][part1[0][0]:part1[0][1]], txts[keys[n]][part2[0][0]:part2[0][1]], False)
					if (matching):
						#if ((b.count([keys[i], keys[n]]) == 0)  & (b.count([keys[n], keys[i]]) == 0)):
							#print str(txts[keys[i]][part1[0][0]:part1[0][1]]) + " " + str(txts[keys[n]][part2[0][0]:part2[0][1]]) + str((keys[i], keys[n]))
						if ((plagiarism.count([keys[i], keys[n]]) == 0)  & (plagiarism.count([keys[n], keys[i]]) == 0)):
							plagiarism.append([keys[i], keys[n]])
			n += 1
		i += 1
	#return copiedparts
	
#q4(texts)
print "exact+near duplicates along with copiers"
print plagiarism

def writeanswer():
	f = open('duplicate.txt', 'w')
	for p in plagiarism:
		f.write(str(p[0])+'-'+str(p[1])+'\n')
	f.close()
	
#writeanswer()