#import regex
import re
import csv
import pprint
import nltk.classify
import get_twitter_data
import json

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)
#end

#start process_tweet
def processTweet(tweet):
    # process the tweets
    
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)    
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end 

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet, stopWords):
    featureVector = []  
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences 
        w = replaceTwoOrMore(w) 
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #ignore if it is a stopWord
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector    
#end

#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end


#Read the tweets one by one and process it
inpTweets = csv.reader(open('data/sampleTweets.csv', 'rb'), delimiter=',', quotechar='|')

#inpTweets = csv.reader(open('data/hello1.csv', 'rb'), delimiter='', quotechar='|')
stopWords = getStopWordList('data/feature_list/stopwords.txt')
count = 0;
featureList = []
tweets = []
cnt = 0;
for row in inpTweets:
    #left_text = row.partition(",")[0]
    #print(left_text)	
    sentiment = row[0]
    tweet = row[1]
    cnt = cnt + 1
    if cnt == 200:
	break;
    print(tweet)
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));
#end loop

# Remove featureList duplicates
featureList = list(set(featureList))
print "done1"
# Generate the training set
training_set = nltk.classify.util.apply_features(extract_features, tweets)
print "done2"
# Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
print "done3"
# Test the classifier
for i in range(0,15):
	print "keyword"
	keyword = raw_input()
	#keyword = 'obama'
	time = 'today'
	twitterData = get_twitter_data.TwitterData()
	tweets = twitterData.getTwitterData(keyword, time)
	print tweets
	print json.dumps(tweets, indent=1)

	for testTweet in tweets:
		#print "this is"
		#print testTweet
		#testTweet = "I hate mia"
		processedTestTweet = processTweet(testTweet)
		#print nltk.classify.accuracy(NBClassifier, training_set)
		#print NBClassifier.show_most_informative_features(5)
		sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
		print "testTweet = %s, sentiment = %s\n" % (testTweet, sentiment)
		




