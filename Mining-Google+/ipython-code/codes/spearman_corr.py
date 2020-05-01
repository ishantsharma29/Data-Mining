
import os

#directory of the file which contains 100 bigrams extracted by our proposed method
file2= '/out_with_filter/new_method'

#entire path of the file
path2=os.getcwd()+file2

f=open(path3,'a')

#list of files with which contains bigrams extracted from predefined existing methods
list_file=['jaccard','pmi','chi_sq','raw_freq','student_t']

#all the files are iterated
for filename in list_file:
	summ = 0

	#number of bigrams
	n = 0

	#rank of the corresponding bigram extracted by existing methods 
	rank_old = 1
	file1= '/out_with_filter/'	
	file1=file1+filename
	path1=os.getcwd()+file1	
	f1=open(path1,'r')
	for line in f1.readlines():
		bigram = line.split(' ')

		#rank of the corresponding bigram extracted by our proposed method
		counter = 1
		for line1 in open(path2):
		 bigram1 = line1.split(' ')

		#the diffrence between ranks of each corresponding bigram
		 if bigram[0]==bigram1[0] and bigram[1][:-1]==bigram1[1][:-1] :
		  summ = summ + (rank_old - counter) ** 2	
		  n = n + 1
		  break
		 else:
		  counter = counter + 1 

		
		rank_old=rank_old+1  

	#The spearman correlation coefficient is evaluated
	res = 1-((6 * summ ) / float(n * (n ** 2 - 1)))
	print "Spearman correalaton coefficient with "+str(filename)+" is " + str(res)
	print
	print


f.flush()
f.close()
f1.close()	  
