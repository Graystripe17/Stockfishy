#!/usr/bin/env python3
import os
import chess.pgn
from state import State

for fn in os.listdir("data"):
    while True:
        pgn = open(os.path.join("data", fn))
        game = chess.pgn.read_game(pgn)
        result = game.headers["Result"]
        board = game.board()
        value = {"1/2-1/2": 0, "0-1": -1, "1-0": 1}
        for i, move in enumerate(game.mainline_moves()):
            board.push(move)
        print(value[result], State(board).serialize())
        if game is None:
            break
    exit(0)
