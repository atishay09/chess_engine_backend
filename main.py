import chess
import chess.engine
import os
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    fen: str
    depth: int

dir = os.getcwd()
print(dir)

engine = chess.engine.SimpleEngine.popen_uci(r"app\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")


@app.post("/bot/")
def hello(data : Data):
    board = chess.Board(data.fen)
    if not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1,depth = data.depth))
        board.push(result.move)
        return {"fen":board,"move":result.move}
    else:
        return {"error":"Game is in Over State"}

@app.get("/")
async def hello2():
    return {"Data":"Success"}
    

# python -m uvicorn main:app --reload 
# to start uvicorn