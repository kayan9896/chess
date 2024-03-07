from flask import Flask, request, jsonify
import chess
from ai import AI  # Assuming the AI class is implemented in a separate file named "ai.py"

from flask_cors import CORS  # Import the CORS module
app = Flask(__name__)
CORS(app) 
game = None
ai = AI()

def to2d(game):
    lines=game.__str__().split('\n')
    rt=[]
    for l in lines:
        l.strip('\"')
        rt.append(l.split(' '))
    return rt

@app.route('/start', methods=['GET'])
def start_game():
    global game
    game = chess.Board()
    
    return jsonify({'board': to2d(game)}), 200

@app.route('/move', methods=['POST'])
def make_move():
    global game
    if not game:
        return jsonify({'message': 'Game not started. Use /start endpoint to start a new game.'}), 400

    move = request.json.get('move')
    if not move:
        return jsonify({'message': 'Move parameter is missing.'}), 400

    try:
        move.replace('-','')
        game.push_san(move)
    except ValueError:
        return jsonify({'message': 'Invalid move.'}), 400
    gg="Gameover" if game.is_game_over else ""
    return jsonify({'board': to2d(game), "message":move + gg }), 200

@app.route('/getmove', methods=['GET'])
def get_move():
    if not game.is_game_over() and game.turn == chess.BLACK:
        best_move, _ = ai.minimax(game, 5, float('-inf'), float('inf'), True)
        game.push(best_move)
    gg="Gameover" if game.is_game_over else ""
    return jsonify({'board': to2d(game), "message":best_move.__str__()+gg}), 200

if __name__ == "__main__":
    app.run(debug=True)
