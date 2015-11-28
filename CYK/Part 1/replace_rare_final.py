'''
Input : Original Count file
Output : Modifies the training dataset and replaces rare terminals with _RARE_
'''


import re
# Function to replace all the rare terminals with _RARE_
def replace_rare(filename):
	global list_rare
	input_file = file(filename,"r")
	file_contents = input_file.read()
	for word in list_rare:
		file_contents = re.sub('''"'''+re.escape(word)+'''"''','''"_RARE_"''',file_contents)
	output_file = file(filename,"w")
	output_file.write(file_contents)


# Function to find the rare words
def find_rare(filename):

	#Dict to hold all the terminals along with their respective counts
	terminals_freq={}
	input_file = file(filename,"r") 
	all = input_file.read()
	lines = all.split("\n")
	lines[:]= [ line for line in lines if line!="" ]
	#List which contains all the terminals whose count is less than 5
	list_rare = []
	for line in lines:
		line=line.strip().split(" ")
		if(line[1] == "UNARYRULE"):
			if(line[3] in terminals_freq):
				terminals_freq[line[3]]  = terminals_freq[line[3]] + int(line[0])
			else:
				terminals_freq[line[3]] = int(line[0])
	keys = terminals_freq.keys()
	for key in keys:
		if(terminals_freq[key]<5):
			list_rare.append(key)
			
	return list_rare


list_rare = find_rare("cfg.counts")
replace_rare("parse_train.dat")

