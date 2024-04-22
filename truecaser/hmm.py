from collections import defaultdict
import numpy as np
import string
import math

# TODOS
# recognize if all word in sentence are capitalized (training, ex for titles)
# get a list of words that commonly precede/follow title cases
    # Inc Corp
# optimize trigram
    # currently causing some words to be incorrectly tagged title case
    # missing some words
# consider common prefixes suffixes (ness, ingm etc,)
# tag urls (http/https/www, etc as lowercase)
# update code to produce properly capitalized sentences rather than the tags
# maybe remove uppercase (try to tag those properly instead)

#curr accuracy: 95.899918

likelihood = defaultdict(lambda: defaultdict(int))
transition = defaultdict(lambda: defaultdict(int))
transition_probabilities = defaultdict(lambda: defaultdict(float))
words = set()
wordCounts = defaultdict(lambda:0)
prev = ('Begin_Sent','Begin_Sent')

# common_words = open('truecaser/google-non-upper.words', 'r').read()
# words_list = common_words.split("\n")

lower = open('truecaser/lower.words', 'r').read()
lower_list = lower.split("\n")

title = open('truecaser/title.words', 'r').read()
title_list = title.split("\n")

suffix = open("truecaser/suffix.end",'r').read()
suffix_list = suffix.split("\n")

follow = open("truecaser/follow.words",'r').read()
follow_list = follow.split("\n")

#training stage
training_files = ['alice.words', 'emma.words', 'moby.words', 'parents.words', 'persuasion.words', 'training.words']
for training in training_files:
    file = open('truecaser/training/'+training, 'r')
    for line in file:
        if line=='\n':
            transition[prev]['End_Sent'] += 1
            transition[prev[1]]['End_Sent']+=1
            prev = ('Begin_Sent','Begin_Sent')
            continue
        word = line.strip()
        if word in string.punctuation:
            pos = 'punctuation'
        elif word[0].isnumeric():
            pos = 'number'
        elif word.istitle():
            if prev[1]=='Begin_Sent':
                pos = 'uppercase'
            else:
                pos = 'title case'
        else:
            pos = 'lowercase'
        word = word.lower()
        words.add(word)
        wordCounts[word] += 1
        likelihood[pos][word] += 1
        transition[prev][pos] += 1
        transition[prev[1]][pos]+=1
        prev = (prev[1],pos)

unknownWords = [k for k, v in wordCounts.items() if v == 1]
for unknown in unknownWords:
    words.remove(unknown)

for pos, word in likelihood.items():
    for unknown in unknownWords:
        if unknown in word:
            word['Unknown_Word'] += 1
            del word[unknown]

for pos in likelihood:
    total = sum(likelihood[pos].values())
    for word in likelihood[pos]:
        likelihood[pos][word] = likelihood[pos][word] / total

for t in transition:
    total = sum(transition[t].values())
    for state in transition[t]:
        transition_probabilities[t][state] = transition[t][state] / total

sentence = []
tags = ['Begin_Sent', 'title case', 'uppercase', 'lowercase', 'End_Sent', 'punctuation', 'number', 'other']
tags[tags.index('End_Sent')] = tags[len(tags)-1]
tags[len(tags)-1] = 'End_Sent'

first_word = True
#transducer, probability calculator

res = open("truecaser/submission.pos", 'w')
res.write('')
res.close()


file = open('truecaser/test.words', 'r')
for line in file:
    if line != '\n':
        line = line.strip()
        sentence.append(line)
        first_word = True
    else:
        res = [None] * (len(sentence)+2)
        res[0] = ['Begin_Sent']
        res[len(sentence)+1] = ['End_Sent']
        viterbi = [[[0 for _ in range(len(tags))] for _ in range(len(tags))] for _ in range(len(sentence)+2)]
        viterbi[0][0][0] = 1
        viterbi[len(sentence)+1][len(tags)-1][len(tags)-1] = 1
        for j in range (1, len(sentence) + 1): ##curr word
            for i in range (len(tags)): #curr tag
                for k in range (len(tags)): #prev tag
                    for t in range(len(tags)): #prev2 tag
                        currWord = sentence[j-1]
                        currTag = tags[i]
                        prevTag = tags[k]
                        prev2Tag = tags[t]
                        currTransition = transition_probabilities[(prev2Tag,prevTag)][currTag]*math.pow(transition_probabilities[prevTag][currTag],1 if j==1 else likelihood[prevTag][sentence[j-2]])
                        #handle oov using unknown word
                        currLikelihood = likelihood[currTag]["Unknown_Word"]
                        #known words
                        if (currWord in words):
                            currLikelihood = likelihood[currTag][currWord]
                        if (currWord in string.punctuation): 
                            if (currTag == "punctuation"):
                                currLikelihood = 1
                        elif (currWord[0].isnumeric()):
                            if (currTag == "number"):
                                currLikelihood = 1
                        elif (not currWord[0].isalnum()):
                            if (currTag == "other"):
                                currLikelihood = 1
                        elif (first_word):
                            if (currTag == "uppercase"):
                                currLikelihood = 1
                        
                        viterbi[j][i][k] = max(viterbi[j][i][k], viterbi[j-1][k][t]*currTransition*currLikelihood)
            first_word = False
        #get index of max val in each column (most likely pos)
        viterbi = np.array(viterbi)
        maxInd = []
        for i in range(len(viterbi)):
            max_prob_per_tag = np.max(viterbi[i], axis=1)
            maxInd.append(np.argmax(max_prob_per_tag))
        #write results in output file
        res = open("truecaser/submission.pos", 'a')
        for i in range(len(sentence)):
            tag = tags[maxInd[i+1]]
            word = sentence[i]
            if word in string.punctuation:
                tag = 'punctuation'
            elif word[0].isnumeric():
                tag = 'number'
            elif not word[0].isalnum():
                tag = 'other'
            #handle oov -> set it to title if its not in list of
            #common lowercase words
            elif ("-" in word):
                if (tag != "uppercase"):
                    tag = "lowercase"
            elif (i<len(sentence)-1 and sentence[i+1] in follow_list):
                tag = "title case"
            elif (word not in words):
                if (word not in lower_list):
                    if (tag != "uppercase"):
                        tag = "title case"
                elif any(word.endswith(suffix) for suffix in suffix_list):
                    if (tag != "uppercase"):
                        tag = "lowercase"
            res.write(sentence[i] + "\t" + tag + "\n")
        res.write("\n")
        res.close()
        sentence=[]