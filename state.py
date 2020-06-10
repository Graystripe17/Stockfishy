#!/usr/bin/env python3
import chess

class State:
    def __init__(self):
        self.board = chess.Board()

    def value(self):
        return 1

    def edges(self):
        return list(self.board.legal_moves)

    def serialize(self):
       # network
       pass

if __name__ == "__main__":
    s = State()
    print(s.edges())
