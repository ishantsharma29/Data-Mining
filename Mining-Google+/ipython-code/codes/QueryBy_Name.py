#This is example1 of the book
#Output is in ex1_output.json file

import httplib2
import json
import apiclient.discovery # pip install google-api-python-client
# XXX: Enter any person's name
Q = "Fraser Cain"

API_KEY = 'AIzaSyDMJRu_ZTMkxZaYWOgaNXp4Ook1djTrEGE'

service = apiclient.discovery.build('plus','v1', http=httplib2.Http(),developerKey=API_KEY)
people_feed = service.people().search(query=Q).execute()
print json.dumps(people_feed['items'], indent=1)

from IPython.core.display import HTML
html = []
for p in people_feed['items']:
	html += ['<p><img src="%s" /> %s: %s</p>' % \
	(p['image']['url'], p['id'], p['displayName'])]

HTML(''.join(html))
