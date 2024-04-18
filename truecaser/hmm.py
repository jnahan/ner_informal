from collections import defaultdict
import numpy as np
import string

likelihood = defaultdict(lambda: defaultdict(int))
transition = defaultdict(lambda: defaultdict(int))
transition_probabilities = defaultdict(lambda: defaultdict(float))
words = set()
wordCounts = defaultdict(lambda:0)
prev = ('Begin_Sent','Begin_Sent')

#training stage
file = open('truecaser/training.words', 'r')
for line in file:
    if line=='\n':
        transition['End_Sent'][prev] += 1
        prev = ('Begin_Sent','Begin_Sent')
        continue
    word = line.strip()
    if word in string.punctuation:
        pos = 'punctuation'
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
tags = ['Begin_Sent', 'title case', 'uppercase', 'lowercase', 'End_Sent', 'punctuation']
tags[tags.index('End_Sent')] = tags[len(tags)-1]
tags[len(tags)-1] = 'End_Sent'

first_word = True
#transducer, probability calculator
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
                        currTransition = transition_probabilities[(prev2Tag,prevTag)][currTag]
                        #handle oov using unknown word
                        currLikelihood = likelihood[currTag]["Unknown_Word"]
                        #known words
                        if (currWord in words):
                            currLikelihood = likelihood[currTag][currWord]
                        if (first_word and currTag == "uppercase"):
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
            res.write(sentence[i] + "\t" + tags[maxInd[i+1]] + "\n")
        res.write("\n")
        res.close()
        sentence=[]
