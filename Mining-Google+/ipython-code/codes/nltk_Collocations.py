import json
import nltk

from nltk.compat import iteritems

# Load in human language data from wherever you've saved it
USER_ID = '107033731246200681024' #Tim O' Reilly
USER_I = 'QueryBy_Id_Output'

DATA = USER_ID + '.json'
data = json.loads(open(DATA).read())

# Number of collocations to find
N = 100

all_tokens = [token for activity in data for token in activity['object']['content'
].lower().split()]

'''
for activity in data:
 for token in activity['object']['content'].lower().split() :
  all_tokens.append(token.encode(''''ascii''''))  
'''

finder = nltk.BigramCollocationFinder.from_words(all_tokens)

'''
print finder.word_fd['truly']
print finder.word_fd['horrible'] 


print 
print finder.ngram_fd[('truly', '') ]


without creation of instance, function is called so in the implementation of the fucntion(cls,words,window size=2)
'''

finder.apply_freq_filter(2)

finder.apply_word_filter(lambda w: w in nltk.corpus.stopwords.words('english'))

'''
for ngram, freq in iteritems(finder.ngram_fd):
 print ngram," " , freq
'''

scorer = nltk.metrics.BigramAssocMeasures.jaccard

collocations = finder.nbest(scorer, N)

for collocation in collocations:
    #print collocation
    c = ' '.join(collocation)
    #s1= c.split(" ")
    print c
    
'''

print "Trigram Functionality " 
print 

finder1 = nltk.TrigramCollocationFinder.from_words(all_tokens)

finder1.apply_freq_filter(3)

finder1.apply_word_filter(lambda w: w in nltk.corpus.stopwords.words('english'))

scorer = nltk.metrics.TrigramAssocMeasures.jaccard

collocations = finder1.nbest(scorer, N)

for collocation in collocations:
    c = ' '.join(collocation)
    print c
'''
    
