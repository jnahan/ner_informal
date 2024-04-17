from collections import defaultdict
import numpy as np

likelihood = defaultdict(lambda: defaultdict(int))
transition = defaultdict(lambda: defaultdict(int))
words = set()
wordCounts = defaultdict(lambda:0)
prev = 'Begin_Sent'

#training stage
file = open('training.words', 'r')
for line in file:
    if line=='\n':
        transition['End_Sent'][prev] += 1
        prev = 'Begin_Sent'
        continue
    word = line.strip()
    if word.istitle():
        pos = 'capitalized'
    else:
        pos = 'uncapitalized'
    word = word.lower()
    words.add(word)
    wordCounts[word] += 1
    likelihood[pos][word] += 1
    transition[prev][pos] += 1
    prev = pos

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

for prev in transition:
    total = sum(transition[prev].values())
    for pos in transition[prev]:
        transition[prev][pos] = transition[prev][pos] / total

sentence = []
tags = list(transition.keys())
tags[tags.index('End_Sent')] = tags[len(tags)-1]
tags[len(tags)-1] = 'End_Sent'

# #transducer, probability calculator
file = open('test.words', 'r')
for line in file:
    if line != '\n':
        line = line.strip()
        sentence.append(line)
    else:
        res = [None] * (len(sentence)+2)
        res[0] = ['Begin_Sent']
        res[len(sentence)+1] = ['End_Sent']
        viterbi = [[0 for i in range(len(sentence)+2)] for j in range(len(tags))]
        viterbi[0][0] = 1
        viterbi[len(tags)-1][len(sentence)+1] = 1
        for j in range (1, len(sentence) + 1):
            for i in range (len(tags)):
                for k in range (len(tags)):
                    currWord = sentence[j-1]
                    currTag = tags[i]
                    prevTag = tags[k]
                    currTransition = transition[prevTag][currTag]
                    #handle oov using unknown word
                    currLikelihood = likelihood[currTag]["Unknown_Word"]
                    #handle oov using transition
                    if prevTag == "Begin_Sent" and currWord[0].islower() and currTag == 'capitalized':
                        currLikelihood = 1
                    #known words
                    if (currWord in words):
                        currLikelihood = likelihood[currTag][currWord]
                    viterbi[i][j] = max(viterbi[i][j], viterbi[k][j-1]*currTransition*currLikelihood)
        #get index of max val in each column (most likely pos)
        viterbi = np.array(viterbi)
        maxInd = list(np.argmax(viterbi, axis=0))
        #write results in output file
        res = open("submission.pos", 'a')
        for i in range(len(sentence)):
            res.write(sentence[i] + "\t" + tags[maxInd[i+1]] + "\n")
        res.write("\n")
        res.close()
        sentence = []