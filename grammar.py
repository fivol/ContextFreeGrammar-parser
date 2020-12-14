from config import *
from constants import *
from exceptions import GrammarIncorrectException
import re


class GrammarRule:

    def __init__(self, nterm: str, product: list):
        assert self.is_nterm(nterm), nterm
        self._nterm = nterm
        self._product = product
        
    @property
    def nterm(self):
        return self._nterm

    @property
    def product(self):
        return self._product

    def __repr__(self):
        return f'{self.nterm} -> {" ".join(self.product if self.product else GRAMMAR_EPSILON)}'

    def __eq__(self, other):
        return self.nterm == other.nterm and self.product == other.product

    def __hash__(self):
        return hash(self.nterm) + sum(map(lambda x: hash(x), self.product))

    @staticmethod
    def is_nterm(string: str):
        return re.fullmatch(r'[A-ZА-Я_]+', string) is not None

    def get_terms(self):
        return [term for term in self.product if not self.is_nterm(term)]

    def get_nterms(self):
        return [term for term in self.product if self.is_nterm(term)]


class Grammar:
    """Класс задающий контекстно свободную грамматику"""

    def __init__(self, rules: list, nterms: set, alphabet: set):
        self._rules = rules
        self._non_terms = nterms
        self._alphabet = alphabet

    @property
    def rules(self):
        return self._rules

    @property
    def alphabet(self):
        return self._alphabet

    def get_init_nterm(self):
        return self._rules[0].nterm

    @staticmethod
    def from_file(filename):
        with open(filename, 'r') as gr_file:
            return Grammar.from_string(gr_file.read())

    @staticmethod
    def from_string(string):
        alphabet = set()
        nterms = set()
        rules = []
        lines = string.strip().split(GRAMMAR_RULES_SEP)

        for line in lines:
            rules += Grammar._parse_rule_string(line)

        for rule in rules:
            alphabet.update(rule.get_terms())
            nterms.add(rule.nterm)

        # check if all right non terminals exist in left part of rules
        Grammar._check_grammar_correct(rules, nterms)

        return Grammar(rules=rules, alphabet=alphabet, nterms=nterms)

    @staticmethod
    def _check_grammar_correct(rules, nterms):
        right_nterms = nterms.copy()
        for rule in rules:
            right_nterms.update(rule.get_nterms())

        if len(right_nterms) > len(nterms):
            msg = f'{MSG_UNDEF_NTERM}: "{next(iter(right_nterms - nterms))}"'
            raise GrammarIncorrectException(msg)

    @staticmethod
    def _parse_rule_string(string: str):
        rules = []
        try:
            non_term, products = string.strip().split(GRAMMAR_RULE_PARTS_SEP)
        except ValueError:
            raise GrammarIncorrectException(MSG_WRONG_RULE)

        non_term = non_term.strip()
        for product in products.split(GRAMMAR_PRODUCT_SEP):
            rules.append(GrammarRule(non_term, Grammar._prepare_product(product)))

        return rules

    @staticmethod
    def _gen_tokens(string):
        i = 0
        while i < len(string):
            word = ''
            while i < len(string) and GrammarRule.is_nterm(string[i]):
                word += string[i]
                i += 1
            if not word and string[i]:
                word += string[i]
                i += 1
            yield word

    @staticmethod
    def _prepare_product(product):
        product = product.replace(GRAMMAR_EPSILON, '').strip().split()
        return list(filter(lambda x: bool(x),
                           sum(map(lambda item:
                                   list(Grammar._gen_tokens(item)), product), [])))
