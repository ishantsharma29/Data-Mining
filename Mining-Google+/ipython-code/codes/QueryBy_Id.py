#This is example 4_3.py 

import httplib2
import json
import apiclient.discovery
USER_ID = '114166456257006785876' # Raunak 

API_KEY = 'AIzaSyDMJRu_ZTMkxZaYWOgaNXp4Ook1djTrEGE'

service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(),
developerKey=API_KEY)
activity_feed = service.activities().list(
	userId=USER_ID,
	collection='public',
	maxResults='100' # Max allowed per API
).execute()
print json.dumps(activity_feed, indent=1)
