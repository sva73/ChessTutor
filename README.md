# ChessTutor

A professional web application for managing and analyzing chess games in PGN format.

## Features

- **Game Management**: Browse available PGN games in the data directory.
- **Visual Analysis**: High-quality chess board representation using `chessground`.
- **Interactive Playback**: Navigate through game moves using the board controls or the move notation list.
- **Tech Stack**:
  - **Frontend**: Vue 3 (TypeScript), Tailwind CSS, Vite.
    - **Backend**: Python (FastAPI), python-chess.
  - **Chess Engine Integration**: Uses `chess.js` and `chessground` for board logic and rendering.

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js & npm

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd ChessTutor/backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   python main.py
   ```
   The server will run on `http://127.0.0.1:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ChessTutor/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173` (or the port shown in your terminal).

## Project Structure

- `ChessTutor/backend/`: FastAPI application.
- `ChessTutor/frontend/`: Vue.js application.
- `ChessTutor/data/`: Directory containing `.pgn` files for analysis.
- `ChessTutor/README.md`: Project documentation.

## License

MIT