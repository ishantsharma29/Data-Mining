import httplib2
import json
import apiclient.discovery
from bs4 import BeautifulSoup
from nltk import clean_html

USER_ID = '107033731246200681024'
# XXX: Re-enter your API_KEY from
# if not currently set
API_KEY = 'AIzaSyDMJRu_ZTMkxZaYWOgaNXp4Ook1djTrEGE'

MAX_RESULTS = 200 # Will require multiple requests
def cleanHtml(html):
	if html == "": return ""
	soup = BeautifulSoup(html)
	return soup.get_text()

service = apiclient.discovery.build('plus', 'v1',http=httplib2.Http(),developerKey=API_KEY)

activity_feed = service.activities().list(
	userId=USER_ID,
	collection='public',
	maxResults='10' # Max allowed per request
)
activity_results = []

time = 0
while activity_feed != None and len(activity_results) < MAX_RESULTS:
 time = time+1
 print time
 if time == 5 :
  break	
 activities = activity_feed.execute()

 if 'items' in activities:
	for activity in activities['items']:
		if activity['object']['objectType'] == 'note' and \
		activity['object']['content'] != '':
			activity['title'] = cleanHtml(activity['title'])
			activity['object']['content'] = cleanHtml(activity['object']['content'])
			activity_results += [activity]

 print "hola--"

# list_next requires the previous request and response objects
 activity_feed = service.activities().list_next(activity_feed, activities)

# Write the output to a file for convenience
f = open(os.path.join(USER_ID + '.json'), 'w')
f.write(json.dumps(activity_results, indent=1))
f.close()
print str(len(activity_results)), "activities written to", f.name


print "hola---"

# Explore some of NLTK's functionality by exploring the data.
# Here are some suggestions for an interactive interpreter session.


import nltk
# Download ancillary nltk packages if not already installed
nltk.download('stopwords')
all_content = " ".join([ a['object']['content'] for a in activity_results ])
# Approximate bytes of text
print len(all_content)
tokens = all_content.split()
text = nltk.Text(tokens)
# Examples of the appearance of the word "open"
text.concordance("open")
# Frequent collocations in the text (usually meaningful phrases)
text.collocations()
# Frequency analysis for words of interest
fdist = text.vocab()
fdist["open"]
fdist["source"]
fdist["web"]
fdist["2.0"]
# Number of words in the text
len(tokens)
# Number of unique words in the text
len(fdist.keys())


print "hola4"

# Common words that aren't stopwords
[w for w in fdist.keys()[:100] \
	if w.lower() not in nltk.corpus.stopwords.words('english')]
# Long words that aren't URLs
[w for w in fdist.keys() if len(w) > 15 and not w.startswith("http")]
# Number of URLs
len([w for w in fdist.keys() if w.startswith("http")])
# Enumerate the frequency distribution
for rank, word in enumerate(fdist):
	print rank, word, fdist[word]
