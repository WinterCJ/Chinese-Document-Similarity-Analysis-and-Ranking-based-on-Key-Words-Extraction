# -*- coding:utf-8 -*-

import logging
import sys
from gensim import corpora, models, similarities

oursimpath = sys.argv[1]


if (oursimpath == "./Similarity.txt"):
	scorepath = "Evaluation_Score_Cosine.txt"
	datapath = "Evaluation_Similarity_List_Cosine.txt"
if (oursimpath == "./Similarity_SimHash.txt"):
	scorepath = "Evaluation_Score_SimHash.txt"
	datapath = "Evaluation_Similarity_List_SimHash.txt"
keypath = "Demo_Corpus_Duplicated.txt"
reducedpath = "Demo_Corpus.txt"
topN = 80

def reduceFile(oursimpath, reducedpath):
	wordList = []
	newline = []
	newlineName = []
	filein = open(oursimpath, "rb")
	readfile = filein.readlines()
	for line in readfile:
		line = line.strip('\n')
		word = line.split()
		wordList.append(word[0])

	filein = open(reducedpath, "rb")
	readfile = filein.readlines()
	for line in readfile:
		start = 0
		while(1):
			if line[start] == ' ':
				break
			start += 1
		for i in range(len(wordList)):
			if ( line[:start] == wordList[i] ):
				newlineName.append(wordList[i])
				newline.append(line[start+1:])
	
	fileout = open(keypath,"w+")
	for i in range(len(newline)):
		fileout.write(newlineName[i] + " " + newline[i])
	filein.close()
	fileout.close()

def readKeyword():
	txtName = []
	keysList = []
	fileNo = 0
	filein = open(keypath, "rb")
	readfile = filein.readlines()
	filein.close()
	fileout = open(datapath,"w+")
	for line in readfile:
		start = 0
		while(1):
			if line[start] == ' ':
				break
			start += 1
		txtName.append(line[:start])
		newline = line[start+1:]
		fileout.write(newline)
		keysList.append( newline.strip('\n') )		
	fileout.close()
	return txtName, keysList
		

def gensimCos( datapath, txtName, queryname, querypath, topN ):
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	class MyCorpus(object):
		def __iter__(self):
			for line in open(datapath):
				yield line.split()

	Corp = MyCorpus()
	dictionary = corpora.Dictionary(Corp)
	corpus = [dictionary.doc2bow(text) for text in Corp]

	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	vec_bow = dictionary.doc2bow(querypath.split())
	vec_tfidf = tfidf[vec_bow]

	index = similarities.MatrixSimilarity(corpus_tfidf)
	sims = index[vec_tfidf]	
	
	similarity = list(sims)
	simList = {}
	i = 0
	for item in similarity:
		simList[txtName[i]] = item
		i += 1
	simList.pop(queryname)
	simList = sorted(simList.iteritems(), key=lambda d:d[1], reverse = True)

	cosineAvg = {}
	topList = queryname + ' '
	for i in range(topN):
		if(i == topN - 1):
			topList += simList[i][0] + '\n'
			cosineAvg[i] = simList[i][1]
		else:
			topList += simList[i][0] + ' '
			cosineAvg[i] = simList[i][1]
	return topList, cosineAvg

def calculateScore(datapath, oursimpath, scorepath, cosineWeight):
	e1 = {}
	e2 = {}
	filescore = {}
	filein = open(datapath, "rb")
	readfile = filein.readlines()
	for line in readfile:
		line = line.strip('\n')
		start = 0
		while(1):
			if line[start] == ' ':
				break
			start += 1
		filename = line[:start]
		filetopn = line[start+1:]
		e1[filename] = filetopn

	filein = open(oursimpath, "rb")
	readfile = filein.readlines()
	for line in readfile:
		line = line.strip('\n')
		start = 0
		while(1):
			if line[start] == ' ':
				break
			start += 1
		filename = line[:start]
		filetopn = line[start+1:]
		e2[filename] = filetopn
	filein.close()

	e1List = []
	e2List = []
	weightSum = 0.0
	for i in range(10):
		weightSum += cosineWeight[i]
	for i in e2:		
		if i in e1:
			e1List = e1[i].split()
			e2List = e2[i].split()
			e1ListDic = {}

			for j in range(len(e1List)):
				#e1ListDic[e1List[j]]  = 100 - (j * 10) + ((j-1) * 5)
				#e1ListDic[e1List[j]]  = 10 - j
				e1ListDic[e1List[j]] = cosineWeight[j]

			score = 0.0
			for j in e2List:
				if j in e1ListDic:
					score += e1ListDic[j]
			if(score == 0.0):
				filescore[i] = 0.0
			if(score > weightSum):
				filescore[i] = 1.0
			else:
				#filescore[i] = float(score)/725.0
				#filescore[i] = float(score)/55.0
				filescore[i] = score/weightSum
	scoresum = 0.0
	for i in filescore:
		scoresum += filescore[i]
	scoreavg = scoresum/float(len(filescore))	
	filescore = sorted(filescore.iteritems(), key=lambda d:d[1], reverse = True)

	fileout = open(scorepath,"w+")
	fileout.write("Evaluation Documents Total Sum: " + str(len(filescore)) + '\n')
	fileout.write("Averange Score: " + str(scoreavg) + '\n')
	fileout.write("Documents Score Ranks: " + '\n')
	for i in range(len(filescore)):
		fileout.write( str(filescore[i][0]) + ' ' + str(filescore[i][1]) + '\n')
	fileout.close()

reduceFile(oursimpath, reducedpath)

txtName, keysList = readKeyword()
writeList = []
cosineWeight = {}
for i in range(topN):
	cosineWeight[i] = 0.0

for i in range(len(txtName)):
	topList, cosineAvg = gensimCos(datapath, txtName, txtName[i], keysList[i], topN)
	writeList.append(topList)
	for j in range(topN):
		cosineWeight[j] += cosineAvg[j]
	print"--------------------------------------------------------\n  Calculating No."+str(i+1)+" Document Cosine Similarity......\n--------------------------------------------------------"

fileout = open(datapath,"w+")
for i in range(len(writeList)):
	fileout.write(writeList[i])
fileout.close()

calculateScore(datapath,oursimpath,scorepath,cosineWeight)
print "Evaluation Finished!"
