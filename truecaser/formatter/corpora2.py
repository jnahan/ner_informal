from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import reuters

titles = gutenberg.fileids()
with open("truecaser/training/gutenberg.words",'w') as file:
    for title in titles:
        sents = gutenberg.sents(title)
        for sent in sents:
            for word in sent:
                file.write(word+"\n")
            file.write("\n")

categories = brown.categories()
with open("truecaser/training/brown.words",'w') as file:
    for category in categories:
        sents = brown.sents(categories=categories)
        for sent in sents:
            for word in sent:
                file.write(word+"\n")
            file.write("\n")

categories = reuters.categories()
with open("truecaser/training/reuters.words",'w') as file:
    for category in categories:
        sents = reuters.sents(categories=categories)
        for sent in sents:
            for word in sent:
                if (not word.isupper()):
                    file.write(word+"\n")
            file.write("\n")