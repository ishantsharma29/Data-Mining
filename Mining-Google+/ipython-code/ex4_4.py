
import httplib2
from bs4 import BeautifulSoup
import json
import apiclient.discovery
import csv

USER_ID = '114166456257006785876' # Raunak 

# XXX: Re-enter your API_KEY from
# if not currently set
  API_KEY = 'AIzaSyDMJRu_ZTMkxZaYWOgaNXp4Ook1djTrEGE'

service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(),developerKey=API_KEY)
activity_feed = service.activities().list(
	userId=USER_ID,
	collection='public',
	maxResults='100' # Max allowed per API
).execute()
print json.dumps(activity_feed, indent=1)



#from nltk import clean_html
#from BeautifulSoup import BeautifulStoneSoup
# clean_html removes tags and
# BeautifulStoneSoup converts HTML entities
def cleanHtml(html):
	if html == "": return ""
	soup = BeautifulSoup(html)
	print soup.get_text()

print activity_feed['items'][0]['object']['content']
print
print cleanHtml(activity_feed['items'][0]['object']['content'])



