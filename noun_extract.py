# function to extract nouns from an input string using NLTK
# input - each movie description
# output - text file of nouns

import nltk

def extract_nouns(line):
	f_out = open("noun_file.txt", 'a')
	text = nltk.word_tokenize(line)
	tag = nltk.pos_tag(text)
	accepted = ['NN', 'NNS', 'NNP']
	print tag
	for item in tag:
		if item[1] in accepted : f_out.write(item[0] + '\n')

	f_out.close()
extract_nouns("the balls rolled up the hill")
extract_nouns("the turtle got his redemption on Thursday in Germany")