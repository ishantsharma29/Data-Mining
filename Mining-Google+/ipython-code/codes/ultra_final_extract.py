
# Importing all Packages
from IPython.html import widgets
import httplib2
import json
import nltk
from IPython.core.display import HTML
import apiclient.discovery 
from IPython.display import Image
import httplib2
import json
from bs4 import BeautifulSoup
import apiclient.discovery
import os
import httplib2
import json
import apiclient.discovery
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from math import log
import operator
from nltk.compat import iteritems
from collections import OrderedDict

#Number of topmost posts of User according to selected bigram 
top_post=0

# A list that will contain all the tokens from all the activities of the mined user
all_tokens = []

# Corpus is the collection of all posts of Google+ user
corpus={}

#This dictionary stores the TF-IDF value for each bigram
tf_idf_scores={}


# This function is called whenever a user types anything in the Text Column to detect trait change
def printTraitChange(name):
    print "Y"
   

# This function Extracts all the posts of the Selected user in Json format and stores it in a file for further processing  
def mineSelectedUser(widget):
    form = container_2.children
    #User Information which is to be mined
    
    G = form[0].value
    #Combination of Name > ID

    words = G.split(">")
    ide = words[2]
    #Extracting ID of user
    
    
    USER_ID = ide
    #USER_ID = '107033731246200681024'
    
    API_KEY = 'AIzaSyDMJRu_ZTMkxZaYWOgaNXp4Ook1djTrEGE'
    #GOOGLE+ API KEY from https://code.google.com/apis/console

    
    MAX_RESULTS = 20000 # Will require multiple requests
   
    # This function cleans the HTML markup from the extracted JSON data
    # such as <br /> tags and escaped HTML entities for apostrophes 
    
    def cleanHtml(html):
        if html == "": return ""

        soup = BeautifulSoup(html)
        return BeautifulStoneSoup(soup.get_text(),
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]

    # service object returned by API client to connect to google+ API
    service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(),developerKey=API_KEY)

    #we create a connection to the Acitivity API by invoking service.activity()
    activity_feed = service.activities().list(
        userId=USER_ID,
        collection='public',
        maxResults='100' # Max allowed per request
    )

    # List of all the activities of the user
    activity_results = []

    # Extract activities untill either activities are finished or max required limit is reached
    while activity_feed != None and len(activity_results) < MAX_RESULTS:
        activities = activity_feed.execute()
        if 'items' in activities:
            for activity in activities['items']:
                if activity['object']['objectType'] == 'note' and \
                activity['object']['content'] != '':

                    activity['title'] = cleanHtml(activity['title'])
                    activity['object']['content'] = cleanHtml(activity['object']['content'])
                    activity_results += [activity]
    # list_next requires the previous request and response objects

        activity_feed = service.activities().list_next(activity_feed, activities)
    
    # Write the output to a file for convenience
    f = open(os.path.join(USER_ID + '.json'), 'w')
    f.write(json.dumps(activity_results, indent=1))
    f.close()
    
    # Output on terminal the no of activities extracted
    print str(len(activity_results)), "activities written to", f.name

	
    # Load in human language data from wherever you've saved it	
    dfile = USER_ID + '.json'
    data = json.loads(open(dfile).read())
   
    #all_tokens = [token for activity in data for token in activity['object']['content'].lower().split()]
    
    #Insert tokens from all activities into a single list 
    for activity in data:
        for token in activity['object']['content'].lower().split():
            all_tokens.append(token)
    
    
    # Create corpus of all activity
    i=0
    for activity in data:
        corpus[i]=' '.join( activity['object']['content'].lower().split() )
        i=i+1
    
    
    # Number of collocations to required 
    print "Enter the number of collocations need to be found"
    #N = input() for command line purpose
    #newline
    print
    
    # Text label to write number of collocations required( Integer value )
    control_5 = widgets.TextWidget(description="Enter number of collocations required: ")
    
    # Submit button for the program to take input from text label
    control_6 = widgets.ButtonWidget(description="Submit")
    
    # It calls printTraitChange function whenever a user types anthing in text label
    control_5.on_trait_change(printTraitChange, "value")
    
    #On submit the it call the process_request function
    control_6.on_click(process_request)
    
    #container that holds the Input of Collocation
    container_3.children = [control_5, control_6]
    


# This function does scoring of bigrams by proposed method , ranks them and prompts user to choose bigram on which TF-IDF is applied
def process_request(widget):
    
    
    print "process request going on ..."
    form1 = container_3.children
    
    # Fetching value (number of collocations) from form 
    N=int(form1[0].value)
    
    # The number of collocations required
    print N
    
    #print "------------------------------------------------",all_tokens
    
    '''
    Construct a BigramCollocationFinder for all bigrams in the given sequence.
    This object has frequency of all unigrams and bigrams calculated.
    '''
    
    finder = nltk.BigramCollocationFinder.from_words(all_tokens)

    # Filter those bigrams that have frequency less than 2
    finder.apply_freq_filter(2)

    # Filter those bigrams that contain stopwords
    finder.apply_word_filter(lambda w: w in nltk.corpus.stopwords.words('english'))
	
	
    bigram_score = OrderedDict()
    #Implementation of Proposed Scoring Method
    for ngram,freq in iteritems(finder.ngram_fd):
      # one by one for each bigram 
      
      #bigram frequency 
      bi_freq = finder.ngram_fd[ngram]
      
      # Frequency of both unigrams in bigram
      w1=finder.word_fd[ngram[0]]
      w2=finder.word_fd[ngram[1]]
      
      # Score of each bigram
      score = (bi_freq)/float(w1*(w1-bi_freq)+w2*(w2-bi_freq)+bi_freq)
      #print score
      bigram_score[ngram]=score

    print "Scoring Done"
    
    # A variable to keep track of top bigrams according to ranking
    count_bigrams = 0

    # List that stores required number of bigrams in sorted order of score
    list_bigram=[]

    for (k,v) in sorted(bigram_score.items(),key=operator.itemgetter(1),reverse=True):

      if count_bigrams == N:
         print "Required Number of Bigrams collected"
         break
      else :
         list_bigram.append('~'.join(k))
         count_bigrams =  count_bigrams + 1

    print "***************MENU**********************"
    print
    
    #lIST Of Required number of bigrams
    print list_bigram
    
    
    print "Listing Bigrams "
    # To display on CLI
    index=1
    for bigram in list_bigram:
      print str(index)+')'+bigram 
      index = index + 1

    
    # Displays List of Bigrams on the IPython Notebook GUI
    control_7 = widgets.RadioButtonsWidget(values=list_bigram, description="Choose any bigram from the below list")
    
    control_7.on_trait_change(printTraitChange, "value")
    
    # Label to Enter number of posts required for selected bigram
    control_8 = widgets.TextWidget(description="Enter the number of top most post for the selected bigram: ")
    control_8.on_trait_change(printTraitChange, "value")
    
    # Submit button
    control_9 = widgets.ButtonWidget(description="Submit")
    
    # On submit control jumps to function TF-IDF to evaluate TF-IDF for selected bigram
    control_9.on_click(TF_IDF)
    container_4.children = [control_7, control_8 , control_9]
    
    
# This function calculated TF-IDF as proposed by us    
def TF_IDF(widget):	
                
        # Store Bigram removing the separator '~'
        form2 = container_4.children
        QT = form2[0].value.split('~')
        print QT
        
        top_post=int(container_4.children[1].value) 
        # = list_bigram[inp-1].split('~')

        print
        #dictionary to keep term frequency of all posts for bigram in query
        tf_scores={}

        for key in corpus:
            match = 0
            list_doc = []

            for term in corpus[key].lower().split(' '):
               list_doc.append(term)

            total_count=len(list_doc)-1

            # Count frequency of Bigram in a post
            for i in range(len(list_doc)-1):
               if list_doc[i] == QT[0] and  list_doc[i+1] == QT[1] :
                 match=match+1
			 
            #print "bIGRAM fREQuency" , match  

            #print "Total Bigrams in selected Post" ,total_count

            c=0
            # Count bigrams that contains stopwords
            for i in range(len(list_doc)-1):
               for w in nltk.corpus.stopwords.words('english'):
                 if list_doc[i]== w :
                    i=i+1
                    c=c+1
			
            # Total Valid Bigrams after removing bigrams that had stopwords in it	   
            total_count=total_count - c
            #print "Valid Bigrams in selected post ",total_count
            if total_count==0:
               total_count=1 

	
            tf = match/ float(total_count)
            #print "Term Frequency" , tf
            tf_scores[key]=tf  

        '''
         IDF Implementation
        '''

        # variable to store the number of posts in which bigram is present
        num_of_matches=0
	
        # List that stores all tokens of an activity under consideration
        corpus_list = []
        for doc in corpus:
            for term in corpus[doc].lower().split(' '):
               corpus_list.append(term)
		   
            for i in range(len(corpus_list)):
               if corpus_list[i] == QT[0] and i+1<len(corpus_list) and  corpus_list[i+1] == QT[1] :
                  num_of_matches=num_of_matches+1
                  break     
            #Clears the list for next activity
            corpus_list=[]
		 
		 
        #print "No of posts in which Bigram is present",num_of_matches 

        #print "Len corpus", len(corpus)
        if num_of_matches != 0:
            idf = 1.0 + log(float(len(corpus)) / num_of_matches )
        else:
            idf =1
		  
        #print "InverseDocument Frequency ",idf 

        #Evaluate TF-IDF 
        for key in tf_scores:
            tf_idf_scores[key]=tf_scores[key]*idf
        
        
        #call to print posts in sorted TF-IDF values
        print_Top_Posts()   



# This function sorts TF-IDF dictionary in decreasing order of TF-IDF values and displays topmost required posts
def print_Top_Posts():
		
        tf_list=[]
        counter = 0
        for (k,v) in sorted(tf_idf_scores.items(),key=operator.itemgetter(1),reverse=True):
            if v==0.0:
                print "In ", str(counter) ,"posts only, this bigram was found"
                break	
            print corpus[k]
            print
            print "TF-IDF",v
            tf_list.append( corpus[k]+ str("TF-IDF") + str(v)+ str("\n" ) )
            print
            print
            counter = counter + 1
            if counter == top_post:
               break
            
        control_10 = widgets.RadioButtonsWidget(values=tf_list, description="Top Posts")
        
        control_10.on_trait_change(printTraitChange, "value")
        container_5.children = [control_10]       
        
        
        accordion = widgets.AccordionWidget()
        accordion.children = [container_5] 
        accordion

        accordion.set_title(0, "Top Posts")
        
        popup = widgets.PopupWidget(description="Top Posts")
        popup.children = [accordion]
        popup

        
def calculate_form(name):
    # Retreive values from form
    print "X"
    
    
def searchPeople(widget):
    form = container_1.children
    Q = form[0].value
    
    #Username Entered
    print Q
    
    #API key of project
    API_KEY = 'AIzaSyDMJRu_ZTMkxZaYWOgaNXp4Ook1djTrEGE'
    
    #List to keep all people with the entered name as a substring in name
    listt=[]

    
    service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(),developerKey=API_KEY)

    people_feed = service.people().search(query=Q).execute()
    #print json.dumps(people_feed['items'], indent=1)

    html = []
    listt = []

    for p in people_feed['items']:
        #html += ['<p><img src="%s" /> %s: %s</p>' % \
        #(p['image']['url'], p['id'], p['displayName'])]
        print "hii"
        #html = html + p['id']
        #html = html + p['displayName'] 
        listt.insert(0, "Name=> " + p['displayName'] + " Id=>" + p['id'])
        
    print listt
    #HTML(''.join(html))
    
    
    #Displays all users of entered username
    control_3 = widgets.RadioButtonsWidget(values=listt, description="Select User_id to mine")
    
    #Button to start mining of selected user
    control_4 = widgets.ButtonWidget(description="Mine this User")
    control_3.on_trait_change(printTraitChange, "value")
    
    #Jump to function mineSelectedUser in Submitting
    control_4.on_click(mineSelectedUser)
    container_2.children = [control_3, control_4]
    
       
    
#Containers of widget
container_1 = widgets.ContainerWidget()
container_2 = widgets.ContainerWidget()
container_3 = widgets.ContainerWidget()
container_4 = widgets.ContainerWidget()
container_5 = widgets.ContainerWidget()


#Control to Begin Mining
control_1 = widgets.TextWidget(description="Username: ")
control_2 = widgets.ButtonWidget(description="Submit")
control_1.on_trait_change(calculate_form, "value")

#Call to search people on google+ with entered username
control_2.on_click(searchPeople)
container_1.children = [control_1, control_2]


accordion = widgets.AccordionWidget()
accordion.children = [container_1, container_2, container_3, container_4] 
accordion

#Title of each block
accordion.set_title(0, "Google+")
accordion.set_title(1,"Result g+")
accordion.set_title(2, "Collocations")
accordion.set_title(3, "List of Bigrams")


#Pop up when program runs - Beginning of Interface
popup = widgets.PopupWidget(description="Data Mining Project")
popup.children = [accordion]
popup



