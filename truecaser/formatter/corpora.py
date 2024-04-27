import nltk
from nltk.corpus import gutenberg
import re
import spacy
from nltk.tokenize.treebank import TreebankWordDetokenizer

nlp = spacy.load("en_core_web_sm") 
nlp.max_length = 1500000
nltk.download('gutenberg')

sentences = []
sentence = []
with open("truecaser/training/training.words",'r') as file:
    for line in file:
        if line=='\n':
            sentences.append(TreebankWordDetokenizer().detokenize(sentence))
            sentence = []
        else:
            sentence.append(line.strip())

with open("truecaser/training/training.words",'w') as file:
    for sentence in sentences:
        doc = nlp(sentence)
        for token in doc:
            file.write(token.text+"\n")
        file.write("\n")

emma = gutenberg.raw('austen-emma.txt')[27:]
tokens = nlp(emma)
with open('truecaser/training/emma.words','w') as file:
    for token in tokens:
        if token.text=="\n":
            continue
        text = token.text.strip()
        file.write(text+'\n')

moby = gutenberg.raw('melville-moby_dick.txt')
chapter_pattern = re.compile(r"CHAPTER 1|Chapter 1|chapter 1", re.IGNORECASE)
match = chapter_pattern.search(moby)
moby = moby[match.start():]
tokens = nlp(moby)
with open('truecaser/training/moby.words','w') as file:
    for token in tokens:
        text = token.text.replace('\n', '').strip()
        if text == "":
            continue
        file.write(text + '\n')
        if text in {'.', '?', '!'}:
            file.write('\n')

persuasion = gutenberg.raw('austen-persuasion.txt')[33:]
tokens = nlp(persuasion)
with open('truecaser/training/persuasion.words','w') as file:
    for token in tokens:
        if token.text=="\n":
            continue
        text = token.text.strip()
        file.write(text+'\n')

parents = gutenberg.raw('edgeworth-parents.txt')[47:]
tokens = nlp(parents)
with open('truecaser/training/parents.words','w') as file:
    for token in tokens:
        text = token.text.replace('\n', '').strip()
        if text == "":
            continue
        file.write(text + '\n')
        if text in {'.', '?', '!'}:
            file.write('\n')

alice = gutenberg.raw('carroll-alice.txt')[57:]
tokens = nlp(alice)
with open('truecaser/training/alice.words','w') as file:
    for token in tokens:
        text = token.text.replace('\n', '').strip()
        if text == "":
            continue
        file.write(text + '\n')
        if text in {'.', '?', '!'}:
            file.write('\n')
