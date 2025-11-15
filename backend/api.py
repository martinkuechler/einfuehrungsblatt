from fastapi import FastAPI, Request
from fastapi.responses import FileResponse   # Ermöglicht, Dateien als HTTP-Antworten zurückzugeben.
from fastapi.responses import JSONResponse   # Ermöglicht, JSON-Antworten mit benutzerdefiniertem Statuscode zu senden.
import datetime
import sqlite3

from fastapi.middleware.cors import CORSMiddleware #New

app = FastAPI()
con = sqlite3.connect('todo.db', check_same_thread=False)  # check_same_thread=False erlaubt Thread-übergreifenden Zugriff.



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cur = con.cursor()                           # Erstellt einen Cursor, um SQL-Befehle auszuführen.

con.commit()                                 # Speichert eventuelle Änderungen (hier redundant, aber unproblematisch).

try:
    cur.execute("""                           # Führt SQL-Befehl aus, um Tabelle 'todo' zu erstellen, falls sie nicht existiert.
    CREATE TABLE todo(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,                  # Titel des Eintrags.
        content TEXT NOT NULL,                # Beschreibung oder Inhalt des Eintrags.
        created_at TEXT NOT NULL              # Zeitstempel der Erstellung.
    )
""")
    con.commit()

except:                                       # Wenn die Tabelle bereits existiert, wird der Fehler ignoriert.
    pass
print(cur.execute("SELECT * FROM todo").fetchall())  # Gibt existierende Daten aus der Tabelle aus (zu Debug-Zwecken).

#--------------------------------------


@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.get("/api/ping")
async def ping() -> dict:
    datum = datetime.datetime.now().isoformat()
    return {"status": "ok", "time": datum}

@app.post("/api/pong")                       #
async def pong() -> str:
    print("pong")
    return ""


# Aufgabe 2 ab hier
@app.post("/api/items")                      # Definiert eine POST-Route zum Erstellen eines neuen ToDo-Eintrags.
async def create_item(request: Request):
    body = await request.json()               # Liest den JSON-Body aus der Anfrage.
    body["id"] = int(body["id"])              # Wandelt die ID in einen Integer um.

    print(body)                               # Gibt den empfangenen Body im Terminal aus.
    if "id" not in body or "title" not in body or "content" not in body:  # Prüft, ob alle Parameter vorhanden sind.
        print("Fehlende Parameter")           # Loggt Hinweis bei fehlenden Parametern.
        return "Fehlende Parameter"           # Gibt eine Fehlermeldung zurück.

    if cur.execute("SELECT * FROM todo WHERE id=?",(body["id"],)).fetchone() is not None:  # Prüft, ob ID schon existiert.
        return JSONResponse(status_code=409, content="Item mit dieser ID existiert bereits")  # Gibt Fehler 409 (Konflikt) zurück.

    res = cur.execute(                        # Führt SQL-INSERT aus, um einen neuen Eintrag hinzuzufügen.
        "INSERT INTO todo VALUES (?,?,?,?)",
        (body["id"], body['title'], body['content'], datetime.datetime.now().isoformat())
    )
    print(res)                                # Gibt das Ergebnis des INSERT-Befehls aus.
    con.commit()                              # Speichert die Änderung in der Datenbank.

    return ""                                 # Gibt leere Antwort zurück (könnte optional JSON mit Erfolgsmeldung sein).

@app.get("/api/items")                       # Definiert GET-Route, um alle Einträge abzurufen.
async def get_items():
    items = cur.execute("SELECT * FROM todo").fetchall()   # Holt alle Einträge aus der Datenbank.
    result = []                              # Erstellt eine leere Liste für formatierten Output.
    for item in items:                       # Iteriert über alle Datenbankzeilen.
        result.append({
            "id": item[0],
            "title": item[1],
            "content": item[2],
            "created_at": item[3]
        })
    return result                             # Gibt die Liste als JSON-Antwort zurück.

@app.get("/api/items/{id}")                  # Definiert GET-Route, um einen Eintrag nach ID zu holen.
async def get_item(id):
    item = cur.execute("SELECT * FROM todo WHERE id=?",(id,)).fetchone()  # Holt den Eintrag mit passender ID.
    if item is None:                         # Prüft, ob es keinen Eintrag gibt.
        return JSONResponse(status_code=404, content="Item nicht gefunden")  # Antwort: 404 Fehler.
    return {                                 # Gibt den Eintrag als Dictionary zurück.
        "id": item[0],
        "title": item[1],
        "content": item[2],
        "created_at": item[3]
    }

@app.delete("/api/items/{id}")               # Definiert DELETE-Route, um einen Eintrag nach ID zu löschen.
async def delete_item(id: int):
    print("delete requested")                # Loggt den Löschvorgang.
    cur.execute("DELETE FROM todo WHERE id=?",(id,))  # Führt SQL-DELETE aus.
    print("rows deleted:", cur.rowcount)     # Gibt aus, wie viele Zeilen gelöscht wurden.
    con.commit()                             # Speichert Änderung dauerhaft.
    return ""                                # Gibt leere Antwort zurück.
