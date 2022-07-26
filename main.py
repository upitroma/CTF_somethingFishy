from stockfish import Stockfish
import chess
from flask import Flask, jsonify, request


stockfish = Stockfish(parameters={"Threads": 2})
stockfish.set_elo_rating(1100)


# lookup game array by gameId
gameLookup={}


def getMove(gameId,playerMove):
    if gameId not in gameLookup:
        gameLookup[gameId] = []


    game=gameLookup[gameId]
    stockfish.set_position(game)

    if stockfish.is_move_correct(playerMove):
        game.append(playerMove)
        stockfish.set_position(game)

        # check for checkmate and stalemate
        fen=stockfish.get_fen_position()
        board = chess.Board(fen)
        if board.is_checkmate():
            if board.outcome().winner:
                return "YOU WIN!!! TECH-FLAG-42069"
            else:
                gameLookup[gameId] = []
                return "YOU LOSE!!! Restarting."

        AIMove=stockfish.get_best_move_time(1000)
        game.append(AIMove)

        stockfish.set_position(game)

        # check for checkmate and stalemate
        fen=stockfish.get_fen_position()
        board = chess.Board(fen)
        if board.is_checkmate():
            if board.outcome().winner:
                return "YOU WIN!!!"
            else:
                gameLookup[gameId] = []
                return "YOU LOSE!!! Restarting."


        return AIMove
    else:
        gameLookup[gameId]=[]
        return "Invalid Move. Restarting."



app = Flask(__name__)
@app.route("/")
def home():
    if(request.method != 'GET'):
        return jsonify({'data': "Invalid Request. Must be GET."}), 400

    args = request.args
    if not args.get("userId"):
        return jsonify({'data': "Invalid Request. Must provide a unique userId and valid move"}), 400
    gameId = args.get("userId")
    
    if not args.get("move"):
        return jsonify({'data': "Invalid Request. Must provide a unique userId and valid move"}), 400
    playerMove = args.get("move")

    move = getMove(gameId,playerMove)
    

    return jsonify({'data': move}), 200


if __name__ == '__main__':
    app.run()  

# getMove(1,"")
# # get player move
# getMove(1,input())