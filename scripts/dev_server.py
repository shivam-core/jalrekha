"""Local-only static mounting; production uses Vercel's public directory."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[1]/"public", html=True))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
