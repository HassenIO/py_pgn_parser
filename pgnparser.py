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

class PGNParser(object):

    TAG_PATTERN = re.compile("^\[([A-Za-z]+) \"(.*)\"\]$")
    PLY_PATTERN = re.compile('^(\d+\.) ([KQRNBOa-hx0-8\+\-\?!# ]+)$')


    def __init__(self, file_name):
        '''
            Init the class attributes
        '''
        self.tags = {}
        self.raw_moves = ''
        self.plies = []

        self.pgn_array = parse_pgn(file_name)
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
            Get a specific ply moves
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



def parse_pgn(file_name):
    '''
        Read and parse the PGN file and return each line in an array
    '''

    # Get the content of the PGN file
    pgn_text = open(file_name).read()

    # Split lines and remove empty elements
    return filter(None, pgn_text.split("\n"))
