#script to format word tag pairs
from nltk.tokenize.treebank import TreebankWordDetokenizer

#for tagged words
def formatter(newline, unformatted_file):
    sentences = []
    sent = []

    file = open(unformatted_file, 'r')
    res = open("ner/testing/formatted.truecased.words", 'w')
    for line in file:
        if (line == "\n"):
            if (len(sent) > 0):
                sentences.append(sent)
                res.write(TreebankWordDetokenizer().detokenize(sent))
                res.write("\n")
            sent = []
            continue
        line = line.strip()
        word, tag = line.split('\t')
        if (tag == "uppercase" or tag == "title case"):
            sent.append(word.capitalize())
        elif (tag == "lowercase"):
            sent.append(word.lower())
        else:
            sent.append(word)
    file.close()
    res.close()

formatter(False, "truecaser/development/result.words")

def new_line_remover():
    sentences = []
    sent = []
    
    #change these
    file = open("truecaser/development/original.words", 'r')
    res = open("ner/testing/formatted.original.words", 'w')
    for line in file:
        if (line == "\n"):
            if (len(sent) > 0):
                sentences.append(sent)
                res.write(TreebankWordDetokenizer().detokenize(sent))
                res.write("\n")
            sent = []
        line = line.strip()
        sent.append(line)

new_line_remover()