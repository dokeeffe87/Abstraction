#!/usr/bin/python

import pandas as pd
import csv
import re

start = 0
starting = start
end = 50000
iter = 100
ending = start + iter
all_titles = []
all_ids = []
all_Abstracts = []
all_Affils = []
all_AbsPages = []
all_Allcats = []
all_Authors = []
all_Citations = []
all_JournRefs = []
all_PrimaryCats = []
all_PubDates = []

for i in range(start,end,100):

	filename = 'Metadata_%i_to_%i.csv' % (starting, ending-1)
	metadata = pd.read_csv(filename)
	titles = metadata['Title'].tolist()
	ids = metadata['Arxiv-id'].tolist()
	Abstracts = metadata['Abstract'].tolist()
	affiliation = metadata['Affiliation'].tolist()
	AbsPage = metadata['AbstractPage'].tolist()
	Allcates = metadata['AllCats'].tolist()
	Authors = metadata['Authors'].tolist()
	Citation = metadata['CitationNum'].tolist()
	JournRef = metadata['JournalRefs'].tolist()
	PrimaryCate = metadata['PrimaryCat'].tolist()
	PublicationDate = metadata['PublishDates'].tolist()

	for j in range(0,len(ids)):
		id = ids[j]
		if id not in all_ids:
			all_ids.append(str(ids[j]))
			all_titles.append(titles[j])
			all_Abstracts.append(Abstracts[j])
			all_Affils.append(affiliation[j])
			all_AbsPages.append(AbsPage[j])
			all_Allcats.append(Allcates[j])
			all_Authors.append(Authors[j])
			all_Citations.append(Citation[j])
			all_JournRefs.append(JournRef[j])
			all_PrimaryCats.append(PrimaryCate[j])
			all_PubDates.append(PublicationDate[j])


	#Iterate the labeling variables
	print('Done %s' % starting)
	starting = starting + 100
	ending = ending + 100


#Put all of the data from the files into one dictonary.
All_metadata_dict = {'Arxiv-id' : all_ids, 'Title' : all_titles, 'PrimaryCat' : all_PrimaryCats, 'Authors' : all_Authors, 'Affiliation' : all_Affils, 'CitationNum' : all_Citations, 'PublishDates' : all_PubDates, 'JournalRefs' : all_JournRefs, 'AllCats' : all_Allcats, 'Abstract' : all_Abstracts, 'AbstractPage' : all_AbsPages}


#Send dictonary to a pandas DataFrame
df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in All_metadata_dict.items() ]))

#Save DataFrame as a csv file for future use. This will be all of our collected data in one file!
filename = 'ALL_Metadata.csv'
#filename = 'Just_a_test.csv'
df.to_csv(filename)
