from collections import defaultdict
from typing import List, Set

from grammar import Grammar, GrammarRule
from config import EARLY_INIT_NTERM


class Situation:
    def __init__(self, rule: GrammarRule, dot_pos=0, init_idx=0):
        self.rule = rule
        self.dot_pos = dot_pos
        self.init_idx = init_idx

    def __eq__(self, other):
        return self.rule == other.rule and self.dot_pos == other.dot_pos and self.init_idx == other.init_idx

    def __hash__(self):
        return hash(self.rule) + hash(self.dot_pos) + hash(self.init_idx)

    def __repr__(self):
        rule = self.rule
        return '({} -> {}.{}, {})'.format(rule.nterm,
                                          ' '.join(rule.product[:self.dot_pos]),
                                          ' '.join(rule.product[self.dot_pos:]),
                                          self.init_idx)

    def with_moved_dot(self):
        return Situation(self.rule, self.dot_pos + 1, self.init_idx)

    def is_dot_last(self):
        return self.dot_pos == len(self.rule.product)

    def is_next_nterm(self):
        return not self.is_dot_last() and GrammarRule.is_nterm(self.rule.product[self.dot_pos])

    def get_next_item(self):
        return self.rule.product[self.dot_pos]


class EarlyAlgorithm:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.rules_dict = self._gen_rules_dict(grammar.rules)
        self.situations: List[Set[Situation]] = []

    @staticmethod
    def _gen_rules_dict(rules):
        rules_dict = defaultdict(set)
        for rule in rules:
            rules_dict[rule.nterm].add(rule)
        return rules_dict

    def _get_finite_situation(self):
        init_nterm = self.grammar.get_init_nterm()
        return Situation(GrammarRule(EARLY_INIT_NTERM, [init_nterm]), dot_pos=1, init_idx=0)

    def _predict(self, j):
        for situation in self.situations[j].copy():
            if not situation.is_next_nterm():
                continue
            for new_rule in self.rules_dict[situation.get_next_item()]:
                self.situations[j].add(Situation(new_rule, init_idx=j))

    def _complete(self, j):
        for situation in self.situations[j].copy():
            if not situation.is_dot_last():
                continue
            for prev_sit in self.situations[situation.init_idx].copy():
                if prev_sit.is_next_nterm() and prev_sit.get_next_item() == situation.rule.nterm:
                    self.situations[j].add(prev_sit.with_moved_dot())

    def _scan(self, j, word):
        if j == 0:
            return
        for situation in self.situations[j - 1]:
            if situation.is_next_nterm() or situation.is_dot_last():
                continue
            if word[j - 1] == situation.get_next_item():
                self.situations[j].add(situation.with_moved_dot())

    def _checking_word(self, word: str):
        for j in range(0, len(word) + 1):
            self._scan(j, word)
            last_set_len = len(self.situations[j])
            while True:
                self._complete(j)
                self._predict(j)
                if len(self.situations[j]) == last_set_len:
                    break
                last_set_len = len(self.situations[j])

    def predict_word(self, word: str):
        self.situations = [set() for i in range(len(word) + 1)]
        init_situation = Situation(GrammarRule(EARLY_INIT_NTERM, [self.grammar.get_init_nterm()]),
                                   dot_pos=0, init_idx=0)
        self.situations[0].add(init_situation)
        self._checking_word(word)
        finite_rule = self._get_finite_situation()
        return finite_rule in self.situations[len(word)]
