######################
# TTS - Assignment 3 #
# s0808798           #
######################

import os, math, string, md5, cProfile, re
from Lab2Support import readFile
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
	
	# clean up the tokens and separate punctuation marks from individual words
	n = 0
	while n < len(text):
		for p in string.punctuation:
			try:
				s = text[n].split(p)
				if (s[0] != ''): #if there's text before the punctuation mark
					text[n] = s[0]
					if (s[1] != ''): #if there's text after the punctuation mark too
						text.insert(n+1, s[1])
				elif (s[1] != ''): #if there's text only after the punctuation mark
					text[n] = s[1]
				else: #if the token is only a punctuation mark
					text.pop(n)
				#print "removed " + str(p) + " and got: " + text[n]
			except:
				pass
		n += 1
	dict[infile.split('.')[0]] = text
  return dict

texts = textopener()

def exactduplicate(text1, text2, lower):
	bool = True
	exactduplicate = False
	t1_len = len(text1)
	t2_len = len(text2)
	if (t1_len != t2_len):
		return exactduplicate
	n = 0
	while (bool):
		if lower:
			if (text1[n].lower() != text2[n].lower()):
				bool = False
			else:
				if (t1_len - 1 == n):
					exactduplicate = True
					bool = False
		else:
			if (text1[n] != text2[n]):
				bool = False
			else:
				if (t1_len - 1 == n):
					exactduplicate = True
					bool = False
		n += 1
	
	#the above approach speeds up computation by a factor of 3 compared to the 
	#very straightforward method below according to cProfile (0.048 s vs 0.168 s)
	"""if lower:
		return map(str.lower, text1) == map(str.lower, text2)
	else:
		return text1 == text2"""
	return exactduplicate
	
def q2(txts):
	keys = txts.keys()
	key_len = len(keys)
	exactduplicates = []
	i = 0
	while i < key_len:
		#print str(i) + " out of " + str(len(keys))
		n = i + 1
		while n < key_len:
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
			# replace 'if (swords.count(w) == 0)', this cuts down 1/3 of the time (0.953s vs 0.666s):
			if not(w in swords): 
				low_w = w.lower()
				try:
					if md5hash[low_w]:
						pass
				except:
					md5hash[low_w] = bin(int(md5.new(low_w).hexdigest(), 16))[2:]
	#print len(md5hash)
	return md5hash
			
#createhash(texts)

def wordfreq(text):
	freq = {}
	distinct = set(text)
	for d in distinct:
		if not(d in swords):
			low_d = d.lower()
			try:
				freq[low_d] += text.count(d)
			except:
				freq[low_d] = text.count(d)
	#freq = sorted(freq.items(), key=itemgetter(1), reverse=True)
	return freq
	
#print wordfreq(texts[texts.keys()[0]])


#implement simhash fingerprinting
def fprints(txts):
	bits = createhash(txts)
	fingerprints = {}
	keys = txts.keys()
	for key in keys: #for every text
		f = wordfreq(txts[key]) #count the number of times each word occurs in a speech
		fprint = [0 for i in range(128)] #initialise the fingerprint
		fkeys = f.keys() #get every word in the current text
		for word in fkeys: #for every word in the current text
			n = 0
			word_len = len(bits[word])
			if (word_len < 128): #ensure all hashes are 128 bits long
				#print "not long enough: " + str(len(bits[k]))
				while (word_len + n < 128):
					#print f[word]
					fprint[n] -= f[word]
					#print fprint
					n += 1
			m = 0
			while m < word_len:
				if (bits[word][m] == '0'):
					fprint[n-1+m] -= f[word]
				else:
					fprint[n-1+m] += f[word]
				m += 1
		k = 0
		fprint_len = len(fprint)
		while (k < fprint_len):
			if (fprint[k] > 0):
				fprint[k] = 1
			else:
				fprint[k] = 0
			k += 1
		#print fprint_len
		fingerprints[key] = fprint
	return fingerprints

#fprints(texts)

def nearduplicate(fprint1, fprint2):
	#nearduplicate = False
	s = 0
	n = 0
	fprint_len = len(fprint1)
	while (n < fprint_len) and (s < 7):
		s += math.fabs(fprint1[n]-fprint2[n])
		n += 1
	if (s == 7):
		return True
	return False

def q3(txts):
	nearduplicates = []
	fingerprints = fprints(txts)
	keys = fingerprints.keys()
	i = 0
	keys_len = len(keys)
	while i < keys_len:
		#print str(i) + " out of " + str(len(keys))
		n = i + 1
		keys_i = keys[i]
		while n < keys_len:
			keys_n = keys[n]
			if (nearduplicate(fingerprints[keys_i], fingerprints[keys_n])):
				if not(([keys_i, keys_n] or [keys_n, keys_i]) in plagiarism):
					plagiarism.append([keys_i, keys_n])
			n += 1
		i += 1
	#return nearduplicates
	
q3(texts)
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