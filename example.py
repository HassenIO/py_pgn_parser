'''
    Run: python example.py
'''

import pgnparser

game = pgnparser.PGNParser('samples/budapest.pgn')
print game.plies
