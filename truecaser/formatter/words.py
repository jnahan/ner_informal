lower = open('truecaser/word_lists/lower.words', 'w')
title = open('truecaser/word_lists/title.words', 'w')

common_words = open('truecaser/word_lists/words.txt', 'r')
for word in common_words:
    if word.islower():
        lower.write(word)
    else:
        title.write(word)