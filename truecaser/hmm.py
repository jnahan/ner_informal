from collections import defaultdict
import numpy as np
import string
import math
import re

# TODOS
# recognize if all word in sentence are capitalized (training, ex for titles)
# optimize trigram
    # currently causing some words to be incorrectly tagged title case
    # missing some words
# update code to produce properly capitalized sentences rather than the tags
# maybe remove uppercase (try to tag those properly instead)

#curr accuracy: 96.058199

"""
likelihood - dictionary that stores likelihood of word being tagged pos (likelihood[pos][word]), trained on training data

transition - dictionary that stores how often, in training data, there exists transitioning from the previous tag to the current tag and the 
transitioning from the previous two tags to the current tag

transition_probabilities - dictionary that stores the probability of transitioning from the previous tag to the current tag and
the probability of transitioning from the previous two tags to the current tag in training data

words - hashset of all words that appeared in training data

wordCounts - dictoinary that maps a word to the number of times the word appeared in the training data

prev - a tuple that stores the previous two tags
"""
likelihood = defaultdict(lambda: defaultdict(int))
transition = defaultdict(lambda: defaultdict(int))
transition_probabilities = defaultdict(lambda: defaultdict(float))
words = set()
wordCounts = defaultdict(lambda:0)
prev = ('Begin_Sent','Begin_Sent')

with open('truecaser/lower.words', 'r') as lower_file:
    lower = lower_file.read()
#stores a list of common words that are not named entities
lower_list = lower.split("\n")

with open('truecaser/title.words', 'r') as title_file:
    title = title_file.read()
#stores a list of common words that are named entities
title_list = title.split("\n")

with open("truecaser/suffix.end",'r') as suffix_file:
    suffix = suffix_file.read()
#stores a list of common suffixes for words that are not named entities
suffix_list = suffix.split("\n")

with open("truecaser/follow.words",'r') as follow_file:
    follow = follow_file.read()
#stores a list of common words that follow a named entity
follow_list = follow.split("\n")

with open("truecaser/prevne.words",'r') as prev_file:
    prev = prev_file.read()
#stores a list of common words that precede a named entity
prev_list = prev.split("\n")

#training stage
training_files = ['alice.words', 'emma.words', 'moby.words', 'parents.words', 'persuasion.words', 'training.words']
for training in training_files:
    file = open('truecaser/training/'+training, 'r')
    for line in file:
        #check if we have reached the end of the sentence
        if line=='\n':
            #update transitions to the end of sentence
            transition[prev]['End_Sent'] += 1
            transition[prev[1]]['End_Sent']+=1
            prev = ('Begin_Sent','Begin_Sent')
            continue
        word = line.strip()
        #pretag certain words: punctuations and numbers
        if word in string.punctuation:
            pos = 'punctuation'
        elif word[0].isnumeric():
            pos = 'number'
        #for other words: uppercase tag = words at start of sentence, title case = named entities, lowercase = everything else
        elif word.istitle():
            if prev[1]=='Begin_Sent':
                pos = 'uppercase'
            else:
                pos = 'title case'
        else:
            pos = 'lowercase'
        
        #normalize all words to lowercase before adding to words, update dictionaries accordingly
        word = word.lower()
        words.add(word)
        wordCounts[word] += 1
        likelihood[pos][word] += 1
        transition[prev][pos] += 1
        transition[prev[1]][pos]+=1
        prev = (prev[1],pos)

file.close()

#unknownWords - stores a list of all words that only appear once in training corpus
unknownWords = [k for k, v in wordCounts.items() if v == 1]
#remove all unknown words from our set of words that appear in training data
for unknown in unknownWords:
    words.remove(unknown)

#update likelihood to reflect new unknown words
for pos, word in likelihood.items():
    for unknown in unknownWords:
        #replace all instances of "unknown" words in likelihood dictionary with an all encompassing "Unknown_Word" tag
        if unknown in word:
            word['Unknown_Word'] += 1
            del word[unknown]

#Calculate the probability of a word being tagged with a specific part of speech (POS) relative
# to the frequency of all other words tagged with the same POS
for pos in likelihood:
    total = sum(likelihood[pos].values())
    for word in likelihood[pos]:
        likelihood[pos][word] = likelihood[pos][word] / total

#Calculate the probability of transitioning from a previous tag/tuple of tags to the current tag
#relative to the frequency of transitioning from the same previous tag/tuple of tags to any other tag
#stored in transition_probabilities
for t in transition:
    total = sum(transition[t].values())
    for state in transition[t]:
        transition_probabilities[t][state] = transition[t][state] / total

#sentence - stores the current sentence in the test data
sentence = []
tags = ['Begin_Sent', 'title case', 'uppercase', 'lowercase', 'End_Sent', 'punctuation', 'number', 'other']
#reorders list of tags so that the 'End_Sent' tag is at the end
tags[tags.index('End_Sent')] = tags[len(tags)-1]
tags[len(tags)-1] = 'End_Sent'

#boolean to track whether or not current word is the first word in the sentence
first_word = True

#clear out previous data in the submission.pos file 
res = open("truecaser/submission.pos", 'w')
res.write('')
res.close()

def is_url(url):
    #check if url starts with http:// or https://
    if re.match(r"^https?://", url, re.IGNORECASE):
        return True
    #check if url starts with www.
    elif re.match(r"^www\.", url, re.IGNORECASE):
        return True
    #check if url ends with common domain extensions
    elif re.search(r"\.(com|net|org|edu|gov|co|io|info|biz)", url, re.IGNORECASE):
        return True
    return False

#truecaser/test.words = test data
file = open('truecaser/test.words', 'r')
#loop through test data
for line in file:
    #if word is part of ongoing sentence
    if line != '\n':
        line = line.strip()
        sentence.append(line)
        first_word = True
    #if sentence has ended
    else:
        #set up viterbi table, initalizing probability of 1 for "Begin_Sent" and "End_Sent"
        viterbi = [[[0 for _ in range(len(tags))] for _ in range(len(tags))] for _ in range(len(sentence)+2)]
        viterbi[0][0][0] = 1 #index of 0 = begin_sent (index of begin_sent in tags array)
        viterbi[len(sentence)+1][len(tags)-1][len(tags)-1] = 1 #index of len(tags)-1 = end_sent (index of end_sent in tags array)

        for j in range (1, len(sentence) + 1): ##curr word
            for i in range (len(tags)): #curr tag
                for k in range (len(tags)): #prev tag
                    for t in range(len(tags)): #prev2 tag
                        #current word of the sentence
                        currWord = sentence[j-1]
                        #current tag
                        currTag = tags[i]
                        #previous tag
                        prevTag = tags[k]
                        #tag before previous tag
                        prev2Tag = tags[t]
                        #calculate probability of transitioning from previous two tags to current tag multipled by the probability of transitioning from 
                        #previous tag to current tag, weighed by the probability of the previous word in the sentence being tagged the previous tag
                        currTransition = transition_probabilities[(prev2Tag,prevTag)][currTag]*math.pow(transition_probabilities[prevTag][currTag],1 if j==1 else likelihood[prevTag][sentence[j-2]])
                        #handle oov using unknown word
                        currLikelihood = likelihood[currTag]["Unknown_Word"]
                        #known words
                        if (currWord in words):
                            currLikelihood = likelihood[currTag][currWord]
                        
                        #hard code likelihood of one for special cases:
                        #if the word is a punctuation
                        if (currWord in string.punctuation): 
                            if (currTag == "punctuation"):
                                currLikelihood = 1
                        #if the word is a number
                        elif (currWord[0].isnumeric()):
                            if (currTag == "number"):
                                currLikelihood = 1
                        #if the word consists of special characters
                        elif (not currWord[0].isalnum()):
                            if (currTag == "other"):
                                currLikelihood = 1
                        #if the word is the first word in the sentence
                        elif (first_word):
                            if (currTag == "uppercase"):
                                currLikelihood = 1
                        #update viterbi accordingly
                        viterbi[j][i][k] = max(viterbi[j][i][k], viterbi[j-1][k][t]*currTransition*currLikelihood)
            first_word = False

        viterbi = np.array(viterbi)
        #get index of max val in each column (most likely pos)
        maxInd = []
        for i in range(len(viterbi)):
            #calculates highest probability for transitioning from any previous state to each current state
            max_prob_per_tag = np.max(viterbi[i], axis=1)
            #appends the index of the current state with the highest transition probability at time step `i`
            maxInd.append(np.argmax(max_prob_per_tag))
        
        #write results in output file
        res = open("truecaser/result.words", 'a')
        for i in range(len(sentence)):
            #tag that word is most likely to be
            tag = tags[maxInd[i+1]]
            word = sentence[i]
            #hard code tag for special cases:
            #if word is a punctuation
            if word in string.punctuation:
                tag = 'punctuation'
            #if word is a number
            elif word[0].isnumeric():
                tag = 'number'
            #if word consists of special characters
            elif not word[0].isalnum():
                tag = 'other'
            #if word constains a hyphen, based on the fact that most words (in corpora) with hyphens are not named entities
            elif ("-" in word):
                if (tag != "uppercase"):
                    tag = "lowercase"
            #if word is preceded by a word that commonly precedes named entities or followed by a word that commonly follows named entities
            elif ((i<len(sentence)-1 and sentence[i+1] in follow_list) or (i>0 and sentence[i-1] in prev_list)):
                if (tag != "uppercase"):
                    tag = "title case"
            #handle oov
            elif (word not in words):
                #set it to title if it is a username
                if (word.startswith("@") and len(word) > 3):
                    tag = "title case"
                #set it to lowercase if it is a url
                elif (is_url(word)):
                    tag = "lowercase"
                #set it to lowercase if word is not the first word in the sentence and ends with a suffix that is rarely found in named entities
                elif any(word.endswith(suffix) for suffix in suffix_list):
                    if (tag != "uppercase"):
                        tag = "lowercase"
                #set it to title if its not in list of common lowercase words
                elif (word not in lower_list):
                    if (tag != "uppercase"):
                        tag = "title case"
            #write out the word and the tag
            res.write(sentence[i] + "\t" + tag + "\n")
        res.write("\n")
        res.close()
        sentence=[]
file.close()