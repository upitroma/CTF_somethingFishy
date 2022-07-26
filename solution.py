#!/usr/bin/python3

# 1. install stockfish on your system
# 2. pip3 install stockfish requests
# 3. ./solution.py

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

    # isn't required but cool to look at
    stockfish.set_position(game)
    print(stockfish.get_board_visual())

    OpponentMove=sendWebRequest(AIMove)
    print("Opponent move: "+OpponentMove)
    game.append(OpponentMove)

    stockfish.set_position(game)

    # isn't required but cool to look at
    print(stockfish.get_board_visual())
