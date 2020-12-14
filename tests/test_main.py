import pytest
from main import main, parser


def test_main():
    main(parser.parse_args(['--grammar_file', 'examples/grammar1.txt', '--word', '()']))
    main(parser.parse_args(['--grammar_file', 'examples/grammar3.txt', '--word_file', 'examples/word3.txt']))
    main(parser.parse_args(['--grammar_file', 'examples/grammar3.txt', '--max_length', '2']))
