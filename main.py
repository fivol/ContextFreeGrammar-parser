#!/bin/python3
import argparse

from grammar import Grammar
from algo import Algo
from exceptions import *
from words_generator import Generator


parser = argparse.ArgumentParser(description='Context-free grammar src. Read more in README.md')
parser.add_argument('--grammar_file', '-g', help='Grammar file name', required=True)
parser.add_argument('--word_file', '-w', help='The name of the file where the word is located', required=False)
parser.add_argument('--word', help='Word to predict fit grammar', required=False)
parser.add_argument('--max_length', help='Generate words in grammar language less than specified length', required=False)


def predict(grammar_file: str, word: str):
    word = word.strip().replace(' ', '')
    grammar = Grammar.from_file(grammar_file)
    algo = Algo()
    algo.fit(grammar)
    return algo.predict(word)


def main(args):
    if args.max_length:
        # Generate words in language
        max_length = int(args.max_length)
        words = Generator(Grammar.from_file(args.grammar_file)).brute_force_generator(max_length)
        print(' '.join(words))
        return

    if not args.word and not args.word_file:
        print('Please specify one of --word_file or --word argument')
        return
    word = args.word
    if not word:
        with open(args.word_file) as f:
            word = f.read()
    try:
        if predict(args.grammar_file, word):
            print('The word belongs to grammar :)')
        else:
            print('The word does not belong to grammar :(')
    except GrammarIncorrectException as e:
        print(f'Incorrect grammar: {str(e)}')


if __name__ == '__main__':
    main(parser.parse_args())
