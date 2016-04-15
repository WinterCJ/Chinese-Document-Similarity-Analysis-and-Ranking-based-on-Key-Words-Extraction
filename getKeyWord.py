# -*- coding:utf-8 -*-
import jieba;
import os;
import math;
import sys;
reload(sys)
sys.setdefaultencoding( "utf-8" )

idfFile = open("IDFfile.txt","rb");

line = idfFile.readline();
fileSum = int(line.strip());
line = idfFile.readline();
idfDic = {};
while line!="":
    line = line.strip();
    ls = line.split("  ");
    idfDic[ls[0]] = int(ls[1]);
    line = idfFile.readline();
idfFile.close();

stopFile = open("stopwords.txt","rb");
stopWords = {};
stopline = stopFile.readline();
while stopline!="":
    stopline = stopline.strip();
    if not stopWords.has_key(stopline):
        stopWords[stopline] = 1;
    stopline = stopFile.readline();
stopFile.close();

path = "./Reduced";

mainDoc = os.listdir(path);

outfileName = "docKeyWords.txt";
ofile = open(outfileName,"wb");


for p in mainDoc:# Each subfile
    if p[0]=='.':
        continue;
    newsSub = os.listdir(path+"/"+p);
    for n in newsSub:# Each file
        if n[0]=='.':
            continue;
        infile = open(path+"/"+p+"/"+n, 'rb');
        wordC = {};
        wordSum = 0;
        line = infile.readline();
        while line!="":
            line = line.strip();
            ls = jieba.cut(line);
            for w in ls:
                w =w.strip();
                #Apply stop words here latter
                if w=="":
                    continue;
                if stopWords.has_key(str(w)):
                    continue;
                wordSum += 1;
                if wordC.has_key(w):
                    wordC[w] += 1;
                else:
                    wordC[w] = 1;
            line = infile.readline();
        tfIdf = {};
        for w in wordC:
            t=0;
            if idfDic.has_key(str(w)):
                t = idfDic[str(w)];
            tfIdf[w] = float(wordC[w])/float(wordSum)*float(math.log(float(fileSum)/float(t+1)));
        tfIdf = sorted(tfIdf.items(), key=lambda d:d[1], reverse=True);
        if len(tfIdf)==0:
            continue;
        ofile.write(infile.name);
        ic = 0;
        for t in tfIdf:
            if ic>=16:
                break;
            ic += 1;
            ofile.write(" "+t[0]);
        ofile.write("\n");
        infile.close();

ofile.close();

################################



'''fileN = "839.txt";
infi = open(fileN, "rb");
wordC = {};
wordSum = 0;
line = infi.readline();

while line!="":
    line = line.strip();
    ls = jieba.cut(line);
    for w in ls:
        #Apply stop words here latter
        w =w.strip();
        if w=="":
            continue;
        wordSum += 1;
        if wordC.has_key(w):
            wordC[w] += 1;
        else:
            wordC[w] = 1;
    line = infi.readline();

tfIdf = {};
print "sum", fileSum
print "了", idfDic["了"]
print "加剂", idfDic["加剂"]

print idfDic.has_key("加剂")
wordc2 = sorted(wordC.items(), key=lambda d:d[1], reverse=True);
for t in wordc2:
    print t[0], t[1]
for w in wordC:
    t=0;
    print str(w), wordC[w],wordC.has_key(w)
    print idfDic.has_key(str(w))
    if idfDic.has_key(str(w)):

        t = idfDic[str(w)];
    tfIdf[w] = float(wordC[w])/float(wordSum)*float(math.log(float(fileSum)/float(t+1)));

tfIdf = sorted(tfIdf.items(), key=lambda d:d[1], reverse=True);
for t in tfIdf:
    print t[0], t[1]'''

