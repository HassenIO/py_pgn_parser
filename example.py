'''
    Run: python example.py
'''

import pgnparser

pgn_games = pgnparser.ParseGames('samples/budapest.pgn')

game = pgn_games.games[1] # Get only the first game
print game.tags # Print tags of the first game
