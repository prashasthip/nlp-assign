import nltk
from nltk.corpus import stopwords

import lex
import re

tokens = ('NUMBER', 'WORD','SNAME','RT','HASHTAG','URL',
'SLANG','SQ','DQ','EMOP','EMON','PUNC','JUNK')

#def t_junk(t):
	#r'\\x85'
	#print("junk")
	#return t

def t_RT(t) :
	r'^[R][T]'
	#print("Rt")
	return t

def t_HASHTAG(t) :
	r'\#[A-Za-z0-9_]+'
	#print("hash")
	return t

def t_SNAME(t) :
	r'\@.*?\s'
	#print("sname")
	return t

def t_EMOP(t) :
	r'([\:\;][PpdD\)\*])|(\^\_\^)'
	#print("emo positive")
	global d
	d.append("happy")
	return t

def t_EMON(t):
	r'\:\('
	global d
	d.append("sad")
	#print("Emo negative")
	return t

def t_URL(t) :
	r'http:\/\/.*\s'
	#print("url")
	return t

def t_SLANG(t) :
	r'[Rr][Oo][Ff][Ll]|[Ll][Oo][Ll]'
#	r'Rofl|rofl|lol'
	global d
	d.append(t.value)
	#print("slang")
	return t

def t_NUMBER(t) :
	r'\d+'
	#print("num")
	return t

def t_WORD(t) :
	r'\w+'
	global d
	d.append(t.value)
	#print("Word")
	return t

def t_PUNC(t):
	r'[\?\!\&\$\%\@\)\(\,\.\;\_\-\:\+\=\^\#\|\/]'
	#print("Punc")

def t_DQ(t):
	r'\"'
	#print("DQ")
	return t

def t_SQ(t):
	r"\'"
	#print("SQ")
	return t

	
t_ignore = ' \t\n'

def t_error(t):
	print("Error")
	

datafile=open("training_tweets.txt", "r");
tweets1=datafile.read()
tweets1=tweets1.split("\n")
tweets1= [ tweet.strip() for tweet in tweets1 ]
tweets1= [ re.sub(r'[^\x00-\x7F]+',' ', tweet) for tweet in tweets1 ]

tweet_set=[]
for i in tweets1:
	#i.strip("\n")
	#i.strip(' ')
	lexer = lex.lex()
	lexer.input(i)
	d=[]
	for t in lexer:
		pass
	tweet_set.append(d)


# Preprocessing of tweets :: Input is an list of lists which comes after PLY

def text_normalize(all_tweets):
	all_index=0
	min_length = 2
	lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
	for tweet in all_tweets:
		index=0
		for word in tweet:
			preproc_word = word.lower()
			if (not preproc_word in stopwords.words('english') and len(preproc_word) >= min_length):
				preproc_word = lmtzr.lemmatize(preproc_word)
			else:
				tweet.remove(word)
				continue
			tweet[index] = preproc_word
			index  = index + 1
		all_tweets[all_index] = tweet
		all_index = all_index + 1
	return all_tweets

all_tweets = text_normalize(tweet_set)

# Function to calculate argmax
def argmax(tweet):
	#NOT_IN_CLASS=1.0
	global vocab;
	global result;
	NOT_IN_VOCAB=1.0/(len(vocab)+1);
	prob_p=1;
	prob_n=1;
	prob_nu=1;
	for word in tweet:
		if word in result:
			prob_p=prob_p*result[word][0]
			prob_n=prob_p*result[word][1]
			prob_nu=prob_p*result[word][2]
		else:
			prob_p=NOT_IN_VOCAB
			prob_nu=NOT_IN_VOCAB
			prob_n=NOT_IN_VOCAB
	prob_p=prob_p*p_probability
	prob_n=prob_n*n_probability
	prob_nu=prob_nu*nu_probability
	prob=[prob_p,prob_n,prob_nu];
	val={0:"p",1:"n",2:"nu"}
	return val[prob.index(max(prob))]



# Calculate probabilities of each class. 

class_probability_file = open("training_sentiment","r")

all = class_probability_file.read()
class_count = all.split("\n")
class_count = [ emotion.strip() for emotion in class_count ]


p_count = 0
n_count = 0
nu_count = 0
total_count = 0

p_tweets = []
n_tweets = []
nu_tweets = []


for emotion in class_count:
		if emotion != "" :
			
			if emotion == "p":
				p_count = p_count + 1
				p_tweets.append(all_tweets[total_count]) 
			elif emotion == "n":
				n_count = n_count + 1
				n_tweets.append(all_tweets[total_count]) 
			elif emotion == "nu":
				nu_count = nu_count + 1
				nu_tweets.append(all_tweets[total_count]) 
		total_count = total_count + 1

print("P_count"+str(p_count))
print("N_count"+str(n_count))
print("NU_count"+str(nu_count))

p_probability = p_count/(total_count*1.0)
n_probability = n_count/(total_count*1.0)
nu_probability = nu_count/(total_count*1.0)

class_probability_file.close()


print("Positive"+str(p_probability))
print("Negative"+str(n_probability))
print("Neutral"+str(nu_probability))


vocab = p_tweets + n_tweets + nu_tweets
vocab = [ word for tweet in vocab for word in tweet ]
vocab = list(set(vocab))

p_tweets=[ word for tweet in p_tweets for word in tweet ]
n_tweets=[ word for tweet in n_tweets for word in tweet ]
nu_tweets=[ word for tweet in nu_tweets for word in tweet ]

result={}

for i in vocab:
		values=[];
		values.append(p_tweets.count(i));
		values.append(n_tweets.count(i));
		values.append(nu_tweets.count(i));
		values.append(sum(values))
		prob=[]
		prob.append((values[0]+1)/(values[3]+len(vocab)*1.0))
		prob.append((values[1]+1)/(values[3]+len(vocab)*1.0))
		prob.append((values[2]+1)/(values[3]+len(vocab)*1.0))
		result[i]=prob


test_file=open("test.txt","r")


test_sentiment_file=open("test_sentiment","r")
test_sentiment=test_sentiment_file.read()
test_sentiment= test_sentiment.split("\n")
test_sentiment = [ sentiment.strip() for sentiment in test_sentiment]

tweets2=test_file.read()
tweets2=tweets2.split("\n")
tweets2= [ tweet.strip() for tweet in tweets2 ]
tweets2= [ re.sub(r'[^\x00-\x7F]+',' ', tweet) for tweet in tweets2 ]

tweet1_set=[]
for i in tweets2:
	#i.strip("\n")
	#i.strip(' ')
	lexer = lex.lex()
	lexer.input(i)
	d=[]
	for t in lexer:
		pass
	tweet1_set.append(d)


tweet1_set = text_normalize(tweet1_set)

count=0

index=0
for i in tweet1_set:
	sentiment_class=argmax(i)
	#print(sentiment_class)
	if(sentiment_class==test_sentiment[index]):
		count=count+1

print("accuracy= "+str((count*100.0)/(len(tweets2)*1.0)));




		




