import string

file = open('truecaser/testing/original.words', 'r')
output = open('truecaser/testing/answers.words', 'w')

tags = ['Begin_Sent', 'title case', 'uppercase', 'lowercase', 'End_Sent', 'punctuation']

count = 0
first = True
for line in file:
    if line=='\n':
        output.write('\n')
        first = True
        continue
    word = line.strip()
    if word in string.punctuation:
        pos = 'punctuation'
    elif word[0].isnumeric():
        pos = 'number'
    elif not word[0].isalnum():
        pos = 'other'
    elif word.istitle():
        if first:
            pos = 'uppercase'
        else:
            pos = 'title case'
    else:
        pos = 'lowercase'
    first = False

    output.write(word.lower() + '\t' + pos + '\n')

print(count)

#python3 truecaser/testing/score.py truecaser/testing/answers.words truecaser/testing/result.words
#regex: answer:(.*)lowercase
#regex: answer:(.*)title case
