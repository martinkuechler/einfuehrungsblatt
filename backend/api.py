from fastapi import FastAPI
import datetime

app = FastAPI()


@app.get("/")
async def root() -> str:
    return "You can visit yourLocalIP/api/ping or yourLocalIP/api/pong"


@app.get("/api/ping")
async def ping() -> dict:
    datum = datetime.datetime.now().isoformat()
    return {"status": "ok" , "time": datum}


@app.post("/api/pong")
async def pong() -> str:
    return "Pong"

