# -*- coding:utf-8 -*-

import sys

print "------ Calculating Corpus TF-IDF Values\n------ Corpus Size: about 17,000 txt Files\n------ Estimated Time: 2min 14s"
execfile("getIDF.py")

print "\n------ Calculating Demo Corpus Top-16 KeyWords\n------ Demo Corpus Size: about 500 txt Files\n------ Estimated Time: 4s"
execfile("getKeyWord.py")

print "\n------ Similarity Program is Running\n------ Estimated Time: 2s"
execfile("getSimilarity.py")

print "\n------ SimHash Similarity Program is Running\n------ Estimated Time: 4s"
execfile("getSimilarity_SimHash.py")
