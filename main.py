import os
import numpy as np
import time
from copy import deepcopy

clear = lambda: os.system('cls')

class Game():
    def __init__(self, human_player):
        self.player = 1 #1, 2
        self.terminate = False
        self.search_depth = 4
        self.human = human_player
        self.board_dim = 8
        self.board = self.initialize_board()
    def initialize_board(self):
        return "0"*self.board_dim**2
    
    def drop_block(self, x, b, p):
        for y in range(self.board_dim+1):
            if y == self.board_dim:
                b = self.place_block(x, y-1, b, p)
                return b
            if b[y*self.board_dim+x] != "0":
                b = self.place_block(x, y-1, b, p)
                return b

    def place_block(self, x, y, b, p):
        a = list(b)
        a[y*self.board_dim+x] = str(p)
        b = "".join(a)
        return b

    def display_board(self,board):
        bd = self.board_dim
        print("-"*(bd*2+1))
        for y in range(bd):
            print(f"|{''.join([board[y*bd+x]+'|' for x in range(bd)])}")
            print("-"*(bd*2+1))
        print("\n")

    def check_board_for_win(self,b):
        # 2D
        bd = self.board_dim
        # TODO
        for p in range(1,3):
            if any([all([b[i*bd+j]==str(p) for j in range(bd)]) for i in range(bd)]) or any([all([b[j*bd+i]==str(p) for j in range(bd)]) for i in range(bd)]) or all([b[i*bd+i]==str(p) for i in range(bd)]) or all([b[i*bd+(bd-i-1)]==str(p) for i in range(bd)]):
                return p
        return False

class Board():
    def __init__(self,board):
        self.board = board
        self.past_moves = []
        self.score = 0
    def full(self):
        return self.board.count("0") == 0
    def get_possible_moves(self):
        return [n for n in range(game.board_dim) if self.board[n]=="0"]
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

# Search tree AI to play a game of connect-4

# task 1: implement in 2D Connect 4
# board is represented as text of length board size ^ 2. "120000...00" means first row from top, looking left to right has placement from player
# "p" and player "b", where "e" is empty.

""" 
"1000 0100 0010 0001" = 
1000
0100
0010
0001
"""
game = Game(human_player=1)

def search_debug(board, to_max, max_depth):
    game.display_board(board.board)
    print(f"past_moves = {board.past_moves} score = {board.score} | to_max = {to_max} | cur_depth = {max_depth}\n")

def search(board, to_max, max_depth): # recursive search for optimal choice within game.depth moves
    # search_debug(board,to_max,max_depth)
    if not board.full() and max_depth > 0:
        # win condition
        if game.check_board_for_win(board.board):
            if to_max:
                board.score = 1
            else:
                board.score = -1
            # print("WIN MOVE FOUND")
            # search_debug(board,to_max,max_depth)
            return board
        # search
        if game.human == 1:
            p = 2 if to_max else 1
        else:
            p = 1 if to_max else 2
        b = Board([])
        if to_max: b.score = float("inf")
        else: b.score = float("-inf") 
        for move_x in [n for n in range(game.board_dim) if board.board[n]=="0"]:
            post_move_board = Board(game.drop_block(move_x, board.board, p))
            post_move_board.past_moves = board.past_moves + [move_x]
            res = search(post_move_board, not to_max, max_depth - 1)
            if to_max: b = res if res.score < b.score else b
            else: b = res if res.score > b.score else b
        # print(b.score)
        return b
    else:
        return board

# main

def main():
    # game.board = "2000200020001100"
    while not game.terminate:
        # decide moves
        if game.player == game.human: # player
            x = int(input("Enter column to place in [x] format, 0 indexed: "))
            while game.board[x] != "0":
                x = int(input("That column is full, try a different one: "))
        else: # bot
            future_board = search(Board(game.board), True, game.search_depth)
            print(future_board.past_moves)
            x = future_board.past_moves[0]
        # make move
        game.board = game.drop_block(x, game.board, game.player)

        # display board
        game.display_board(game.board)

        # check game end
        # did anyone win
        res = game.check_board_for_win(game.board)
        if res:
            print(f"{res} WIN! GG")
            game.terminate = True
        # is board full
        if game.board.count("0") == 0:
            print("TIE!")
            game.terminate = True

        # flip player
        game.player = 2 if game.player == 1 else 1
        
        time.sleep(0.2)
        # clear()

main()