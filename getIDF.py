# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import jieba
import sys
import os

'''file = open("839.txt","rb");'''


'''l = file.readline();
while l!="":
    ll = jieba.cut(l);
    for lll in ll:
        outfile.write(lll)
    l = file.readline();
dic = {'a':31, 'bc':5, 'c':3, 'asd':4, 'aa':74, 'd':0}
dict= sorted(dic.iteritems(), key=lambda d:d[1], reverse = True)
for d in dict:
    outfile.write(d[0]+" "+str(d[1])+"\n")


file.close();
exit()'''

stopFile = open("stopwords.txt","rb");
stopWords = {};
stopline = stopFile.readline();
while stopline!="":
    stopline = stopline.strip();
    if not stopWords.has_key(stopline):
        stopWords[stopline] = 1;
    stopline = stopFile.readline();
stopFile.close();



outfile = open("IDFfile.txt","wb");

path = "./Reduced";

mainDoc = os.listdir(path);

totalDic = {};
fileSum = 0;

for p in mainDoc:# Each subfile
    if p[0]=='.':
        continue;
    newsSub = os.listdir(path+"/"+p);
    for n in newsSub:# Each file
        if n[0]=='.':
            continue;
        #print n
        fileSum += 1;
        subDic = {};
        infile = open(path+"/"+p+"/"+n, 'rb');
        line = infile.readline();
        while line!="":
            j = jieba.cut(line);
            for w in j:
                w = w.strip();
                if w!="":
                    if stopWords.has_key(str(w)):
                        print str(w), w
                        continue;
                    if not subDic.has_key(w):
                        subDic[w] = 1;
            line = infile.readline();
        for s in subDic:
            if totalDic.has_key(s):
                totalDic[s] += 1;
            else:
                totalDic[s] = 1;
        infile.close();

outfile = open("IDFfile.txt","wb");
outfile.write(str(fileSum));

totalDic = sorted(totalDic.iteritems(), key=lambda d:d[1], reverse=True);

for t in totalDic:
    outfile.write("\n");
    outfile.write(t[0]+"  "+str(t[1]))
#print totalDic

outfile.close();

print "Finished!"