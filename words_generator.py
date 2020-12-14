from grammar import Grammar
from algo import Algo


class Generator:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.algo = Algo()
        self.algo.fit(grammar)

    def _recursive_generator(self, curr_word, word_len, words: list):
        if self.algo.predict(curr_word):
            words.append(curr_word)
        for c in self.grammar.alphabet:
            if len(curr_word) < word_len:
                self._recursive_generator(curr_word + c, word_len, words)

    def brute_force_generator(self, max_length=5):
        words = []
        self._recursive_generator('', max_length, words)
        return words
