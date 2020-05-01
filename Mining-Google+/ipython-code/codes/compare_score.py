
import os

file1= '/out_with_filter/jaccard'
file2= '/out_with_filter/new_method'
file3= '/out_with_filter/compare'
path=os.getcwd()+file1
path2=os.getcwd()+file2
path3=os.getcwd()+file3
f=open(path3,'a')
f2=open(path2,'r')
f1=open(path,'r')
rank_in_Jaccard = 1
f.write("Jaccard Rank    Bigram 							" + "Rank in Our Method \n")
for line in f1.readlines():
	bigram = line.split(' ')
	counter = 1
	for line1 in open(path2):
	 bigram1 = line1.split(' ')
	 if bigram[0]==bigram1[0] and bigram[1][:-1]==bigram1[1][:-1] :
	  s = str(bigram[0])+" "+str(bigram[1][:-1])
	  l=65-len(s)
	  for i in range(l):
	  	s=s+' '
	  f.write( str(rank_in_Jaccard)+"     		"+s+str(counter)+"\n" )
	  break
	 else:
	  counter = counter + 1 
	rank_in_Jaccard=rank_in_Jaccard+1  
	
f.flush()
f.close()
f1.close()
f2.close()	  
