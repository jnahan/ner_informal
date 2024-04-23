# truecaser

### resources
- nltk corpus
- list of common words that are/are not named entities
- list of common suffixes
- list of common words that precede/follow named entities

### approach
- hmm + viterbi trained on nltk corpus
    - 50% tweets?

### features
- unknown words that appear once
- hard coded likelihood (punctuation, number, other, uppercase, hyphenation)
- check if there are common words that precede/follow named entities before/after the word
- if we have oov
    - check if is a url/username
    - check if word ends with suffix that is rarely found in named entities
    - set it to title if it isn't in list of common lower case words