from classifier_base import IETFClassifier
from functools import reduce

class PrototypeClassifier(IETFClassifier):
    def __init__(self, path: str):
        with open(path, 'r') as word_file:
            self.words = set([word.strip().lower() for word in word_file.readlines()])
    
    def classify(self, input: str):
        foreign_words_count = reduce(lambda count, _: count + 1,
                                filter(lambda word: word.lower() not in self.words, input.split(' ')),
                                0)
        if foreign_words_count:
            return None
        else:
            return 'en-US'