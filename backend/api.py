from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
import datetime
import sqlite3


app = FastAPI()
con=sqlite3.connect('todo.db', check_same_thread=False)
cur = con.cursor()

con.commit()

try:
    cur.execute("""
    CREATE TABLE todo(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
""")
    con.commit()

except:
    pass
print(cur.execute("SELECT * FROM todo").fetchall())




@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.get("/api/ping")
async def ping() -> dict:
    datum = datetime.datetime.now().isoformat()
    return {"status": "ok" , "time": datum}


@app.post("/api/pong")
async def pong() -> str:
        print("pong")   # <-- loggt ins Server-Log
        return ""
        
#aufgabe 2 ab hier
@app.post("/api/items")
async def create_item(request: Request):
     body=await request.json()
     body["id"] = int(body["id"])

     print(body)
     if "id" not in body or "title" not in body or "content" not in body:
         print("Fehlende Parameter")
         return "Fehlende Parameter"
     if cur.execute("SELECT * FROM todo WHERE id=?",(body["id"],)).fetchone() is not None:
         return(JSONResponse(status_code=409, content="Item mit dieser ID existiert bereits"))

     res=cur.execute("INSERT INTO todo VALUES (?,?,?,?)",(body["id"],body['title'],body['content'],datetime.datetime.now().isoformat()))
     print(res)
     con.commit()

     return ""

@app.get("/api/items")
async def get_items():
        items=cur.execute("SELECT * FROM todo").fetchall()
        result=[]
        for item in items:
            result.append({
                "id":item[0],
                "title":item[1],
                "content":item[2],
                "created_at":item[3]
            })
        return result

@app.get("/api/items/{id}")
async def get_item(id):
    item=cur.execute("SELECT * FROM todo WHERE id=?",(id,)).fetchone()
    if item is None:
        return JSONResponse(status_code=404, content="Item nicht gefunden")
    return {
        "id":item[0],
        "title":item[1],
        "content":item[2],
        "created_at":item[3]
    }

@app.delete("/api/items/{id}")
async def delete_item(id: int ):
     print("delete requested")
     cur.execute("DELETE FROM todo WHERE id=?",(id,))
     print("rows deleted:", cur.rowcount)
     con.commit()
     return ""
    
     


     