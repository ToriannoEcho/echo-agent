from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import psycopg2
import os

app = FastAPI()
DB_URL = os.environ.get("DATABASE_URL")


@app.get("/")
async def home():
    return {"message": "Echo Agent is online."}


@app.post("/memory")
async def save_memory(request: Request):
    data = await request.json()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS memory (id SERIAL PRIMARY KEY, note TEXT);")
    cur.execute("INSERT INTO memory (note) VALUES (%s);", (data["note"],))
    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse({"status": "saved"})


@app.get("/memory")
async def get_memory():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT note FROM memory;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": [row[0] for row in rows]}
