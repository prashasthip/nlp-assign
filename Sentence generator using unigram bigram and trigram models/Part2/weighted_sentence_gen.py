
# INPUT : list of lists

from math import log
from nltk import word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
from collections import Counter
from random import randint

unigram_keys = []

def tokenize_input():
	global list_of_start
	global list_of_end
	file=open("Corpus 2.txt")
	data=file.read()
	sentences=PunktSentenceTokenizer().tokenize(data)
	corpus=[]
	for i in sentences:
		s1=[]
		sentence=word_tokenize(i)
		for j in range(0,len(sentence)):
			if(sentence[j] not in ["",".",",","`","?","!",")","(","``","[","]",";","''","'","'s"]):
				s1.append(sentence[j].lower())
		if(len(s1)!=0):
			list_of_start.append(s1[0])
			list_of_end.append(s1[-1])
			corpus.append(s1)
	return corpus

def unigram_generator(inList):

	global unigram_model

	frequencyDict={}
	total_count = 0
	for sentence in inList:
		for word in sentence:
			if word in frequencyDict:
				frequencyDict[word]=[frequencyDict[word][0]+1] 
				total_count+= 1 
			else:
				frequencyDict[word] = [1]
				total_count+= 1

	#(frequencyDict,total_count) = frequency_calculator(inList)
	
	for word in frequencyDict:
		count = frequencyDict[word][0]
		q_ML = count/(total_count*1.0)
		log_q_ML = log(q_ML,10)
		frequencyDict[word].append(q_ML)
		frequencyDict[word].append(log_q_ML)
		
		

	unigram_model = frequencyDict

def bigram_generator(inList):

	global bigram_model
	
	for sentence in inList:
		sentence.insert(0,'$')
		sentence.append('^')

	frequencyDict={}

	for i in range(0,len(inList)):
		for j in range(0,len(inList[i])-1):
			pair = (inList[i][j],inList[i][j+1])
			if pair in frequencyDict:
				frequencyDict[pair]=[ frequencyDict[pair][0] + 1 ]
			else:
				frequencyDict[pair]=[1]
		
	for word in frequencyDict:
		count = frequencyDict[word][0]
	 	word_1 = word[0]
		if (word_1 == '$'):
			count_word1 = len(inList)
		else:
			count_word1 = unigram_model[word_1][0]
		q_ML = count/(count_word1*1.0)
		log_q_ML = log(q_ML,10)
		frequencyDict[word].append(q_ML)
		frequencyDict[word].append(log_q_ML)

	bigram_model = frequencyDict

def trigram_generator(inList):

	global trigram_model


	for sentence in inList:
		sentence.insert(0,'$')
		sentence.append('^')

	frequencyDict={}
	
	for i in range(0,len(inList)):
		for j in range(0,len(inList[i])-2):
			triplet = (inList[i][j],inList[i][j+1],inList[i][j+2])
			if triplet in frequencyDict:
				frequencyDict[triplet] = [frequencyDict[triplet][0]+1]
			else:
				frequencyDict[triplet] = [1]
		
	for word in frequencyDict:
		count = frequencyDict[word][0]
		word_1 = word[0]
		word_2 = word[1]
		if (word_1 == '$' and word_2 == '$'):
			count_word1_word2 = len(inList)
		else:
			word_tuple = (word_1,word_2)
			count_word1_word2 = bigram_model[word_tuple][0]
		q_ML = count/(count_word1_word2*1.0)
		log_q_ML = log(q_ML,10)
		frequencyDict[word].append(q_ML)
		frequencyDict[word].append(log_q_ML)

	trigram_model = frequencyDict


startmaxlist=[]
endmaxlist=[]
maxlist=[]


	
def generateMaxProbStart_End():
	set_list = set(list_of_start)
	set_end = set(list_of_end)
	max_prob_start = 0
	max_prob_end = 0
	global max_prob_start_list
	global max_prob_end_list
	count_word = []
	for i in set_list:
		count_word.append([i,list_of_start.count(i)])
		count_word.sort(key=lambda x:x[1])
	count_word = count_word[-20:]
	for i in count_word:
		max_prob_start_list.append(i[0])
	count_word = []
	for i in set_end:
		count_word.append([i,list_of_end.count(i)])
		count_word.sort(key=lambda x:x[1])
	for i in count_word:
		max_prob_end_list.append(i[0])
	
	

def sentence_bigram():
	sent1= []
	bigram_keys = bigram_model.keys()		
	sindex = randint(0,len(max_prob_start_list)-1)
	bigram_start = []
	for i in bigram_keys:
		val = max_prob_start_list[sindex]
		if(i[0]==val):
			bigram_start.append(i)
	max_prob = 0
	count_word = []
	max_big = []
	for i in bigram_start:
		mult = bigram_model[i][0] * bigram_model[i][1]
		count_word.append([i,mult])
	count_word.sort(key=lambda x:x[1])
	for i in count_word:
		max_big.append(i[0])

	sindex = randint(0,len(max_big)-1)
	sent1.append(max_big[sindex])		
	word1 = max_big[sindex]	
	
	while(True):
		word = word1[1]
		if(word in max_prob_end_list and len(sent1) > 8 ):
			sent1.append(".")
			break
		bigram_list = []
		for i in bigram_keys:
			if(i[0]==word):
				bigram_list.append(i)
		if ( len(bigram_list) == 0 ):
			sent1.append(".")
			break
		else:
			count_word = []
			max_big = []
			for i in bigram_list:
				mult = bigram_model[i][0] * bigram_model[i][1]
				count_word.append([i,mult])
			count_word.sort(key=lambda x:x[1])
			for i in count_word:
				max_big.append(i[0])
			
		sindex = randint(0,len(max_big)-1)
		sent1.append(max_big[sindex])		
		word1 = max_big[sindex]
	return sent1

def sentence_trigram():
	sent1= []
	trigram_keys = trigram_model.keys()		
	sindex = randint(0,len(max_prob_start_list)-1)
	trigram_start = []
	for i in trigram_keys:
		val = max_prob_start_list[sindex]
		if(i[0]==val):
			trigram_start.append(i)
	max_prob = 0
	count_word = []
	max_big = []
	for i in trigram_start:
		mult = trigram_model[i][0] * trigram_model[i][1] 
		count_word.append([i,mult])
	count_word.sort(key=lambda x:x[1])
	for i in count_word:
		max_big.append(i[0])

	sindex = randint(0,len(max_big)-1)
	sent1.append(max_big[sindex])		
	word1 = max_big[sindex]	
	
	while(True):
		word = word1[1]
		word2 = word1[2]
		if(word2 in list_of_end and len(sent1) > 15 ):
			sent1.append(".")
			break
		trigram_list=[]
		for i in trigram_keys:
			if(i[0]==word and i[1]==word2):
				trigram_list.append(i)
		if ( len(trigram_list) == 0 ):
			sent1.append(".")
			break
		else:
			count_word = []
			max_big = []
			for i in trigram_list:
				mult = trigram_model[i][0] * trigram_model[i][1]
				count_word.append([i,mult])
			count_word.sort(key=lambda x:x[1])
			for i in count_word:
				max_big.append(i[0])
			
		sindex = randint(0,len(max_big)-1)
		sent1.append(max_big[sindex])		
		word1 = max_big[sindex]
	return sent1



# INPUT : list of lists

from math import log
from nltk import word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
from collections import Counter
from random import randint

unigram_keys = []

def tokenize_input():
	global list_of_start
	global list_of_end
	file=open("Corpus1.txt")
	data=file.read()
	sentences=PunktSentenceTokenizer().tokenize(data)
	corpus=[]
	for i in sentences:
		s1=[]
		sentence=word_tokenize(i)
		for j in range(0,len(sentence)):
			if(sentence[j] not in ["",".",",","`","?","!",")","(","``","[","]",";","''","'","'s"]):
				s1.append(sentence[j].lower())
		if(len(s1)!=0):
			list_of_start.append(s1[0])
			list_of_end.append(s1[-1])
			corpus.append(s1)
	return corpus

def unigram_generator(inList):

	global unigram_model

	frequencyDict={}
	total_count = 0
	for sentence in inList:
		for word in sentence:
			if word in frequencyDict:
				frequencyDict[word]=[frequencyDict[word][0]+1] 
				total_count+= 1 
			else:
				frequencyDict[word] = [1]
				total_count+= 1

	#(frequencyDict,total_count) = frequency_calculator(inList)
	
	for word in frequencyDict:
		count = frequencyDict[word][0]
		q_ML = count/(total_count*1.0)
		log_q_ML = log(q_ML,10)
		frequencyDict[word].append(q_ML)
		frequencyDict[word].append(log_q_ML)
		
		

	unigram_model = frequencyDict

def bigram_generator(inList):

	global bigram_model
	
	for sentence in inList:
		sentence.insert(0,'$')
		sentence.append('^')

	frequencyDict={}

	for i in range(0,len(inList)):
		for j in range(0,len(inList[i])-1):
			pair = (inList[i][j],inList[i][j+1])
			if pair in frequencyDict:
				frequencyDict[pair]=[ frequencyDict[pair][0] + 1 ]
			else:
				frequencyDict[pair]=[1]
		
	for word in frequencyDict:
		count = frequencyDict[word][0]
	 	word_1 = word[0]
		if (word_1 == '$'):
			count_word1 = len(inList)
		else:
			count_word1 = unigram_model[word_1][0]
		q_ML = count/(count_word1*1.0)
		log_q_ML = log(q_ML,10)
		frequencyDict[word].append(q_ML)
		frequencyDict[word].append(log_q_ML)

	bigram_model = frequencyDict

def trigram_generator(inList):

	global trigram_model


	for sentence in inList:
		sentence.insert(0,'$')
		sentence.append('^')

	frequencyDict={}
	
	for i in range(0,len(inList)):
		for j in range(0,len(inList[i])-2):
			triplet = (inList[i][j],inList[i][j+1],inList[i][j+2])
			if triplet in frequencyDict:
				frequencyDict[triplet] = [frequencyDict[triplet][0]+1]
			else:
				frequencyDict[triplet] = [1]
		
	for word in frequencyDict:
		count = frequencyDict[word][0]
		word_1 = word[0]
		word_2 = word[1]
		if (word_1 == '$' and word_2 == '$'):
			count_word1_word2 = len(inList)
		else:
			word_tuple = (word_1,word_2)
			count_word1_word2 = bigram_model[word_tuple][0]
		q_ML = count/(count_word1_word2*1.0)
		log_q_ML = log(q_ML,10)
		frequencyDict[word].append(q_ML)
		frequencyDict[word].append(log_q_ML)

	trigram_model = frequencyDict


startmaxlist=[]
endmaxlist=[]
maxlist=[]


def generateUniLists():

	global startmaxlist
	global endmaxlist
	global maxlist
	global unigram_model
# find list of start words with highest probability
	setstart=set(list_of_start)
	startmaxval=0;
	startlist=[]
	
	for i in setstart :
		startlist.append((i,list_of_start.count(i)))
	startlist.sort(reverse=True,key=lambda i : i[1])

	startlist=startlist[:100]
	

	for i in range(len(startlist)) :
		startlist[i]=(startlist[i][0],startlist[i][1]//10.0)
	#print startlist
	for i in startlist :
		for j in range(0,int(i[1])):
			startmaxlist.append(i[0])

	#print startmaxlist

	interlist=[]
	for i in unigram_model :
		if unigram_model[i][0]>100 :
			interlist.append((i,unigram_model[i][0]))

	interlist.sort(reverse=True,key=lambda i:i[1])

	interlist=interlist[:100]
	for i in range(len(interlist)) :
		interlist[i]=(interlist[i][0],interlist[i][1]//50.0)

	for i in interlist :
		for j in range(0,int(i[1])):
			maxlist.append(i[0])

	#print maxlist
	endlist=[]
	setend=set(list_of_start)
	for i in setend :
		endlist.append((i,list_of_end.count(i)))
	endlist.sort(reverse=True,key=lambda i : i[1])
	endlist=endlist[:100]

	for i in range(len(endlist)) :
		endlist[i]=(endlist[i][0],endlist[i][1]//10.0)

	for i in endlist :
		for j in range(0,int(i[1])):
			endmaxlist.append(i[0])



def sentence_unigram():
	
	sent1 =[]
	
	startword=startmaxlist[randint(0,len(startmaxlist)-1)]
	sent1.append(startword.lower())
	
	for i in range(0,10):
		nindex = randint(0,len(maxlist)-1)
		word = maxlist[nindex]
		sent1.append(word)
	

	for i in range(10,30):
		nindex = randint(0,len(maxlist)-1)
		word = maxlist[nindex]
		if word in endmaxlist:
			sent1.append(word)
			sent1.append(".")
			
			return sent1
		else :
			
			sent1.append(word)

	endword=endmaxlist[randint(0,len(endmaxlist)-1)]
	
	sent1.append(endword)
	sent1.append(".")
	return sent1


max_prob_start_list = []
max_prob_end_list = []

def generateMaxProbStart_End():
	set_list = set(list_of_start)
	set_end = set(list_of_end)
	max_prob_start = 0
	max_prob_end = 0
	global max_prob_start_list
	global max_prob_end_list
	count_word = []
	for i in set_list:
		count_word.append([i,list_of_start.count(i)])
		count_word.sort(key=lambda x:x[1])
	count_word = count_word[-20:]
	for i in count_word:
		max_prob_start_list.append(i[0])
	count_word = []
	for i in set_end:
		count_word.append([i,list_of_end.count(i)])
		count_word.sort(key=lambda x:x[1])
	for i in count_word:
		max_prob_end_list.append(i[0])
	
	

def sentence_bigram():
	sent1= []
	bigram_keys = bigram_model.keys()		
	sindex = randint(0,len(max_prob_start_list)-1)
	bigram_start = []
	for i in bigram_keys:
		val = max_prob_start_list[sindex]
		if(i[0]==val):
			bigram_start.append(i)
	max_prob = 0
	count_word = []
	max_big = []
	for i in bigram_start:
		mult = bigram_model[i][0] * bigram_model[i][1]
		count_word.append([i,mult])
	count_word.sort(key=lambda x:x[1])
	for i in count_word:
		max_big.append(i[0])

	sindex = randint(0,len(max_big)-1)
	sent1.append(max_big[sindex])		
	word1 = max_big[sindex]	
	
	while(True):
		word = word1[1]
		if(word in max_prob_end_list and len(sent1) > 8 ):
			sent1.append(".")
			break
		bigram_list = []
		for i in bigram_keys:
			if(i[0]==word):
				bigram_list.append(i)
		if ( len(bigram_list) == 0 ):
			sent1.append(".")
			break
		else:
			count_word = []
			max_big = []
			for i in bigram_list:
				mult = bigram_model[i][0] * bigram_model[i][1]
				count_word.append([i,mult])
			count_word.sort(key=lambda x:x[1])
			for i in count_word:
				max_big.append(i[0])
			
		sindex = randint(0,len(max_big)-1)
		sent1.append(max_big[sindex])		
		word1 = max_big[sindex]
	return sent1

def sentence_trigram():
	sent1= []
	trigram_keys = trigram_model.keys()		
	sindex = randint(0,len(max_prob_start_list)-1)
	trigram_start = []
	for i in trigram_keys:
		val = max_prob_start_list[sindex]
		if(i[0]==val):
			trigram_start.append(i)
	max_prob = 0
	count_word = []
	max_big = []
	for i in trigram_start:
		mult = trigram_model[i][0] * trigram_model[i][1] 
		count_word.append([i,mult])
	count_word.sort(key=lambda x:x[1])
	for i in count_word:
		max_big.append(i[0])

	sindex = randint(0,len(max_big)-1)
	sent1.append(max_big[sindex])		
	word1 = max_big[sindex]	
	
	while(True):
		word = word1[1]
		word2 = word1[2]
		if(word2 in list_of_end and len(sent1) > 15 ):
			sent1.append(".")
			break
		trigram_list=[]
		for i in trigram_keys:
			if(i[0]==word and i[1]==word2):
				trigram_list.append(i)
		if ( len(trigram_list) == 0 ):
			sent1.append(".")
			break
		else:
			count_word = []
			max_big = []
			for i in trigram_list:
				mult = trigram_model[i][0] * trigram_model[i][1]
				count_word.append([i,mult])
			count_word.sort(key=lambda x:x[1])
			for i in count_word:
				max_big.append(i[0])
			
		sindex = randint(0,len(max_big)-1)
		sent1.append(max_big[sindex])		
		word1 = max_big[sindex]
	return sent1


list_of_start = []
list_of_end = []

corpus = tokenize_input()
unigram_generator(corpus)
generateUniLists()

unifile=open("weightedUniSentence.txt","w")
for i in range(0,10):
	uni_sent=""
	uni_sent_list = sentence_unigram()
	for j in uni_sent_list:
		uni_sent += j + " "

	unifile.write(uni_sent+"\n\n")

generateMaxProbStart_End()

bigram_generator(corpus)
bifile=open("weightedBiSentence.txt","w")
for i in range(0,10):
	bi_sent=""
	bi_sent_list = sentence_bigram()
	#print bi_sent_list
	bi_sent+=bi_sent_list[0][0] + " " +bi_sent_list[0][1] + " "
	for j in range(1,len(bi_sent_list)-1):
		if(bi_sent_list[j][1]!="^"):
			bi_sent += bi_sent_list[j][1] + " "
	bi_sent += "."
	bifile.write(bi_sent+"\n\n")

trigram_generator(corpus)
trifile=open("weightedTriSentence.txt","w")
for i in range(0,10):
	tri_sent=""
	tri_sent_list = sentence_trigram()
#	print tri_sent_list
	tri_sent+=tri_sent_list[0][0] + " " +tri_sent_list[0][1] + " "+ tri_sent_list[0][2] + " "
	for j in range(1,len(tri_sent_list)-1):
		if(tri_sent_list[j][2]!="^"):
			tri_sent += tri_sent_list[j][2] + " "
	tri_sent += "."
	trifile.write(tri_sent+"\n\n")
	

