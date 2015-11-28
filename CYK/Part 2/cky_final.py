# Dict has key as a non-terminal and value as it's count
nonterminals_counts={}
# Dict has key as a tuple (X,terminal) and value as it's count where tuple represents rules of form X -> terminal
unary_rule_counts={}
# Dict has key as a tuple (X,Y,Z) and value as it's count where tuple represents rules of form X -> YZ
binary_rule_counts={}

# Dict which has key as a non-terminal and value is a list of tuples of form (Y,Z). Basically it records
# all the binary rules associated with a given non-terminal
binary_rules_per_terminal={}

# Consists of the non-rare terminals
nonRare = set()

#String which holds the parse tree for each sentence in json form
json=""

# This function calculates the contents of the four dict's mentioned above
def generate_counts(filename):
	countsfile=open(filename)
	#read all values
	values=countsfile.readlines();
	#print len(values)	
	for i in values:
		i=i.strip()
		line=i.split(" ")	
		#check if count of nonterminals i.e, length==3
		if(len(line)==3):
			nonterminals_counts[line[2]]=int(line[0])
		#check if count of unary rule, i.e length==4	
		elif(len(line)==4):
			nonRare.add(line[3])
			unary_rule_counts[(line[2],line[3])]=int(line[0])
		elif(len(line)==5):
			binary_rule_counts[(line[2],line[3],line[4])]=int(line[0])
			if(line[2] in binary_rules_per_terminal):
				if((line[3],line[4]) not in binary_rules_per_terminal[line[2]]):
					binary_rules_per_terminal[line[2]].append((line[3],line[4]))
			else:
				binary_rules_per_terminal[line[2]]=[(line[3],line[4])]
	nonRare.remove("_RARE_")


# Query function which takes a non-terminal as an input and returns a list of all possible binary productions' RHS
def getProductions(Nterminal):
	if(Nterminal not in binary_rules_per_terminal):
		return []
	else:
		return binary_rules_per_terminal[Nterminal]

# Function to calculate the maximum likelihood estimates as and when required.
# Input is a tuple of the form (X,terminal) in case of unary rule and of the form (X,Y,Z) in case of binary rule
def qCacl(rule):
	#unary rule
	if(len(rule)==2):
		if(rule not in unary_rule_counts):
			return 0.0
		else:
			q=unary_rule_counts[rule]*1.0/nonterminals_counts[rule[0]]*1.0
			return q
	#binary rule
	elif(len(rule)==3):
		if(rule not in binary_rule_counts):
			return 0.0
		else:
			q=binary_rule_counts[rule]*1.0/nonterminals_counts[rule[0]]*1.0
			return q
	

#This function implements the CKY algorithm as explained in slides.
# It takes a sentence is the form of a list of words and computes the required tables : pie and bp
#This function also calls another function to back propagate and generate the best parse tree.
def CKY(words):
	global json
	n = len(words)
	pie = [[{} for j in range(n+1)] for i in range(n+1)]
	bp = [[{} for j in range(n+1)] for i in range(n+1)]
	NTS=nonterminals_counts.keys()
	for i in range(1,n+1):
		for aNT in NTS:
			p_got = qCacl((aNT,words[i-1]))
			pie[i][i][aNT]= p_got
			bp[i][i][aNT]=(aNT,words[i-1])



	for span in range(1,n):
		start_range = 1 + n - span
		for start in range(1,start_range):
			end = start + span
			for split in range(start,end):
				for aNT in NTS:
					productionRHSList = getProductions(aNT)
					if(len(productionRHSList)!=0):
						for aRHS in productionRHSList:
							qProb = qCacl((aNT,aRHS[0],aRHS[1]))
							prob = qProb * pie[start][split][aRHS[0]] * pie[split+1][end][aRHS[1]] * 1.0
							if(aNT not in pie[start][end]):
								pie[start][end][aNT] = prob
								bp[start][end][aNT]=(split,aRHS[0],aRHS[1])
							elif(prob > pie[start][end][aNT]):
								pie[start][end][aNT]=prob
								bp[start][end][aNT]=(split,aRHS[0],aRHS[1])
					else:
							pie[start][end][aNT] = 0.0
	#Loop to check which is to be the start symbol based on  the last terminal
	#This is required to call function to generate best parse tree
	if(sen[-1] == "."):						
		json=""
		print_grammar(bp,1,len(sen),"S")
		outputfile.write(json+"\n")
	else:
		json=""
		print_grammar(bp,1,len(sen),"SBARQ")
		outputfile.write(json+"\n")					
								
	
# Function to generate the best parse tree
def print_grammar(bp,start,end,nt):
	global json
	if(start==end):
		json+= "[\"" +bp[start][end][nt][0]+"\", \""+ bp[start][end][nt][1] +"\"]"
		return
	
	split,nt1,nt2=bp[start][end][nt]
	json+="[\""+nt+"\", "
	print_grammar(bp,start,split,nt1)
	json+=", "
	print_grammar(bp,split+1,end,nt2)
	json +="]"
									
						
	
# Takes in the count file as well as the training dataset. 
# Filename can be replaced to test for testing dataset
generate_counts("parse_train.counts.out")
inputfile=open("parse_dev.dat")
outputfile=open("result.dat","w")

sentences=inputfile.readlines()
# If a new or rare word is encountered, replace it with _RARE_ 
for i in sentences:
	print i
	sen=i.strip().split()
	for index in range(len(sen)):
		if(sen[index] not in nonRare):
			sen[index] = "_RARE_"
	CKY(sen)
inputfile.close()
outputfile.close()




