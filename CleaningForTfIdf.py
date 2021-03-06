#!/usr/bin/python

#Import 
import os
import sys
import nltk
import string
import pandas as pd
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer


#Do not stem the words in the abstracts.  Given that the words are scientific in nature, they can have different meanings depending on their ending.  For example, crossing and cross do not refer to the same concept.

#We'll remove all of the latex and the punctuation from the abstracts.  Also, we'll remove the stop words and any of the strange remenants that get left over from removing non-letter (latex) symbols.

path = '/Users/daniel/Desktop/ArxivProject/TfIdfPredict'
Abstract_folder = u'CleanedAbstractsNoLatex'
Abstracts_folder_noLatex = path + '/' + Abstract_folder
try:
	test_or_not = sys.argv[1]
	if test_or_not:
		#Use this file name for the test database
		metadatafile = 'Just_a_test.csv'
		print("This is a test")
except IndexError:
	#Use this file name for the full dataset.
	metadatafile = 'All_Metadata.csv'

AbstractPath = path+'/'+metadatafile
#Read the metadata file
metadata = pd.read_csv(AbstractPath)

#ArxivIds:
ids = metadata['Arxiv-id'].tolist()

Abstracts = metadata['Abstract'].tolist()

def RemoveLatex(Abstract):

	#This function will remove all of the non-letter words from the abstracts.
	#Do this with regular expressions.
	#Sometimes, some junk gets left behind, like single letters or string of
	#letters that were at one point math, remove as much as possible.

	#Remove non-letters:
	Abstract_removeNonlets = re.sub("[^a-zA-Z]"," ",Abstract)

	#Convert to string with white spaces in the right places
	Abstract_lets_string = " ".join(Abstract_removeNonlets.split()).lower()
	Abstract_lets = re.sub("[^\w]", " ",  Abstract_lets_string).split()
	
	#For all the elements in the list Abstracts_lets, remove as many of the odd left over
	#pieces as possible
	#We made need to modify this a bit if we find that it's too restrictive.
	#Accuracy would be better if I built in a list of common scientific abreviations...
	
	CleanOdd = []
	for word in Abstract_lets:
		if len(word) > 2:
			CleanOdd.append(word)
	#Now turn the result back into a string
	AbsRemoveLatex = " ".join(CleanOdd)

	return AbsRemoveLatex


#Go through the abstracts and clean them using the RemoveLatex function:

Clean_Abstracts = []
i = 0
for Ab in Abstracts:
	id = ids[i]
	print("Processing %s" % i)
	Cleaned = RemoveLatex(Ab)
	Clean_Abstracts.append(Cleaned)
	i += 1

#Get the cleaned abstracts and their id numbers into files in our directory.
#This also removes any duplicates that could have arisen due to update to
#The arxiv during the scrapping processes.
Ordered_Abs_dict = {}
for i in range(0,len(Clean_Abstracts)):
	id = ids[i]
	if id not in Ordered_Abs_dict:
		Ordered_Abs_dict[id] = Clean_Abstracts[i]

#Save the cleaned abstracts as txt files, labeled by id to serve as the data set for NLP.

if not os.path.exists(Abstracts_folder_noLatex):
	os.makedirs(Abstracts_folder_noLatex)


for id, Ab in Ordered_Abs_dict.items():
	Ab_id = str(id)
	if Ab_id[:2] == '16' or Ab_id[:2] == '15':
		Ab_text_filename = os.path.join(Abstracts_folder_noLatex, '%.5f.txt') % (float(Ab_id))
		print("Writing %s" % Ab_text_filename)
		open(Ab_text_filename, 'wb').write(Ab.encode('utf-8','ignore'))
	else:
		try:
			Ab_text_filename = os.path.join(Abstracts_folder_noLatex,'%09.4f.txt') % (float(Ab_id))
			print("Writing %s" % Ab_text_filename)
			open(Ab_text_filename, 'wb').write(Ab.encode('utf-8', 'ignore'))
		except ValueError:
			Ab_id = Ab_id[:-1]
			Ab_text_filename = os.path.join(Abstracts_folder_noLatex,'%09.4f.txt') % (float(Ab_id))
			print("Writing %s" % Ab_text_filename)
			open(Ab_text_filename, 'wb').write(Ab.encode('utf-8', 'ignore'))





