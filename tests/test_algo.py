import pytest
from main import predict

"""Не меняйте файлы в папке examples, иначе тесты не пройдут"""

examples = 'examples'


def predict_word_in_grammar(i, word):
    g_name = f'{examples}/grammar{i}.txt'
    return predict(grammar_file=g_name, word=word)


def predict_str_grammar(grammar_text, word):
    t_file = '/tmp/grammar_parser.txt'
    with open(t_file, 'w') as f:
        f.write(grammar_text)
    return predict(grammar_file=t_file, word=word)


def test_examples():
    for i in range(1, 4):
        g_name = f'{examples}/grammar{i}.txt'
        word_name = f'{examples}/word{i}.txt'
        with open(word_name) as word_f:
            assert predict(grammar_file=g_name, word=word_f.read())


def test_grammar1():
    """Грамматика правильных скобочный последовательностей с буквой 'a' в любом месте"""
    assert predict_word_in_grammar(1, 'a')
    assert predict_word_in_grammar(1, 'aaaaaaa')
    assert predict_word_in_grammar(1, '(a)aaa()()()')
    assert predict_word_in_grammar(1, '(((())))a')
    assert predict_word_in_grammar(1, '()()()()((()))((()()()))((()))')
    assert predict_word_in_grammar(1, '()a((aa((a)a))a)aa')
    assert predict_word_in_grammar(1, 'a(a)')
    assert predict_word_in_grammar(1, '')
    assert predict_word_in_grammar(1, '()')
    assert predict_word_in_grammar(1, '(())')
    assert predict_word_in_grammar(1, 'aa()')
    assert not predict_word_in_grammar(1, '()()()()((()))((()()()))(()))')
    assert not predict_word_in_grammar(1, 'fsd')
    assert not predict_word_in_grammar(1, 'ab')
    assert not predict_word_in_grammar(1, 'aaaaaabaaaaa')
    assert not predict_word_in_grammar(1, '(((((((aaaaaabaaaaa)))))))')
    assert not predict_word_in_grammar(1, '(')
    assert not predict_word_in_grammar(1, ')))))))))')
    assert not predict_word_in_grammar(1, '()()()()()b')
    assert not predict_word_in_grammar(1, '()()()()()FDSFDS')
    assert not predict_word_in_grammar(1, '()()()()()(')
    assert not predict_word_in_grammar(1, '()(((()))')
    assert not predict_word_in_grammar(1, '()a((aa((a)a))aaa')


def test_grammar2():
    """Одинаковое количеству букв 'a' и 'b' в слове. Любое кол-во букв 'c'"""
    assert predict_word_in_grammar(2, 'ab')
    assert predict_word_in_grammar(2, 'aabbcccccc')
    assert predict_word_in_grammar(2, 'ccccc ababababab ccc ababcabab')
    assert predict_word_in_grammar(2, 'aabb')
    assert predict_word_in_grammar(2, 'bababababa')
    assert predict_word_in_grammar(2, 'bbbbaaaa')
    assert predict_word_in_grammar(2, 'cbbcbbccacaaaccccc')
    assert predict_word_in_grammar(2, 'abbbaccbababcccccbbaaaabbaa')
    assert predict_word_in_grammar(2, '')
    assert predict_word_in_grammar(2, 'cccc')
    assert predict_word_in_grammar(2, 'ba')
    assert not predict_word_in_grammar(2, 'x')
    assert not predict_word_in_grammar(2, 'fsdiofjodsfj')
    assert not predict_word_in_grammar(2, 'ababababr')
    assert not predict_word_in_grammar(2, 'aba')
    assert not predict_word_in_grammar(2, 'a')
    assert not predict_word_in_grammar(2, 'b')
    assert not predict_word_in_grammar(2, 'aaaabbb')
    assert not predict_word_in_grammar(2, 'ababbaabbaabbabbaaa')
    assert not predict_word_in_grammar(2, 'cccccca')


def test_grammar3():
    """Правильное математическое выражение в десятичной системе со знаками +-*/ и скобками. Нету унарного минуса!"""
    assert predict_word_in_grammar(3, '0')
    assert predict_word_in_grammar(3, '6')
    assert predict_word_in_grammar(3, '32523432432')
    assert predict_word_in_grammar(3, '(343)')
    assert predict_word_in_grammar(3, '(2) + (2-2) / 123*32*(44-3) + 0 - 16')
    assert predict_word_in_grammar(3, '1+1-1+2-3*3/44444*(((3)))')
    assert predict_word_in_grammar(3, '1+(0/43)*444 - ((3-1)*4323/(1+1))')
    assert not predict_word_in_grammar(3, '01')
    assert not predict_word_in_grammar(3, '')
    assert not predict_word_in_grammar(3, '00')
    assert not predict_word_in_grammar(3, '0000')
    assert not predict_word_in_grammar(3, '77&&')
    assert not predict_word_in_grammar(3, '((')
    assert not predict_word_in_grammar(3, '(434+')
    assert not predict_word_in_grammar(3, '0(12)')
    assert not predict_word_in_grammar(3, '(12) + 00')
    assert not predict_word_in_grammar(3, '+ 01312')
    assert not predict_word_in_grammar(3, '+.01312')
    assert not predict_word_in_grammar(3, '+')
    assert not predict_word_in_grammar(3, '3+-4')
    assert not predict_word_in_grammar(3, '-4')
    assert not predict_word_in_grammar(3, '1+(0/43)*444 - ((3-1)*4323/(1+1))-00')


def test_custom_grammar():
    g = """AB->aABb|ab"""
    assert predict_str_grammar(g, "ab")
    assert predict_str_grammar(g, "aaabbb")
    assert predict_str_grammar(g, "aabb")
    assert predict_str_grammar(g, 'a'* 100 + 'b'*100)
    assert not predict_str_grammar(g, '')
    assert not predict_str_grammar(g, 'cab')
    assert not predict_str_grammar(g, 'bac')
    assert not predict_str_grammar(g, 'bbaa')
    assert not predict_str_grammar(g, 'ba')
    assert not predict_str_grammar(g, 'aaabb')
    assert not predict_str_grammar(g, 'abab')
    assert not predict_str_grammar(g, 'aba')
    assert not predict_str_grammar(g, 'baba')
    assert not predict_str_grammar(g, 'bbbaaa')
    assert not predict_str_grammar(g, 'aaabbbb')
    assert not predict_str_grammar(g, 'aaab')
    assert not predict_str_grammar(g, 'cccc')
