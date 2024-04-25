# truecaser

### resources
- nltk corpus
- list of common words that are/are not named entities
    - https://github.com/dwyl/english-words
- list of common suffixes
- list of common words that precede/follow named entities

### approach
- hmm + viterbi trained on nltk corpus
    - 50% tweets?

### todo
- neural network in minor way
    - bert embeddings
        - u can download different sized embeddings
    - machine learning packages allow u to download embeddings other people have trained
    - don't jump to bert, there are smaller embedding
- spacy python library
    - embeddings u can download (vectors representing words)
    - classes of words to address oov
- similarity to uppercase words, lowercase words
- one embedding that is average of all lower, average of all upper
- reference nymble -> high performance name finder
- john vertago? office hours, more experience with neural networks

### compare to state of the art
- our work is better than ___ but not as good as ___
- our work is within 1% of the state of the arts
- if we do work on nltk, we can say we were able to improve the system by x%
- however idk how represenative nltk is of ner taggers
- more likely to succeed (publishing) if we focus on truecaser
- as an example, we can also talk about how much we were able to improve ner system with our code

### features
- unknown words that appear once
- hard coded likelihood (punctuation, number, other, uppercase, hyphenation)
- check if there are common words that precede/follow named entities before/after the word
- if we have oov
    - check if is a url/username
    - check if word ends with suffix that is rarely found in named entities
    - set it to title if it isn't in list of common lower case words

training
development
testing (when we are done with development)