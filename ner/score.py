correct = 0
incorrect = 0

answer_set = set()
response_set = set()

with open('ner/spacy/formatted.original.words', 'r') as answer_file:
    for line in answer_file:
        answer_set.add(line.strip().lower())
        
with open('ner/spacy/formatted.lower.words', 'r') as response_file:
    for line in response_file:
        response_set.add(line.strip().lower())

# True positives, false positive, false negatives
TP = len(answer_set.intersection(response_set))
FP = len(response_set.difference(answer_set))
FN = len(answer_set.difference(response_set))

# Calculate precision, recall, and F1-score
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1_score)