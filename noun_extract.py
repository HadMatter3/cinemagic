# function to extract nouns from an input string using NLTK
# input - each movie description
# output - text file of nouns

import nltk
def extract_nouns(line):
	f_out = open("noun_file.txt", 'a')
	text = nltk.word_tokenize(line)
	tag = nltk.pos_tag(text)
	accepted = ['NN', 'NNS', 'NNP']
	return_list = []
	for item in tag:
		if item[1] in accepted : return_list.append(item[0])

	f_out.close()
	return return_list
