# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import jieba
import os

def is_num_by_execpt(num):
    try:
        float(num);
        return True;
    except ValueError:
        return False;


stopFile = open("stopwords.txt","rb");
stopWords = {};
stopline = stopFile.readline();
while stopline!="":
    stopline = stopline.strip();
    if not stopWords.has_key(stopline):
        stopWords[stopline] = 1;
    stopline = stopFile.readline();
stopFile.close();

outfile = open("filesContent.txt", "wb");

path = "./corpus_reduced"

mainDoc = os.listdir(path);

for p in mainDoc:
    if p[0]=='.':
        continue;
    newsSub = os.listdir(path+"/"+p);
    for n in newsSub:
        if n[0]=='.':
            continue;
        infile = open(path+"/"+p+"/"+n, 'rb');
        line = infile.readline();
        outfile.write(p+"/"+n)
        while line!="":
            j = jieba.cut(line);
            for w in j:
                w = w.strip();
                if w!="":
                    if stopWords.has_key(str(w)):
                        continue;
                    if w=='\00':
                        continue;
                    if is_num_by_execpt(str(w)):
                        continue;
                    outfile.write(" "+str(w))
            line = infile.readline();
        outfile.write("\n");
        infile.close();

outfile.close();