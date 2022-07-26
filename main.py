from stockfish import Stockfish, StockfishException
import chess
from flask import Flask, jsonify, request


stockfish = Stockfish(parameters={"Threads": 1})

stockfish.set_elo_rating(1100)

# lookup game array by gameId
gameLookup={}

def callStockfish(game):
    stockfish.set_position(game)
    while True:
        try:
            return stockfish.get_best_move()
        except StockfishException:
            print("AAAAA")
            pass

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
        elif board.is_insufficient_material():
            return "Insufficient material for forced checkmate. STALEMATE!!! Restarting."
        elif not stockfish.is_fen_valid(fen):
            return "move is valid but board isn't??????"


        # AIMove=stockfish.get_best_move()
        AIMove=callStockfish(game)
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
        elif board.is_insufficient_material():
            return "Insufficient material for forced checkmate. STALEMATE!!! Restarting."
        elif not stockfish.is_fen_valid(fen):
            return "move is valid but board isn't??????"

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
        return jsonify({'data': "Invalid Request. Must provide a unique userId and valid move. Example of valid first move: /?userId=upitroma&move=e2e3"}), 400
    gameId = args.get("userId")
    
    if not args.get("move"):
        return jsonify({'data': "Invalid Request. Must provide a unique userId and valid move. Example of valid first move: /?userId=upitroma&move=e2e3"}), 400
    playerMove = args.get("move")

    move = getMove(gameId,playerMove)
    

    return jsonify({'data': move}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')  
