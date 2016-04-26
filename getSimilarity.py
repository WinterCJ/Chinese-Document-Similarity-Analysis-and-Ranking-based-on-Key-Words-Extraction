# -*- coding:utf-8 -*-
import os;
import math;
import sys;
reload(sys)
sys.setdefaultencoding( "utf-8" )
import hashlib

infile = open("docKeyWordst.txt","rb");

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

weightF = open("IDFfile.txt",'rb');
line = weightF.readline();
fileSum = int(line.strip());
line = weightF.readline();
idfDic = {};
while line!="":
    line = line.strip();
    ls = line.split("  ");
    idfDic[ls[0]] = int(ls[1]);
    line = weightF.readline();
weightF.close();


for t in totalDic:
    h = [0]*128;
    for w in totalDic[t]:
        tt=0;
        if idfDic.has_key(str(w)):
            tt = idfDic[str(w)];
        dt = math.log(float(fileSum)/float(tt+1))*100
        print dt
        #m = hashlib.md5(str(w)).hexdigest();
        #num = long(m,16);
        num = hash(str(w));
        x=1;
        for i in range(0,128):
            tempi = num&x;
            if tempi==0:
                h[64-i-1] = h[64-i-1]-dt;
            else:
                h[64-i-1] = h[64-i-1]+dt;
            x = x*2;
    hc = 0;
    for i in range(0,128):
        hc = hc*2;
        if h[i]>0:
            #print 1
            hc+=1;
        '''elif h[i]<0:
            print -1
        else:
            print 0'''
        totalDic[t] = hc;


totalL = totalDic.items();

outfile = open("Similarity.txt","wb");

for t in range (0,len(totalL)):
    fn = totalL[t][0];
    fhc = totalL[t][1];
    topThree = {};
    for i in totalL[0:]:
        guestFile = i[0];
        guestHc = i[1];
        humD = fhc^guestHc;
        count = 0;
        x = 1;
        for j in range(0,128):
            if humD&x!=0:
                count += 1;
            x = x*2;
        topThree[guestFile] = count;
        topThree = dict( (sorted(topThree.items(), key=lambda d:d[1], reverse=False))[:20] );
    '''for i in totalL[t+1:]:
        guestFile = i[0];
        guestHc = i[1];
        humD = fhc^guestHc;
        count = 0;
        x = 1;
        for j in range(0,64):
            if humD&x!=0:
                count += 1;
            x = x<<1;
        topThree[guestFile] = count;
        topThree = dict( (sorted(topThree.items(), key=lambda d:d[1], reverse=False))[:20] );'''

    outfile.write(fn);
    print fn
    topThree = (sorted(topThree.items(), key=lambda d:d[1], reverse=False));
    for t in topThree:
        outfile.write(" "+t[0]);
        print "TOPs:",t[0],t[1]
    outfile.write("\n");

####################################


'''totalL = totalDic.items();

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
        topThree = dict( (sorted(topThree.items(), key=lambda d:d[1], reverse=True))[:3] );
    for i in totalL[t+1: ]:
        guestFile = i[0];
        guestDic = i[1];
        count = 0;
        for k in fkd:
            if guestDic.has_key(k):
                count += 1;
        topThree[guestFile] = count;
        topThree = dict( (sorted(topThree.items(), key=lambda d:d[1], reverse=True))[:3] );

    outfile.write(fn);
    topThree = (sorted(topThree.items(), key=lambda d:d[1], reverse=True));
    for t in topThree:
        outfile.write(" "+t[0]);
    outfile.write("\n");
    print fn, topThree'''
outfile.close();