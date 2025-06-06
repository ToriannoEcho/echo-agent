from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)
DB_URL = os.environ.get("DATABASE_URL")

@app.route("/")
def home():
    return "Echo Agent is online."

@app.route("/memory", methods=["POST"])
def save_memory():
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
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT note FROM memory;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([row[0] for row in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)