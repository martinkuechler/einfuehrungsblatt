from fastapi import FastAPI
from fastapi.responses import FileResponse
import datetime

app = FastAPI()

@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.get("/api/ping")
async def ping() -> dict:
    datum = datetime.datetime.now().isoformat()
    return {"status": "ok" , "time": datum}


@app.post("/api/pong")
async def pong() -> str:
        print("pong received")   # <-- loggt ins Server-Log
        return ""
        

