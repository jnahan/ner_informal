#https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/
# spacy, nltk, stanford

import spacy 
nlp = spacy.load('en_core_web_sm') 

import nltk
from collections import defaultdict

def tokenize_nltk(path):
    file = open("ner/testing/"+path, "r")
    tokens = nltk.word_tokenize(file.read())
    tagged_tokens = nltk.pos_tag(tokens)
    entities = nltk.ne_chunk(tagged_tokens)
    lines = str(entities).split('\n')

    tags = defaultdict(int)
    res = open("ner/nltk/"+path, "w")
    for line in lines:
        line = line.strip()
        if (line[0] == "(" and line != "(/(" and line != "(S"):
            res.write(line+"\n")
            split_line = line.strip('()').split(" ")
            tag = split_line[0]
            # word = ''.join(map(str, split_line[2:]))
            tags[tag]+=1

    file.close()
    res.close()
    print(path)
    print(tags)
    print("\n")

tokenize_nltk("formatted.lower.words")
tokenize_nltk("formatted.truecased.words")
tokenize_nltk("formatted.original.words")


def tokenize_spacy(path):
    file = open("ner/testing/"+path, "r")
    doc = nlp(file.read()) 

    tags = defaultdict(int)
    res = open("ner/spacy/"+path, "w")
    for ent in doc.ents:
        res.write(ent.text + "\t" + ent.label_ + "\n")
        tags[ent.label_]+=1

    file.close()
    res.close()
    print(path)
    print(tags)
    print("\n")

tokenize_spacy("formatted.lower.words")
tokenize_spacy("formatted.truecased.words")
tokenize_spacy("formatted.original.words")
