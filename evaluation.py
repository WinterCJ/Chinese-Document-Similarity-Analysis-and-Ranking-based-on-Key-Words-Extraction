# -*- coding:utf-8 -*-

import logging
from gensim import corpora, models, similarities

datapath = "evaluation.txt"
scorepath = "evaluationScore.txt"
keypath = "docKeyWords.txt"
oursimpath = "Similarity.txt"
topN = 10

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
	for i in range(len(cosineWeight)):
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
	
txtName, keysList = readKeyword()
writeList = []
cosineWeight = {}
for i in range(topN):
	cosineWeight[i] = 0.0
for i in range(len(txtName)):
	topList, cosineAvg = gensimCos(datapath, txtName, txtName[i], keysList[i], topN)
	writeList.append(topList)
	for i in range(topN):
		cosineWeight[i] += cosineAvg[i]

fileout = open(datapath,"w+")
for i in range(len(writeList)):
	fileout.write(writeList[i])
fileout.close()

calculateScore(datapath,oursimpath,scorepath,cosineWeight)
