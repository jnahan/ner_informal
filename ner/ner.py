#https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/
# spacy, nltk, stanford

# import spacy 

# nlp = spacy.load('en_core_web_sm') 
# sentence = "apple is looking at buying U.K. startup for $1 billion"
# doc = nlp(sentence) 
# for ent in doc.ents: 
#     print(ent.text, ent.start_char, ent.end_char, ent.label_) 

import truecase
import nltk

sample_text = "HAPPY BIRTHDAY AHYEON 💜🖤 I LOVE YOU AND BE YOUR FAN FROM FIRST DAYH I SAW YOU ON BABYMONSTER PAGE !! Unnie will always support you  🤍"
capitalized_text = truecase.get_true_case(sample_text)

# tokens = nltk.word_tokenize(sample_text)
tokens = nltk.word_tokenize(capitalized_text)
tagged_tokens = nltk.pos_tag(tokens)
entities = nltk.ne_chunk(tagged_tokens)
print(entities)
