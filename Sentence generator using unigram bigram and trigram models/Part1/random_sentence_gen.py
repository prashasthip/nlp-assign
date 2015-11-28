
# INPUT : list of lists

from math import log
from nltk import word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
from collections import Counter
from random import randint

unigram_keys = []

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
	#print bigram_model

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

def file_generator_unigram():

	unigram_file = open("Unigram.csv","w")
	
	for details in unigram_model:
		line = details + "," + str(unigram_model[details][0]) + "," + str(unigram_model[details][1]) + "," + str(unigram_model[details][2]) +"\n"
		unigram_file.write(line)
	unigram_file.close()

	

def file_generator_bigram():

	
	bigram_file = open("Bigram.csv","w")
	
	for details in bigram_model:
		line = details[0] + "," + details[1] + "," + str(bigram_model[details][0]) + "," + str(bigram_model[details][1]) + "," + str(bigram_model[details][2])  + "\n"
		bigram_file.write(line)
	bigram_file.close()

	

def file_generator_trigram():

	trigram_file = open("Trigram.csv","w")

	for details in trigram_model:
		line = details[0] + "," + details[1] + "," + details[2] + "," + str(trigram_model[details][0]) + "," + str(trigram_model[details][1]) + "," + str(trigram_model[details][2])  +"\n"
		trigram_file.write(line)
	trigram_file.close()

def tokenize_input():
	global list_of_start
	global list_of_end
	file=open("corpus1.txt")
	data=file.read()
	sentences=PunktSentenceTokenizer().tokenize(data)
	corpus=[]
	for i in sentences:
		s1=[]
		sentence=word_tokenize(i)
		for j in range(0,len(sentence)):
			if(sentence[j] not in ["",".",",","`","?","!",")","(","``","[","]",";","''","'"]):
				s1.append(sentence[j].lower())
		if(len(s1)!=0):
			list_of_start.append(s1[0])
			list_of_end.append(s1[-1])
			corpus.append(s1)
	return corpus
#inn =[["Hey","how","are","you"],["you","are","how","are"],["Hey","how","are"]]

def sentence_unigram():
	sent1 =[]
	unigram_keys = unigram_model.keys()
	sindex = randint(0,len(list_of_start)-1)	
	sent1.append(list_of_start[sindex])
	for i in range(0,5):
		nindex = randint(0,len(unigram_keys)-1)
		word = unigram_keys[nindex]
		sent1.append(word)
	while(True):
		nindex = randint(0,len(unigram_keys)-1)
		word = unigram_keys[nindex]
		sent1.append(word)
		if(word in list_of_end):
			sent1.append(".")
			break
	return sent1
	
			
def sentence_bigram():
	sent1= []
	bigram_keys = bigram_model.keys()
	sindex = randint(0,len(list_of_start)-1)
	bigram_start = []
	for i in bigram_keys:
		if(i[0]==list_of_start[sindex]):
			bigram_start.append(i)
	sindex = randint(0,len(bigram_start)-1)
	sent1.append(bigram_start[sindex])
	word1 = bigram_start[sindex]
	while(True):
		word = word1[1]
		if(word in list_of_end and len(sent1) > 8 ):
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
			sindex = randint(0,len(bigram_list)-1)
		sent1.append(bigram_list[sindex])
		word1 = bigram_list[sindex]
	return sent1

def sentence_trigram():
	sent1= []
	trigram_keys = trigram_model.keys()
	sindex = randint(0,len(list_of_start)-1)
	trigram_start = []
	for i in trigram_keys:
		if(i[0]==list_of_start[sindex]):
			trigram_start.append(i)
	sindex = randint(0,len(trigram_start)-1)
	sent1.append(trigram_start[sindex])
	word1 = trigram_start[sindex]
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
			sindex = randint(0,len(trigram_list)-1)
		sent1.append(trigram_list[sindex])
		word1 = trigram_list[sindex]
	return sent1
	

list_of_start = []
list_of_end = []
corpus = tokenize_input()

unigram_generator(corpus)

bigram_generator(corpus)

trigram_generator(corpus)


unifile=open("randomUniSentence.txt","w")
for i in range(0,10):
	uni_sent=""
	uni_sent_list = sentence_unigram()
	for j in uni_sent_list:
		uni_sent += j + " "
	unifile.write(uni_sent+"\n\n")

bifile=open("randomBiSentence.txt","w")
for i in range(0,10):
	bi_sent=""
	bi_sent_list = sentence_bigram()
	bi_sent+=bi_sent_list[0][0] + " " +bi_sent_list[0][1] + " "
	for j in range(1,len(bi_sent_list)-1):
		if(bi_sent_list[j][1]!="^"):
			bi_sent += bi_sent_list[j][1] + " "
	bi_sent += "."
	bifile.write(bi_sent+"\n\n")

trifile=open("randomTriSentence.txt","w")

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



