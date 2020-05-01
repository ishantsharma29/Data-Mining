import json
import nltk
# Load in human language data from wherever you've saved it
import operator
from nltk.compat import iteritems

USER_ID = '107033731246200681024' #Tim O' Reilly
USER_I = 'QueryBy_Id_Output'

DATA = USER_ID + '.json'
data = json.loads(open(DATA).read())

# Number of collocations to find
N = 100

i = 0
for activity in data :
	i = i + 1
 #print activity['object']['content'].lower().split()

print i

all_tokens = [token for activity in data for token in activity['object']['content'
].lower().split()]


finder = nltk.BigramCollocationFinder.from_words(all_tokens)

finder.apply_freq_filter(2)

finder.apply_word_filter(lambda w: w in nltk.corpus.stopwords.words('english'))

bigram_score={}
for ngram,freq in iteritems(finder.ngram_fd):
	bi_freq = finder.ngram_fd[ngram]
	w1=finder.word_fd[ngram[0]]
	w2=finder.word_fd[ngram[1]]
	score = (bi_freq)/float(w1*(w1-bi_freq)+w2*(w2-bi_freq)+bi_freq)
	#print score
	bigram_score[ngram]=score


counter = 0
for (k,v) in sorted(bigram_score.items(),key=operator.itemgetter(1),reverse=True):
	if counter == 100:
		break
	#print k," ",v
	c = ' '.join(k)
	print c
	counter =  counter + 1
