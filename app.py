"""JALREKHA's slim, stateless deployment entrypoint."""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
app = FastAPI(title="JALREKHA", version="0.1.0")
@app.get("/")
def index():
    return RedirectResponse("/index.html")
@app.get("/api/health")
def health():
    return {"status": "ok", "schema_version": "1", "mode": "synthetic compatibility fixture"}
@app.get("/api/scenario")
def scenario():
    return {"mode": "synthetic compatibility fixture", "population": 100, "allocated": 80, "unallocated": 20}
