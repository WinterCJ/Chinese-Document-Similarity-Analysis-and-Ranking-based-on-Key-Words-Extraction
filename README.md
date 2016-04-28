## Chinese Document Similarity Analysis and Ranking <br> based on Key Words Extraction

###Corpus:
**./corpus**: 　　　　　17,910 txt Chinese News Files From [Sogou Lab Data](http://www.sogou.com/labs/dl/c.html) <br>
**./corpus/reduced**: 　about 500 txt Files for Demo Test <br>

<hr>

###Python Files and Output:
**./getIDF.py**: Word Segmentation and Training Word TF-IDF (except Stopword) from Corpus <br>
　　　　　*See output in "IDFfile.txt"* <br>
**./getKeyWord.py**: Calculate the Top-16 KeyWords of each Demo Data txt Files <br>
　　　　　　　　*See output in "Demo_Corpus_KeyWords.txt"* <br>
**./getSimilarity.py**: Calculate Demo Corpus Top-10 Similarity by our Algorithm <br>
　　　　　　　　*See output in "Similarity.txt"* <br>
**./getSimilarity_SimHash.py**: Calculate Demo Corpus Top-10 Similarity by our Simhash Algorithm <br>
　　　　　　　　　　　　　*See output in "Similarity_SimHash.txt"* <br>

<hr>

###Demo and Evaluation:
**./demo.py**: *> python demo.py* -- Auto run the above 4 py files, and you can see 2 output txt files: <br>
　　　　　One is ***Similarity.txt***, the Top-10 Similarity List by our Algorithm <br>
　　　　　Another is ***Similarity_SimHash.txt***, the Top-10 Similarity List by our SimHash Algorithm <br>
**./evaluation.py**: *> python evaluation.py* -- The Program will ***ask you to input***:  <br>
　　　　　　***1*** will evaluate ***Similarity.txt***, ***2*** will evaluate ***Similarity_SimHash.txt*** <br>
　　　　　　The Evaluation Standard is Gensim Cosine Similarity Function <br>
　　　　　　You can see two Evaluation Score output txt:  ***Evaluation_Score.txt*** and ***Evaluation_Score_SimHash.txt*** <br>

<hr>

###Gensim:
Our Evaluation based on [Gensim](https://radimrehurek.com/gensim/), If you want to run the *evaluation.py*, You should install it. <br>
1. **Install [easy_install](https://pypi.python.org/pypi/setuptools#installation-instructions)** <br>
2. **Install SciPy & NumPy** <br>
　　　　*> easy_install numpy* <br>
　　　　*> easy_install scipy* <br>
3. **Install Gensim** <br>
　　　　*> easy_install -U gensim* <br>
