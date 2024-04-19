from collections import defaultdict
import numpy as np
import string
# import nltk
# from nltk import pos_tag


#tagger to be used
# nltk.download('averaged_perceptron_tagger')

likelihood = defaultdict(lambda: defaultdict(int))
transition = defaultdict(lambda: defaultdict(int))
transition_probabilities = defaultdict(lambda: defaultdict(float))
words = set()
wordCounts = defaultdict(lambda:0)
prev = ('Begin_Sent','Begin_Sent')
all_tokenized_pos = set()

#training stage
# training_files = ['alice.words', 'emma.words', 'moby.words', 'parents.words', 'persuasion.words', 'training.words']
# for training in training_files:
file = open('truecaser/training/training.pos', 'r')
for line in file:
    if line=='\n':
        transition[prev]['End_Sent'] += 1
        prev = ('Begin_Sent','Begin_Sent')
        continue
    line = line.strip().split('\t')
    word = line[0]
    token_pos = line[1]
    if word in string.punctuation:
        pos = 'punctuation'
    elif word[0].isnumeric():
        pos = 'number'
    elif word.istitle():
        if prev[1]=='Begin_Sent':
            pos='uppercase-'+token_pos
        else:
            pos = 'title case-'+token_pos
        all_tokenized_pos.add(pos)
    else:
        pos = 'lowercase-'+token_pos
        all_tokenized_pos.add(pos)
    word = word.lower()
    words.add(word)
    wordCounts[word] += 1
    likelihood[pos][word] += 1
    transition[prev][pos] += 1
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

for bigram in transition:
    total = sum(transition[bigram].values())
    for state in transition[bigram]:
        transition_probabilities[bigram][state] = transition[bigram][state] / total

sentence = []
tags = ['Begin_Sent', 'End_Sent', 'punctuation', 'number', 'other']
for tag in all_tokenized_pos:
    tags.append(tag)
tags[tags.index('End_Sent')] = tags[len(tags)-1]
tags[len(tags)-1] = 'End_Sent'

first_word = True
#transducer, probability calculator

res = open("truecaser/submission.pos", 'w')
res.write('')
res.close()

file = open('truecaser/test.words', 'r')
for line in file:
    print(line)
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
                        currTransition = transition_probabilities[(prev2Tag,prevTag)][currTag]
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
                            if "uppercase" in currTag:
                                currLikelihood = 1
                        if (not first_word):
                            if (currTag == 'Begin_Sent'):
                                currLikelihood = 0
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
            tag = tags[maxInd[i+1]].split('-')[0] if '-' in tags[maxInd[i+1]] else tags[maxInd[i+1]]
            word = sentence[i]
            if word in string.punctuation:
                tag = 'punctuation'
            elif word[0].isnumeric():
                tag = 'number'
            elif not word[0].isalnum():
                tag = 'other'
            res.write(sentence[i] + "\t" + tag + "\n")
        res.write("\n")
        res.close()
        sentence=[]
