from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import chess.pgn

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@app.get("/games")
async def list_games():
    """Lists all available PGN games in the data directory."""
    if not os.path.exists(DATA_DIR):
        return []
    
    games = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pgn"):
            games.append(filename)
    return games

@app.get("/games/{filename}")
async def get_game(filename: str):
    """Fetches details and moves for a specific PGN game."""
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        with open(file_path, "r") as pgn_file:
            pgn = chess.pgn.read_game(pgn_file)
            if pgn is None:
                raise HTTPException(status_code=400, detail="Invalid PGN file")
            
            # Extract metadata
            metadata = {
                "headers": {key: value for key, value in pgn.headers.items()},
                "moves": []
            }
            
            # Extract moves in SAN format
            board = chess.Board()
            for move in pgn.mainline_moves():
                metadata["moves"].append(board.san(move))
                board.push(move)
                
            return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
