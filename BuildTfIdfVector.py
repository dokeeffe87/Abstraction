#!/usr/bin/python

#This program will build the Tf-Idf (Term frequency - Inverse document frequency) vectors for the abstracts with Latex removed.

#Import modules:

import nltk
import string
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA
import collections
import pickle
#nltk.download()

path = '/Users/daniel/Desktop/ArxivProject/TfIdfPredict/CleanedAbstractsNoLatex/'

#token_dict = {}
token_dict = collections.OrderedDict()

#Do not perform stemming on the cleaned abstracts. Scientific terms can have different meanings depending on their endings (i.e. crossing and cross), so stemming the words in the abstracts will cause context loss.

def tokenize(Abstract):
	#This function will tokenize the abstracts using NLTK
	tokens = nltk.word_tokenize(Abstract)
	return tokens

#Build up the token dictonary using the txt files containing the abstracts
for subdir, dirs, files in os.walk(path):
	for file in files:
		file_path = subdir + os.path.sep + file
		Abstract = open(file_path,'r')
		Ab = Abstract.read()
		token_dict[file] = Ab

tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())

#Test string:
Teststr = 'study the effects produced brane instantons the holomorphic quantities brane gauge theory orbifold singularity these effects are not limited reproducing the well known contributions the gauge theory instantons but also generate extra terms the superpotential the prepotential these brane instantons there are some neutral fermionic zero modes addition the ones expected from broken supertranslations they are crucial correctly reproducing effects which are dual gauge theory instantons but they may make some other interesting contributions vanish analyze how orientifold projections can remove these zero modes and thus allow for new superpotential terms these terms contribute the dynamics the effective gauge theory for instance the stabilization runaway directions'

testVectorizerArray = tfidf.transform([Teststr]).toarray()
trainVectorizerArray = tfs.toarray()

def TestCosineSim(testVectorizerArray, trainVectorizerArray, files):

	#This function tests the cosine similarity between test documents and the training set.
	#It's a bit slow, but it does the job.
	#If all works well, it should return the same document as passed in
	#Since this document can be the only one with a cosine similarity of 1 if we've
	#built the classifier right.
	i=0
	cx = lambda a, b : round(np.inner(a, b)/(LA.norm(a)*LA.norm(b)), 3)
	ans = []
	for vector in trainVectorizerArray:
		for testV in testVectorizerArray:
			cosine = cx(vector,testV)
			if cosine == 1:
				ans.append(i)
			else:
				i+=1
	File_ind = int(ans[0])
	Test_filename = files[File_ind]
	#print(Test_filename)
	return Test_filename

def SaveTheData(files):

	#This should save the dictonary built out of the abstracts, the tf-idf vectors for
	#each abstract and the order of the files which corresponds to the id of the tf-idf
	#vectors (i.e. the id of the associated document).

	#First get the list of file names in the order they appear in the trained vectors
	#This is contained in the files list.
	Article_id_inOrder = []
	for file in files:
		Article_id_inOrder.append(file)
	f = open('ArticleOrder.txt','wb')
	for id in Article_id_inOrder:
		f.write("%s" % id)


def SaveTheData(files):

    #This should save the dictonary built out of the abstracts, the tf-idf vectors for
    #each abstract and the order of the files which corresponds to the id of the tf-idf
    #vectors (i.e. the id of the associated document).

    #First get the list of file names in the order they appear in the trained vectors
    #This is contained in the files list.
    Article_id_inOrder = []
    for file in files:
        Article_id_inOrder.append(file)
    f = open('ArticleOrder.txt','wb')
    for id in Article_id_inOrder:
        towrite = id+'\n'
        f.write(bytes(towrite,'utf-8'))

def SaveDictonary(vocab):
    
    #This function saves the word dictonary built out of the abstracts so that it doesn't
    #have to be rebuilt each runtime.
    pickle.dump(vocab,open("feature.pkl","wb"))


def SaveVectors(vecs):
    
    #This function saves the pre-built tf-idf vectors built out of the abstracts.
    #Use this in conjunction with the list of filenames and the saved vocabulary
    #To reload the model and make recommendations on new, unseen, documents.
    from sklearn.externals import joblib
    joblib.dump(vecs, 'tfidf.pkl')

def SaveVectorizer(tfidf):
	#This function saves the vectorizer input, including the tfidf.idf_ vector
	#Which contains the idf weights needed to properly vectorize future documents.
	#Without it, new documents will only get approximately accurate vector representations
	#Upon reloading the model.
	from sklearn.externals import joblib
	joblib.dump(tfidf, 'Vectorizer.pkl')


#Use the test string to make sure this is working:
result = TestCosineSim(testVectorizerArray, trainVectorizerArray, files)
if result == '0704.0262.txt':
	print(result)
	print("Test successful!")

	#Save the model for reloading later:
	SaveTheData(files)
	SaveDictonary(tfidf.vocabulary_)
	SaveVectors(tfs)
	SaveVectorizer(tfidf)

