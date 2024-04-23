#!/usr/bin/python
#
# scorer for NLP class Spring 2016
# ver.1.0
#
# score a key file against a response file
# both should consist of lines of the form:   token \t tag
# sentences are separated by empty lines
#
import sys
import os

#python3 truecaser/testing/score.py truecaser/testing/answers.words truecaser/testing/submission.pos

def score (keyFileName, responseFileName):
	incorrect_list = open("truecaser/testing/incorrect.pos", 'w')
	incorrect_list.write('')
	incorrect_list.close()

	keyFile = open(keyFileName, 'r')
	key = keyFile.readlines()
	responseFile = open(responseFileName, 'r')
	response = responseFile.readlines()
	if len(key) != len(response):
		print("length mismatch between key and submitted file")
		exit()
	correct = 0
	incorrect = 0
	correct_is_title = 0
	correct_is_lower = 0
	for i in range(len(key)):
		key[i] = key[i].rstrip(os.linesep)
		response[i] = response[i].rstrip(os.linesep)
		if key[i] == "":
			if response[i] == "":
				continue
			else:
				print ("sentence break expected at line " + str(i))
				exit()
		keyFields = key[i].split('\t')
		if len(keyFields) != 2:
			print ("format error in key at line " + str(i) + ":" + key[i])
			exit()
		keyToken = keyFields[0]
		keyPos = keyFields[1]
		responseFields = response[i].split('\t')
		if len(responseFields) != 2:
			print ("format error at line " + str(i))
			exit()
		responseToken = responseFields[0]
		responsePos = responseFields[1]
		if responseToken != keyToken:
			print ("token mismatch at line " + str(i))
			exit()

		if responsePos == keyPos:
			correct = correct + 1
		elif responsePos != keyPos:
			incorrect = incorrect + 1

			if keyPos == "title case":
				correct_is_title += 1
			elif keyPos == "lowercase":
				correct_is_lower += 1

			incorrect_list = open("truecaser/testing/incorrect.pos", 'a')
			incorrect_list.write('line ' + str(i) + '\n')
			incorrect_list.write('answer: ' + keyToken.strip() + '  ' + keyPos.strip() + '\n')
			incorrect_list.write('response: ' + responseToken.strip() + '  ' + responsePos.strip() + '\n\n')

			print('answer: ' + keyToken.strip() + '  ' + keyPos.strip())
			print('response: ' + responseToken.strip() + '  ' + responsePos.strip())
			print('')
	print (str(correct) + " out of " + str(correct + incorrect) + " tags correct")
	accuracy = 100.0 * correct / (correct + incorrect)
	print("  accuracy: %f" % accuracy)
	print ("incorrect, answer was supposed to be title: " + str(correct_is_title))
	print ("incorrect, answer was supposed to be lower: " + str(correct_is_lower))

def main(args):
	key_file = args[1]
	response_file = args[2]
	score(key_file,response_file)

if __name__ == '__main__': sys.exit(main(sys.argv))
