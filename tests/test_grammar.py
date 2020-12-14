import pytest
from grammar import Grammar, GrammarRule
from config import *


def test_grammar_recognition1():
    grammar = """
    S->a
    S->b|c
    """
    g = Grammar.from_string(grammar)
    assert len(g.rules) == 3
    assert g.get_init_nterm() == 'S'


def test_grammar_recognition2():
    grammar = """
    WORD->abSYM
    SYM->b|c|$
    """
    g = Grammar.from_string(grammar)
    assert len(g.rules) == 4
    assert g.get_init_nterm() == 'WORD'


def test_grammar_recognition4():
    grammar = """
    SS->SS|a
    """
    g = Grammar.from_string(grammar)
    assert len(g.rules) == 2
    assert g.get_init_nterm() == 'SS'


def test_grammar_recognition5():
    grammar = """
    A   -> aaaaa|a|a|bb   bbb    |B
    B->&
    """
    g = Grammar.from_string(grammar)
    assert len(g.rules) == 6
    assert g.get_init_nterm() == 'A'
    assert len(g._alphabet) == 3


def test_grammar_rule():
    assert Grammar._prepare_product('FdSD') == ['F', 'd', 'SD']
    assert Grammar._prepare_product('WORD') == ['WORD']
    assert Grammar._prepare_product('12 34') == ['1', '2', '3', '4']
    assert Grammar._prepare_product('a b   c') == ['a', 'b', 'c']
    assert Grammar._prepare_product('H   D  F') == ['H', 'D', 'F']
    assert Grammar._prepare_product('  U ij') == ['U', 'i', 'j']
    assert Grammar._prepare_product(GRAMMAR_EPSILON) == []
