# -*- coding:utf-8 -*-
# Copyright (c) 2016 Hassen TAIDIRT, htaidirt at gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

'''
    Simple Chess game parser based on PGN.

    Portable Game Notation (PGN) is a plain text computer-processible format for recording chess games (both the moves and related data), supported by many chess programs (source: https://en.wikipedia.org/wiki/Portable_Game_Notation).

    Basic usage:
'''

class ParseGames(object):
    '''
        This class parses PGN file that contains many games.
    '''


    def __init__(self, file_name):
        '''
            Init the class attributes
        '''
        self.file_name = file_name
        self.raw_games = self._split_games() # Get the games as an array of PGN texts
        self.games = [ParseGame(game_pgn_text) for game_pgn_text in self.raw_games]


    def _split_games(self):
        '''
            Given a PGN file, split games into array of PGN lines
        '''
        with open(self.file_name) as f:
            pgn_content = f.readlines()

        is_tag, is_move = False, False
        games, game = [], ''

        for pgn_line in pgn_content:

            # If we are in a tag game line, and we already passed through tags and moves
            # then this means it's a new game. Append the previous game in the games array
            # and reset variables for the new game.
            if pgn_line[0] == '[' and is_tag and is_move:
                games.append(game)
                is_tag, is_move = False, False
                game = ''

            # Change is_tag and is_move when necessary
            if pgn_line[0] == '[':
                is_tag = True
            elif pgn_line[0] == '1':
                is_move = True

            game = game + pgn_line

        # The last game doesn't have a tag after the moves
        games.append(game)
        return games




class ParseGame(object):
    '''
        This class parses a single PGN game, given the PGN text.
    '''

    TAG_PATTERN = re.compile("^\[([A-Za-z]+) \"(.*)\"\]$")
    PLY_PATTERN = re.compile('^(\d+\.) ([KQRNBOa-hx0-8\+\-\?!# ]+)$')


    def __init__(self, pgn_text_game):
        '''
            Init the class attributes
        '''
        self.pgn_text_game = pgn_text_game
        self.tags = {}
        self.raw_moves = ''
        self.plies = []

        self.pgn_array = filter(None, pgn_text_game.split("\n"))
        self._parse_game()


    def _parse_game(self):
        '''
            Parse the game by separating tags and moves
        '''

        moves = ''

        for pgn_el in self.pgn_array:
            # Match current element against tag pattern
            match_tag = self.TAG_PATTERN.match(pgn_el)

            if match_tag:
                # This means there are still game tags
                self.tags[match_tag.group(1)] = match_tag.group(2)
            else:
                # This means that the following line is a game transcript
                moves = moves + pgn_el + ' '

        # Clean moves before processing them
        moves = re.sub(' +', ' ', moves) # No double (or more) spaces
        moves = moves.strip() # Remove possible spaces in beginning and end
        self.raw_moves = moves

        plies_arr = re.split(r'[ ](?=[\d*\.])', moves) # Convert String moves to an array of plies
        plies_arr.pop() # Remove the last ply which is always the result of the game
        plies_arr = [self.PLY_PATTERN.match(ply_el).group(2) for ply_el in plies_arr] # Remove ply numbers

        self.plies = [{
            'w': ply.split(' ')[0],
            'b': ply.split(' ')[1] if len(ply.split(' ')) == 2 else ''
        } for ply in plies_arr] # Split each ply in a dictionnary of white (w) and black (b) move


    def ply(self, ply_number, player = False):
        '''
            Get a specific ply moves (white move and black move of a ply)
        '''

        if ply_number > len(self.plies):
            return {}
        else:
            if player in ['w', 'b']:
                return self.plies[ply_number - 1][player]
            else:
                return self.plies[ply_number - 1]


    def tag(self, tag_name):
        '''
            Get value of specific tag
        '''
        return self.tags[tag_name] if tag_name in self.game_tags() else ''


    def game_tags(self):
        '''
            List game tags keys
        '''
        return list(self.tags.keys())
