# -*- coding:utf-8 -*-
import os;
import sys;
reload(sys)
sys.setdefaultencoding( "utf-8" )

infile = open("Demo_Corpus_KeyWords.txt","rb");

line = infile.readline().strip();
totalDic = {};
while line!="":
    ls = line.split(" ");
    fname = ls[0];
    kd = {};
    for k in ls[1:]:
        kd[k] = 1;
    totalDic[fname] = kd;
    line = infile.readline().strip();

infile.close();

totalL = totalDic.items();

outfile = open("Similarity.txt","wb");

for t in range(0,len(totalL)):
    fn = totalL[t][0];
    fkd = totalL[t][1];
    topThree = {};
    for i in totalL[0:t]:
        guestFile = i[0];
        guestDic = i[1];
        count = 0;
        for k in fkd:
            if guestDic.has_key(k):
                count += 1;
        topThree[guestFile] = count;
        topThree = dict( (sorted(topThree.items(), key=lambda d:d[1], reverse=True))[:10] );
    for i in totalL[t+1: ]:
        guestFile = i[0];
        guestDic = i[1];
        count = 0;
        for k in fkd:
            if guestDic.has_key(k):
                count += 1;
        topThree[guestFile] = count;
        topThree = dict( (sorted(topThree.items(), key=lambda d:d[1], reverse=True))[:10] );

    outfile.write(fn);
    topThree = (sorted(topThree.items(), key=lambda d:d[1], reverse=True));
    for t in topThree:
        outfile.write(" "+t[0]);
    outfile.write("\n");

outfile.close();

print "Finished!"
