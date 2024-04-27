import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
import re

nltk.download('gutenberg')
nltk.download('punkt')

emma = gutenberg.raw('austen-emma.txt')[27:]
tokens = word_tokenize(emma)
with open('truecaser/emma.words','w') as file:
    for token in tokens:
        file.write(token+'\n')
        if token in {'.', '?', '!'}:
            file.write('\n')

moby = gutenberg.raw('melville-moby_dick.txt')
chapter_pattern = re.compile(r"CHAPTER 1|Chapter 1|chapter 1", re.IGNORECASE)
match = chapter_pattern.search(moby)
moby = moby[match.start():]
tokens = word_tokenize(moby)
with open('truecaser/moby.words','w') as file:
    for token in tokens:
        file.write(token+'\n')
        if token in {'.', '?', '!'}:
            file.write('\n')

persuasion = gutenberg.raw('austen-persuasion.txt')[33:]
tokens = word_tokenize(persuasion)
with open('truecaser/persuasion.words','w') as file:
    for token in tokens:
        file.write(token+'\n')
        if token in {'.', '?', '!'}:
            file.write('\n')

parents = gutenberg.raw('edgeworth-parents.txt')[47:]
tokens = word_tokenize(parents)
with open('truecaser/parents.words','w') as file:
    for token in tokens:
        file.write(token+'\n')
        if token in {'.', '?', '!'}:
            file.write('\n')

alice = gutenberg.raw('carroll-alice.txt')[57:]
tokens = word_tokenize(alice)
with open('truecaser/alice.words','w') as file:
    for token in tokens:
        file.write(token+'\n')
        if token in {'.', '?', '!'}:
            file.write('\n')
