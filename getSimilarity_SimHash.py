# -*- coding:utf-8 -*-

import sys
import math
import hashlib

IDFpath = "IDFfile.txt"
keypath = "Demo_Corpus_KeyWords.txt"

def getWeight(IDFpath):
	wdict = {}
	wordlist = []
	filein = open(IDFpath, "rb")
	readfile = filein.readlines()
	filein.close()
	for line in readfile:
		line = line.strip('\n')
		wordlist = line.split()
		if( len(wordlist) == 1):
			idftotal = wordlist[0]
		if( len(wordlist) == 2):
			wdict[wordlist[0]] = wordlist[1]
	return wdict,idftotal

def readKeyword():
	txtName = []
	keysList = {}
	filein = open(keypath, "rb")
	readfile = filein.readlines()
	filein.close()
	for line in readfile:
		start = 0
		while(1):
			if line[start] == ' ':
				break
			start += 1
		line = line.strip('\n')
		wordlist = line.split()
		txtName.append(wordlist[0])
		keysList[wordlist[0]] = line[start+1 :]
	return txtName, keysList

def simhash(idftotal, wdict, keyspath, txtName, keysList):
	wordList = keysList[txtName].split()
	codeLen = 128
	codeSum = []
	for i in range(codeLen):
		codeSum.append('0')
	for i in range(len(wordList)):
		hex16 = hashlib.md5(wordList[i]).hexdigest()
		bin2 = bin(long(hex16,16))
		eachCode = str(bin2[2:])
		comCode = []
		if wordList[i] in wdict:
			weight = math.log(float(idftotal) / float(int(wdict[wordList[i]]) + 1))
		if (len(eachCode) < codeLen):
			diff = codeLen - len(eachCode)
			for j in range(diff):
				comCode.append('0')
			for j in range(len(eachCode)):
				comCode.append(eachCode[j])
		else:
			comCode = eachCode
		for j in range(len(comCode)):
			temp = 0.0
			if (comCode[j] == '0'):
				temp = weight * (-1.0)
			if (comCode[j] == '1'):
				temp = weight * 1.0
			tempint = float(codeSum[j])
			codeSum[j] = str(tempint + temp)
	codeBin = []	
	for i in codeSum:
		if(float(i) > 0):
			codeBin.append("1")
		else:
			codeBin.append("0")
	Binsum = 0
	for i in range(len(codeBin)):
		Binsum += long(codeBin[codeLen-i-1]) * pow(2,i)
	return Binsum
	
def hammingDistance(simhashcode):
	fileout = open("Similarity_SimHash.txt","w+")
	for i in simhashcode:
		hmdistance = {}
		fileout.write(i + ' ')
		for j in simhashcode:
			count = 0
			if (i == j):
				continue
			else:
				temp = bin(int(simhashcode[i]) ^ int(simhashcode[j]))
				temp = temp[2:]				
				for k in range(len(temp)):
					if (temp[k] == '1'):
						count += 1
			hmdistance[j] = count
		hmdistance = sorted(hmdistance.iteritems(), key=lambda d:d[1], reverse = False)
		for i in range(10):
			if( i == 9 ):
				fileout.write(hmdistance[i][0] + '\n')
			else:
				fileout.write(hmdistance[i][0] + ' ')
	fileout.close()


wdict, idftotal = getWeight(IDFpath)
txtName, keysList = readKeyword()

simhashcode = {}
for i in range(len(txtName)):
	Binsum = simhash(idftotal, wdict, keypath, txtName[i], keysList)
	simhashcode[txtName[i]] = Binsum

hammingDistance(simhashcode)

print "------ SimHash Similarity Finished! See output in: \"Similarity_SimHash.txt\""
