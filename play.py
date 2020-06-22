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
