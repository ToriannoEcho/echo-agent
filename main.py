from flask import Flask, request, jsonify, abort
import psycopg2
import os

app = Flask(__name__)
DB_URL = os.environ.get("DATABASE_URL")
API_SECRET = os.environ.get("API_SECRET")

def check_auth():
    if request.headers.get("x-api-key") != API_SECRET:
        abort(403)

@app.route("/")
def home():
    check_auth()
    return "Echo Agent is online."

@app.route("/memory", methods=["POST"])
def save_memory():
    check_auth()
    data = request.json
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS memory (id SERIAL PRIMARY KEY, note TEXT);")
    cur.execute("INSERT INTO memory (note) VALUES (%s);", (data["note"],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "saved"})

@app.route("/memory", methods=["GET"])
def get_memory():
    check_auth()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT note FROM memory;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([row[0] for row in rows])
