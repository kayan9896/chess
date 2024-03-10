from flask import Flask, request, jsonify
import chess
from ai import AI  # Assuming the AI class is implemented in a separate file named "ai.py"
import uuid
from flask_cors import CORS  # Import the CORS module
import time

app = Flask(__name__)
CORS(app) 
games = {}
ai = AI()

def to2d(game):
    lines=game.__str__().split('\n')
    rt=[]
    for l in lines:
        l.strip('\"')
        rt.append(l.split(' '))
    return rt

@app.route('/board', methods=['POST'])
def board():
    id=request.json.get('number')
    if id not in games:
        return jsonify({'message': 'Gameover.'}), 400
    game=games[id]['game']
    return jsonify({'board': to2d(game)}), 200

@app.route('/start', methods=['GET'])
def start_game():
    game_id = str(uuid.uuid4())
    game = chess.Board()
    games[game_id]={'game': game}
    return jsonify({'board': to2d(game),'id':game_id,"message":'White turn'}), 200

@app.route('/mov', methods=['POST'])
def make_mov():
    id=request.json.get('id')
    game=games[id]['game']
    if not game:
        return jsonify({'message': 'Game not started. Use /start endpoint to start a new game.'}), 400
    
    move = request.json.get('move')
    if not move:
        return jsonify({'message': 'Move parameter is missing.'}), 400

    try:
        game.push_san(move)
    except ValueError:
        return jsonify({'message': 'Invalid move.'}), 400
    if game.is_game_over():
        games.pop(id)
        return jsonify({'board': to2d(game), "message":'Gameover' }), 200
    return jsonify({'board': to2d(game), "message":'Last move: '+move +'\n' + ('black' if game.turn==chess.BLACK else 'white')+' turn' }), 200

@app.route('/startai', methods=['POST'])
def start_ai():
    game_id = str(uuid.uuid4())
    game = chess.Board()
    diff=request.json.get('diff')
    games[game_id]={'game': game, 'diff': diff}
    return jsonify({'board': to2d(game),'id':game_id}), 200

@app.route('/move', methods=['POST'])
def make_move():
    id=request.json.get('id')
    game=games[id]['game']
    if not game:
        return jsonify({'message': 'Game not started. Use /start endpoint to start a new game.'}), 400

    move = request.json.get('move')
    if not move:
        return jsonify({'message': 'Move parameter is missing.'}), 400

    try:
        game.push_san(move)
    except ValueError:
        return jsonify({'message': 'Invalid move.'}), 400
    gg= "AI is thinking"

    return jsonify({'board': to2d(game), "message":'Last move of you: '+move +'\n' + gg }), 200

@app.route('/getmove/<id>', methods=['GET'])
def get_move(id):
    if id not in games:
        return jsonify({'message': 'Invalid id.'}), 400
    game=games[id]['game']
    diff=games[id]['diff']
    best_move=None
    gg="Your turn"
    if not game.is_game_over() and game.turn == chess.BLACK:
        best_move, _ = ai.minimax(game, diff, float('-inf'), float('inf'), True)
        game.push(best_move)
    if game.is_game_over():
        gg="Gameover."
        games.pop(id)
        print(games)
    return jsonify({'board': to2d(game), "message":'Last move of AI: '+best_move.__str__() if best_move else ''+'\n'+gg}), 200


@app.route('/join', methods=['POST'])
def join_game():
    number = request.json.get('number')
    if number not in games:
        games[number] = {'game': None}
        t=5
        while t>0:
            time.sleep(6)
            t-=1
            if games[number]['game']:
                side=not games[number]['p2']
                return jsonify({'board': to2d(games[number]['game']),'side': side}), 200   
        games.pop(number)
        return jsonify({'error': 'Timeout waiting for another player'}), 500
    else:
        # Player joined; start game and return board
        if games[number]['game']:
            return jsonify({'error': 'Room is not available'}), 500
        else:
            game = chess.Board()
            games[number]={'game': game,'p2':chess.BLACK}
            return jsonify({'board': to2d(game),'side':chess.BLACK}), 200

def match():
    while len(waitlist)>1:
        p1=waitlist.pop()
        p2=waitlist.pop()
        game_id = str(uuid.uuid4())
        game = chess.Board()
        games[game_id]={'game': game,p1:chess.WHITE,p2:chess.BLACK}
        assigned[p1]=game_id
        assigned[p2]=game_id

waitlist=[]
assigned={}
@app.route('/find', methods=['POST'])
def find():
    number = uuid.uuid4()
    waitlist.append(number)
    t=5
    while t>0:
        time.sleep(6)
        t-=1
        match()
        if number in assigned:
            return jsonify({'board': to2d(games[assigned[number]]['game']),'side': games[assigned[number]][number],'gameid':assigned[number]}), 200   
    waitlist.remove(number)
    return jsonify({'error': 'Timeout waiting for another player'}), 500


if __name__ == "__main__":
    app.run(debug=True)
