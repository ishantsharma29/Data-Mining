import nltk
import json

nltk.download('stopwords')

USER_ID = '107033731246200681024' #Tim O' Reilly

dfile = USER_ID + '.json'
dat = json.loads(open(dfile).read())

all_content = [token for activity in dat for token in activity['object']['content'
                  ].split()]

print 
print "All_content  -> " , all_content
# Approximate bytes of text
print "Bytes of text -> ",len(all_content)

tokens= all_content
text = nltk.Text(tokens)
print " Text -> ", text 

# Examples of the appearance of the word "open"
print "Examples of the appearance of the word essay -> ",text.concordance("essay")
# Frequent collocations in the text (usually meaningful phrases)
print "Frequent Collocations in text -> " ,text.collocations()
# Frequency analysis for words of interest


fdist = text.vocab()
print "Fdist is - " , fdist
print " essay ", fdist["essay"]
print
print "Source ", fdist["source"]
print 
fdist["web"]
fdist["2.0"]
# Number of words in the text
print "Number of words in the text ", len(tokens)
# Number of unique words in the text
print "Number of unique words in the text", len(fdist.keys())


# Common words that aren't stopwords
print "Not stop words " ,
print [w for w in fdist.keys()[:100] \
	if w.lower() not in nltk.corpus.stopwords.words('english')]


# Long words that aren't URLs
print 
print
print "Not URL's " ,
print [w for w in fdist.keys() if len(w) > 15 and not w.startswith("http")]



print 
print 
# Number of URLs
print "Number of URLs"
print len([w for w in fdist.keys() if w.startswith("http")])
# Enumerate the frequency distribution



print "Enumerate the frequency distribution",
print
for rank, word in enumerate(fdist):
	print rank, word, fdist[word]
