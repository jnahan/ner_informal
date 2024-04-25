#script to format word tag pairs

def formatter(newline):
    next_tag = ""

    file = open("truecaser/result.words", 'r')
    res = open("truecaser/formatted.words", 'w')
    lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if (line == "\n"):
            res.write("\n\n")
            continue
        line = line.strip()
        word, tag = line.split('\t')

        if i < len(lines) - 1:
            next_line = lines[i+1].strip()
            if next_line:  # Check if the line is not empty
                next_word, next_tag = next_line.split('\t')
            else:
                next_tag = ""
        if (tag == "uppercase" or tag == "titlecase"):
            res.write(word.capitalize())
        elif (tag == "lowercase"):
            res.write(word.lower())
        else:
            res.write(word)
        if (newline):
            res.write("\n")
        else:
            if (next_tag == "punctuation" or next_tag == "other"):
                continue
            res.write(" ")

    file.close()
    res.close()

formatter(False)