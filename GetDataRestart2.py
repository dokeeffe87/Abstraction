#!/usr/bin/python

from urllib.request import urlopen
import feedparser
import csv
import pandas as pd
import re
import time

# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

#Url for collecting citation info with Arxiv-id that we will extract.
Cite_url = 'https://inspirehep.net/search?p=arXiv%3A'

# Search parameters
search_query = 'cat:hep-th' # search for hep-th as the primary category
start = 0
total_results = 50000
results_per_iteration = 100
wait_time = 5
#Initial file labeling variable
starting = start
ending = start + results_per_iteration

print('Searching arXiv for %s' % search_query)
for i in range(start,total_results,results_per_iteration):
	len_id = 0
	#print('Start for loop')
	while len_id == 0:
	
		#Use this query to grab article data by newest!
		query = 'search_query=%s&start=%i&max_results=%i&sortBy=submittedDate&sortOrder=descending' % (search_query,i,results_per_iteration)

		# Opensearch metadata such as totalResults, startIndex,
		# and itemsPerPage live in the opensearch namespase.
		# Some entry metadata lives in the arXiv namespace.
		# This is a hack to expose both of these namespaces in
		# feedparser v4.1
		feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
		feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

		# perform a GET request using the base_url and query
		#response = urllib.urlopen(base_url+query).read()
		url = urlopen(base_url+query)
		response = url.read().decode('utf-8')

		# parse the response using feedparser
		feed = feedparser.parse(response)

		# print out feed information
		print('Feed title: %s' % feed.feed.title)
		print('Feed last updated: %s' % feed.feed.updated)

		# print opensearch metadata
		print('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
		print('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
		print('startIndex for this query: %s'   % feed.feed.opensearch_startindex)

		#Now let's get all the data into a pandas dataframe.  To do this, let's create a dict for each data piece that we need and then put it all together.

		Arxiv_id_list = []
		Title_list = []
		PrimaryCat_list = []
		Author_list = []
		AuthorAffiliation_list = []
		PublishDates_list = []
		JournalRefs_list = []
		AllCats_list = []
		Abstract_list = []
		AbsPage_list = []
		CitationNum_list = []

		for entry in feed.entries:

			#Update the id list:
			Get_id = entry.id.split('/abs/')[-1]
			Arxiv_id_list.append(Get_id[:-2])

			#Update the title list:
			Title_list.append(entry.title)

			#Update primary category list:
			PrimaryCat_list.append(entry.tags[0]['term'])

			#feedparser v4.1 only grabs the first author
			author_string = entry.author

			#Update Author list:
			try:
				Author_list.append([', '.join(author.name for author in entry.authors)])
			except AttributeError:
				pass

			#Update author affiliation list:
			try:
				author_string += ' (%s)' % entry.arxiv_affiliation
				AuthorAffiliation_list.append(entry.arxiv_affiliation)
			except AttributeError:
				pass

			#Update publication date list:
			PublishDates_list.append(entry.published)

			#Update joural references list:
			try:
				journal_ref = entry.arxiv_journal_ref
			except AttributeError:
				journal_ref = 'No journal ref found'
			JournalRefs_list.append(journal_ref)

			#Update all categories list:
			AllCats_list.append([t['term'] for t in entry.tags])

			#Update Abstract list:
			Abstract_list.append(entry.summary)

			#Update abstract page list:
			for link in entry.links:
				if link.rel == 'alternate':
					#print('abs page link: %s' % link.href)
					AbsPage_list.append(link.href)



			#Using the list of Arxiv-id's, access inspire-hep database and extract the citation numbers per paper.  Since the id's are stored in order, the citations will also be in order by paper.
		for id in Arxiv_id_list:
			url = urlopen(Cite_url+str(id))
			response = str(url.read())
			match = re.search(r'(Cited by)+\s+(\d+)',response)
			if match:
				CitationNum_list.append(match.group(2))
			else:
				CitationNum_list.append(0)
			#print(len(Arxiv_id_list))
			
		len_id = len(Arxiv_id_list)
		print(len_id)
		if len_id == 0:
			print('Failed to find data. Restarting in %i secoond' % wait_time)
			time.sleep(wait_time)
		elif len_id > 0:
			print('Got the data!')

	#Now lets get all of this data into a pandas data frame for future convenience.
	
	metadata_dict = {'Arxiv-id' : Arxiv_id_list, 'Title' : Title_list, 'PrimaryCat' : PrimaryCat_list, 'Authors' : Author_list, 'Affiliation' : AuthorAffiliation_list, 'CitationNum' : CitationNum_list, 'PublishDates' : PublishDates_list, 'JournalRefs' : JournalRefs_list, 'AllCats' : AllCats_list, 'Abstract' : Abstract_list, 'AbstractPage' : AbsPage_list}

	df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in metadata_dict.items() ]))

	#Print this data to a csv file for later.
	filename = 'Metadata_%i_to_%i.csv' % (starting, ending-1)
	df.to_csv(filename)

	#Increment labeling variable
	starting = starting + results_per_iteration
	ending = ending + results_per_iteration

	#Let the server sleep a bit before we call it again!
	print('Sleeping for %i seconds' % wait_time)
	time.sleep(wait_time)
