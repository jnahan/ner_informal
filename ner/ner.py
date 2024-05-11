#https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/
# spacy, nltk, stanford

# import spacy 

# nlp = spacy.load('en_core_web_sm') 
# sentence = "apple is looking at buying U.K. startup for $1 billion"
# doc = nlp(sentence) 
# for ent in doc.ents: 
#     print(ent.text, ent.start_char, ent.end_char, ent.label_) 

import nltk

def tokenize(path):
    file = open("ner/testing/"+path, "r")
    tokens = nltk.word_tokenize(file.read())
    tagged_tokens = nltk.pos_tag(tokens)
    entities = nltk.ne_chunk(tagged_tokens)
    lines = str(entities).split('\n')
    res = open("ner/results/"+path, "w")
    for line in lines:
        line = line.strip()
        if (line[0] == "("):
            res.write(line+"\n")

    file.close()

tokenize("formatted.lower.words")
tokenize("formatted.original.words")
tokenize("formatted.truecased.words")