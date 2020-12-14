from grammar import Grammar
from early_algorithm import EarlyAlgorithm


class Algo:
    def __init__(self):
        self.grammar = None

    def fit(self, grammar: Grammar):
        self.grammar = grammar

    def predict(self, word: str):
        algorithm = EarlyAlgorithm(self.grammar)
        return algorithm.predict_word(word)
