import os
from math import log
import json
import nltk
# Load in human language data from wherever you've saved it
import operator
from nltk.compat import iteritems
from collections import OrderedDict

#trainer_set is the dictonary which contain the bigrams with respective to the indentifier of the language
trainer_set = {}

'''
For time being we have kept only four types of language and 3 files of each language as trainer data.
At any point of time addtion of language or files of particular language wont be troublesome.
you will just have to make a list consisting of the name of files of that particular language and append that in 'files[]'.
In case you want to increase the training data just add file names in the given lists.
All other working will be handled by the program itself.
'''

#List of lists which contains the files from which the trainer_set will be generated
fileName1 = ['c1.txt','c2.txt','c3.txt']
fileName2 = ['cpp1.txt','cpp2.txt','cpp3.txt']
fileName3 = ['python1.txt','python2.txt','python3.txt']
fileName4 = ['java1.txt','java2.txt','java3.txt']

files=[]
files.append(fileName1)
files.append(fileName2)
files.append(fileName3)
files.append(fileName4)

i = 0


for fileName in files:
	#i is the identifier of the languages	
	i = i + 1
	all_tokens = [] 
	
	for name in fileName :

		#to access the path of file. os.getcwd return the current working path.
		path=os.getcwd()+'/'+name
		f=open(path,'r')

		#all the tokens of a particular language is stored in all_tokens
		for line in f.readlines():
			for word in line.split():
				all_tokens.append(word)

	'''bigrams of a particular language are extracted.
	Here we didnot use any frequency filter since any bigram may be of significant use.
	And for languages there are no defined set of stopwords hence stopword filter is also not used
	'''
	finder = nltk.BigramCollocationFinder.from_words(all_tokens)

	#the bigrams extracted are iterated to find whether the same bigram is present in any othe language or not
	for ngram, freq in iteritems(finder.ngram_fd):
		
		#in case the bigram appears in more than one language its value is made -1 to signify that the bigram is insignificant to 			classify
		if ngram in trainer_set:
			trainer_set[ngram] = -1
		else:
			trainer_set[ngram]=i


#browse choose files to classify 
while True :

	tokens = []

	#in case you want to claasify more than one file
	print "Enter name of file you want to classify OR -1 To exit"

	#take the name of file to be classified as input from the user
	file_check = raw_input()

	#check if the user wants to end the classification of files 
	if file_check == str(-1):
	 break

	#path which stores the path of the file tobe classified
	path1=os.getcwd()+'/'+file_check
	f1=open(path1,'r') 

	#all the tokens are stored in tokens[]
	for line in f1.readlines():
		for word in line.split():
			tokens.append(word)

	#bigram of the file to be classified is extracted
	finder1 = nltk.BigramCollocationFinder.from_words(tokens)

	#counters to keep track of which particular language bigrams appear most.
	c_count = 0
	cpp_count = 0
	p_count = 0
	j_count = 0

	#counters are updated
	for ngram, freq in iteritems(finder1.ngram_fd):
		if ngram in trainer_set:
			if trainer_set[ngram] == -1:
				continue
			elif trainer_set[ngram] == 1:
				c_count = c_count + 1
			elif trainer_set[ngram] == 2:
				cpp_count = cpp_count + 1
			elif trainer_set[ngram] == 3:
				p_count = p_count + 1
			elif trainer_set[ngram] == 4:
				j_count = j_count + 1	

	#the counter with maximum count is being checked to declare the result
	if c_count == cpp_count and cpp_count == p_count and p_count == j_count :
	 print "Insufficient training set to classify this document "
	else: 
	 if c_count >= cpp_count and c_count >= p_count and c_count >= j_count:
		print "the document is a c source code"
	 elif cpp_count >= c_count and cpp_count >= p_count and cpp_count >= j_count:
		print "the document is a c++ source code"
	 elif p_count >= cpp_count and p_count >= c_count and p_count >= j_count:
		print "the document is a python source code"
	 elif j_count >= cpp_count and j_count >= c_count and j_count >= p_count:
		print "the document is a java source code"	
