
import os


file2= '/out_with_filter/pmi'
file3= '/out_with_filter/compare'

path2=os.getcwd()+file2
path3=os.getcwd()+file3
f=open(path3,'a')


list_file=['jaccard','chi_sq']


for filename in list_file:
	summ = 0
	n = 0
	rank_old = 1
	file1= '/out_with_filter/'	
	file1=file1+filename
	path1=os.getcwd()+file1	
	f1=open(path1,'r')
	for line in f1.readlines():
		bigram = line.split(' ')
		counter = 1
		for line1 in open(path2):
		 bigram1 = line1.split(' ')
		 if bigram[0]==bigram1[0] and bigram[1][:-1]==bigram1[1][:-1] :
		  summ = summ + (rank_old - counter) ** 2	
		  n = n + 1
		  break
		 else:
		  counter = counter + 1 

		rank_old=rank_old+1  

	res = 1-((6 * summ ) / float(n * (n ** 2 - 1)))
	print "Spearman correalaton coefficient with "+str(filename)+" is " + str(res)
	print
	print


f.flush()
f.close()
f1.close()	  
