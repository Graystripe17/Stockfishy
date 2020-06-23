import os
from state import State
import time
from flask import Flask, Response, request
app = Flask(__name__)

MAXVAL = 10000
def explore_leaves(s, v):
    ret = []
    start = time.time()
    v.reset()
    bval = v(s)
    cval, ret = computer_minimax(s, v, 0, a=-MAXVAL, b=MAXVAL, big=True)
    eta = time.time() - start
    print("%.2f -> @.2f: explored %d nodes in %.3f seconds %d/sec" % (bval, cval, v.count, eta, v.count // eta))
    return ret


s = State()

class ClassicValuator:
    values = {chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0}

    def __init__(self):
        self.reset()
        self.memo = {}

    def reset(self):
        self.count = 0

    def __call__(self, s):
        self.count += 1
        key = s.key()
        if key not in self.memo:
            self.memo[key] = self.value(s)
        return self.memo[key]

    def value(self, s):
        b = s.board
        if b.is_game_over():
            if b.result() == "1-0":
                return MAXVAL
            elif b.result() == "0-1":
                return -MAXVAL
            else:
                return 0
        val = 0.0
        # Material
        pm = s.board.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                val += tval
            else:
                val -= tval
        # Legal moves
        bak = b.turn
        b.turn = chess.WHITE
        val += 0.1 * b.legal_moves.count()
        b.turn = chess.BLACK
        val -= 0.1 * b.legal_moves.count()
        b.turn = bak
        return val

def computer_minimax(s, v, depth, a, b):
    if depth >= 5 or s.board.is_game_over():
        return v(s)
    if s.board.turn == chess.WHITE:
        ret = -MAXVAL
    else:
        ret = MAXVAL
    isort = []
    for e in s.board.legal_moves:
        s.board.push(e)
        isort.append((v(s), e))
        s.board.pop()
    move = sorted(isort, key=lambda x: x[0], reverse=s.board.turn) # WHITE == True
    # Beam search
    if depth >= 3:
        move = move[:10]

    for e in [x[1] for x in move]:
        s.board.push(e)
        tval = computer_minimax(s, v, depth+1, a, b)
        s.board.pop()
        if s.board.turn == chess.WHITE:
            ret = max(ret, tval)
            a = max(a, ret)
            if a >= b: # b cut-off
                break
        else:
            ret = min(ret, tval)
            b = min(b, ret)
            if a >= b: # a cut-off
                break
    return ret

@app.route("/")
def hello():
    ret = open("index.html").read()
    return ret.replace('start', s.board.fen())

def computer_move(s, v):
    move = sorted(explore_leaves(s, v), key=lambda x:x[0], reverse=s.board.turn)
    if len(move) == 0:
        return
    print("Top 3:")
    for i, m in enumerate(move[0:3]):
        print("  ", m)
    print(s.board.turn, "moving", move[0][1])
    s.board.push(move[0][1])

@app.route("/move_coordinates")
def move_coordinates():
    if not s.board.is_game_over():
        source = int(request.args.get('from', default=''))
        target = int(request.args.get('to', default=''))
        promotion = True if request.args.get('promotion', default='') == 'true' else False
        move = s.board.san(chess.Move(source, target, promotion=chess.QUEEN if promotion else None))
        if move is not None and move != "":
            print("Human moves", move)
            try:
                s.board.push_san(move)
                computer_move(s, v)
            except Exception:
                traceback.print_exc()
        response = app.response_class(
            response=s.board.fen(),
            status=200
        )
        return response
    print("Game over")
    response = app.response_class(
        response="game over",
        status=200
    )
    return response

@app.route("/newgame")
def newgame():
    s.board.reset()
    response = app.response_class(
        response=s.board.fen(),
        status=200
    )
    return response

if __name__ == "__main__":
    if os.getenv("SELFPLAY") is not None:
        s = State()
        while not s.board.is_game_over():
            computer_move(s, v)
            print(s.board)
        print(s.board.result())
    else:
        app.run(debug=True)
