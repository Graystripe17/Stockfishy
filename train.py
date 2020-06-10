#!/usr/bin/env python3
import os
import chess.pgn
for fn in os.listdir("data"):
    while True:
        pgn = open(os.path.join("data", fn))
        game = chess.pgn.read_game(pgn)
        print(game.headers)
        board = game.board()
        for i, move in enumerate(game.mainline_moves()):
            board.push(move)
            print(i, board)
        if game is None:
            break
    exit(0)

