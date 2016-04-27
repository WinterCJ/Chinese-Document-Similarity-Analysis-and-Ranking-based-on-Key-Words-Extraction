import re

filenameI = 'Similarity.txt'
#filenameI = 'evaluation.txt'
filenameI2 = 'docKeyWords.txt'

fin = open(filenameI,'rb')
fin2 = open(filenameI2,'rb')
readfile = fin.readlines()
readfile2 = fin2.readlines()
fin.close()
fin2.close()

nodeData = []
linkData = []
Sencond = []
Third = []
docName = []
keyWords = []
nodeDic = {}

nodeHead = '    {\"name\":'
nodeEnd = '},\n'

linkHead = '    {\"source\":'
linkMiddle = ',\"target\":'
linkEnd = '},\n'

topnHead = '    {\"name0\":\"'
topnMid1 = '\",\"name1\":\"'
topnMid2 = '\",\"name2\":\"'
topnMid3 = '\",\"name3\":\"'
topnEnd = '\"},\n'

keywordHead = '    {\"name\":\"'
keywordMid = '\",\"keys\":\"'
keywordEnd = '\"},\n'

lineNo = 0
for line in readfile:
	line=line.strip('\n')
	nameList= line.split(' ')
	nodeDic[nameList[0]] = lineNo
	nodeData.append(nameList[0])
	linkData.append(nameList[1])
	Sencond.append(nameList[2])
	Third.append(nameList[3])
	lineNo += 1

reObj = re.compile(r"\\")

lineNo = 0
for line in readfile2:
	line=line.strip('\n')
	nameList= line.split(' ')
	doc = nameList[0]
	key = ''
	i = 1
	while( i < len(nameList)):
		if(i == len(nameList) - 1):
			key += nameList[i]
		else:
			key += nameList[i] + ' '
		i += 1
	docName.append(doc)
	keyWords.append(key)
	lineNo += 1

filenameO = 'similarity.json'
#filenameO = 'similarityGensim.json'
fout = open(filenameO,'w+')

fout.write('{\n')
fout.write('  \"nodes\":[\n')

i=0
while(i<len(nodeData)):
	if(i == len(nodeData) - 1):
		fout.write(nodeHead + '\"' + nodeData[i] + '\"'	+ '}\n')
	else:
		fout.write(nodeHead + '\"' + nodeData[i] + '\"'	+ nodeEnd)
	i += 1

fout.write('  ],\n')
fout.write('  \"links\":[\n')

i=0
while(i<len(linkData)):
	source = str(i)
	if linkData[i] in nodeDic:
		target = str(nodeDic[linkData[i]])
	else:
		print 'error'

	if(i == len(linkData) - 1):
		fout.write(linkHead + source + linkMiddle + target + '}\n')
	else:
		fout.write(linkHead + source + linkMiddle + target + linkEnd)
	i += 1

fout.write('  ],\n')
fout.write('  \"topn\":[\n')

i=0
while(i<len(nodeData)):
	if(i == len(nodeData) - 1):
		fout.write(topnHead + nodeData[i] + topnMid1 + linkData[i] + topnMid2 + Sencond[i] + topnMid3 + Third[i] + '\"}\n')
	else:
		fout.write(topnHead + nodeData[i] + topnMid1 + linkData[i] + topnMid2 + Sencond[i] + topnMid3 + Third[i] + topnEnd)
	i += 1

fout.write('  ],\n')
fout.write('  \"keyword\":[\n')

i=0
while(i<len(docName)):
	if(i == len(nodeData) - 1):
		fout.write(keywordHead + docName[i] + keywordMid + keyWords[i] + '\"}\n')
	else:
		fout.write(keywordHead + docName[i] + keywordMid + keyWords[i] + keywordEnd)
	i += 1

fout.write('  ]\n')
fout.write('}')
fout.close()
