from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import chess
from .ai import AI 
import uuid
import time
from datetime import datetime
import json

games = {}
ai = AI()

def to2d(game):
    lines = game.__str__().split('\n')
    rt = []
    for l in lines:
        l.strip('\"')
        rt.append(l.split(' '))
    return rt


@csrf_exempt  # Add this decorator for POST requests if CSRF protection is enabled
def board(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('number')
        if id not in games:
            return JsonResponse({'message': 'Gameover.'}, status=400)
        game = games[id]['game']
        if game.is_game_over():
            return JsonResponse({'board': to2d(game), 'message': 'Gameover.'}, status=200)
        return JsonResponse({'board': to2d(game)}, status=200)

@csrf_exempt  # Add this decorator for GET requests if CSRF protection is enabled
def start_game(request):
    if request.method == 'GET':
        game_id = str(uuid.uuid4())
        game = chess.Board()
        games[game_id] = {'game': game}
        return JsonResponse({'board': to2d(game), 'id': game_id, 'message': 'White turn'}, status=200)

@csrf_exempt  # Add this decorator for POST requests if CSRF protection is enabled
def make_mov(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        time = data.get('time')

        if id not in games:
            print(id,games)
            return JsonResponse({'message': 'Game not started. Use /start endpoint to start a new game.'}, status=400)
        game = games[id]['game']
        games[id]['last'] = time
        if not game:
            return JsonResponse({'message': 'Game not started. Use /start endpoint to start a new game.'}, status=400)

        move = data.get('move')
        if not move:
            return JsonResponse({'message': 'Move parameter is missing.'}, status=400)

        try:
            game.push_san(move)
        except ValueError:
            return JsonResponse({'message': 'Invalid move.'}, status=400)
        if game.is_game_over():
            return JsonResponse({'board': to2d(game), 'message': 'Gameover'}, status=200)
        return JsonResponse({'board': to2d(game), 'message': f'Last move: {move}\n{"black" if game.turn == chess.BLACK else "white"} turn'}, status=200)

@csrf_exempt  # Add this decorator for POST requests if CSRF protection is enabled
def start_ai(request):
    if request.method == 'POST':
        game_id = str(uuid.uuid4())
        game = chess.Board()
        diff = json.loads(request.body).get('diff')
        games[game_id] = {'game': game, 'diff': diff}
        return JsonResponse({'board': to2d(game), 'id': game_id}, status=200)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

@csrf_exempt  # Add this decorator for POST requests if CSRF protection is enabled
def make_move(request):
    if request.method == 'POST':
        id = json.loads(request.body).get('id')
        time = json.loads(request.body).get('time')
        if id not in games:
            return JsonResponse({'message': 'Game not started. Use /start endpoint to start a new game.'}, status=400)
        game = games[id]['game']
        games[id]['last'] = time
        move = json.loads(request.body).get('move')
        if not move:
            return JsonResponse({'message': 'Move parameter is missing.'}, status=400)

        try:
            game.push_san(move)
        except ValueError:
            return JsonResponse({'message': 'Invalid move.'}, status=400)

        gg = "AI is thinking"
        return JsonResponse({'board': to2d(game), "message": 'Last move of you: ' + move + '\n' + gg}, status=200)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

def get_move(request, id):
    if request.method == 'GET':
        if id not in games:
            return JsonResponse({'message': 'Invalid id.'}, status=400)
        game = games[id]['game']
        diff = games[id]['diff']
        best_move = None
        gg = "Your turn"
        if not game.is_game_over() and game.turn == chess.BLACK:
            best_move, _ = ai.minimax(game, diff, float('-inf'), float('inf'), True)
            game.push(best_move)
        if game.is_game_over():
            gg = "Gameover."
            games.pop(id)
        return JsonResponse({'board': to2d(game), "message": 'Last move of AI: ' + best_move.__str__() if best_move else '' + '\n' + gg}, status=200)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

@csrf_exempt  # Add this decorator for POST requests if CSRF protection is enabled
def join_game(request):
    if request.method == 'POST':
        number = json.loads(request.body).get('number')
        if number not in games:
            games[number] = {'game': None}
            t = 5
            while t > 0:
                time.sleep(6)
                t -= 1
                if games[number]['game']:
                    side = not games[number]['p2']
                    return JsonResponse({'board': to2d(games[number]['game']), 'side': side}, status=200)
            games.pop(number)
            return JsonResponse({'error': 'Timeout waiting for another player'}, status=500)
        else:
            if games[number]['game']:
                return JsonResponse({'error': 'Room is not available'}, status=500)
            else:
                game = chess.Board()
                games[number] = {'game': game, 'p2': chess.BLACK}
                return JsonResponse({'board': to2d(game), 'side': chess.BLACK}, status=200)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

waitlist = []
assigned = {}
def match():
    while len(waitlist) > 1:
        p1 = waitlist.pop()
        p2 = waitlist.pop()
        game_id = str(uuid.uuid4())
        game = chess.Board()
        games[game_id] = {'game': game, p1: chess.WHITE, p2: chess.BLACK}
        assigned[p1] = game_id
        assigned[p2] = game_id

@csrf_exempt
def find(request):
    if request.method == 'POST':
        number = uuid.uuid4()
        waitlist.append(number)
        t = 5
        while t > 0:
            time.sleep(6)
            t -= 1
            match()
            if number in assigned:
                print(games[assigned[number]])
                return JsonResponse({
                    'board': to2d(games[assigned[number]]['game']),
                    'side': games[assigned[number]][number],
                    'gameid': assigned[number]
                }, status=200)
        waitlist.remove(number)
        return JsonResponse({'error': 'Timeout waiting for another player'}, status=500)


def clear(request):
    if request.method == 'GET':
        print(games)
        time.sleep(1800)
        rm = []
        for i in games:
            if 'last' in games[i]:
                print(datetime.now().timestamp() - games[i]['last'])
                if datetime.now().timestamp() - games[i]['last'] > 900:
                    rm.append(i)
        for j in rm:
            games.pop(j)
        print(games)
        return JsonResponse({'message': 'rm'}, status=200)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)