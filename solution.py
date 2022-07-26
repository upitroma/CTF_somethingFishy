from stockfish import Stockfish
import requests

stockfish = Stockfish(parameters={"Threads": 8})

stockfish.set_skill_level(20)

game=[]

stockfish.set_position(game)

  

    

def sendWebRequest(move):
    url="http://localhost:5000/?userId=upitroma&move="+move
    response = requests.get(url).json().get("data")
    return response



while True:
    AIMove=stockfish.get_best_move()
    print("My move: "+AIMove)
    game.append(AIMove)

    stockfish.set_position(game)
    print(stockfish.get_board_visual())

    OpponentMove=sendWebRequest(AIMove)
    print("Opponent move: "+OpponentMove)
    game.append(OpponentMove)

    stockfish.set_position(game)
    print(stockfish.get_board_visual())
