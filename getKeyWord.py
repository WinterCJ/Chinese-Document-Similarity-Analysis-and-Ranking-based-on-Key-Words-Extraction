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

td = {};#for the use of get rid of redudence

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
        #ofile.write(p+"/"+n);
        ic = 0;
        wl = "";
        for t in tfIdf:
            if ic>=16:
                break;
            ic += 1;
            wl += " "+t[0]
            #ofile.write(" "+t[0]);
        if not td.has_key(wl):
            ofile.write(p+"/"+n);
            ofile.write(wl);
            ofile.write("\n");
            td[wl] = 1;
        infile.close();

ofile.close();

################################