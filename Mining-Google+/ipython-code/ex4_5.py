import httplib2
import json
import apiclient.discovery
from bs4 import BeautifulSoup
from nltk import clean_html
USER_ID = '107033731246200681024' #Tim O' Reilly

API_KEY = 'AIzaSyDMJRu_ZTMkxZaYWOgaNXp4Ook1djTrEGE'

MAX_RESULTS = 2000 # Will require multiple requests
def cleanHtml(html):
	if html == "": return ""
	soup = BeautifulSoup(html)
	return soup.get_text()

service = apiclient.discovery.build('plus', 'v1',http=httplib2.Http(),developerKey=API_KEY)

activity_feed = service.activities().list(
	userId=USER_ID,
	collection='public',
	maxResults='100' # Max allowed per request
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
