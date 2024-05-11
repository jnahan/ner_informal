# options
    # 1. f1 evaluation based on data we annotate by hand

    # 2. f1 evaluation with ner on original set as our baseline
        # our precision might be low

    # 3. no f1 evaluation, talk about the # of tags we recognized
        # "through preprocessing the data with our truecaser, we restored recognition of x named entities..."

# the way ners tag
    # MMS/NNP International/NNP ORGANIZATION
    # Mms/NNP   ORGANIZATION

    # OPTION 2 - correct, incorrect, partial
    # OPTION 3

    # MMS International	ORG
    # mms international	ORG
        # ner didn't recognize this org on truecased set
    # talk about groups ner didn't capture properly, trends, whys

# write about trends i notice

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
            split_line = line.strip('()').split(" ")
            tag = split_line[0]
            word = ' '.join(map(str, split_line[1:]))
            res.write(word + "\t" + tag + "\n")
            tags[tag]+=1

    file.close()
    res.close()
    print(path)
    print(tags)
    tags_count = sum(tags.values())
    print("Total tags: " + str(tags_count) + "\n")

print("-----NLTK-----")
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
    tags_count = sum(tags.values())
    print("Total tags: " + str(tags_count) + "\n")

print("-----SPACY-----")
tokenize_spacy("formatted.lower.words")
tokenize_spacy("formatted.truecased.words")
tokenize_spacy("formatted.original.words")
