title = open('truecaser/title.words', 'w')
lower = open('truecaser/lower.words', 'w')

common_words = open('truecaser/words.txt', 'r')
for word in common_words:
    if word.islower():
        lower.write(word)
    else:
        title.write(word)