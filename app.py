import sqlite3 as sql
from pathlib import Path
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

folder = Path(__file__).resolve().parent
db = "forum.db"

def get_db():
    conn = sql.connect(folder/db)
    conn.row_factory = sql.Row
    return conn

@app.route("/home")
def to_home():
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/forum")
def forum():
    return "hi"

@app.route("/releases")
def download_page():
    return "hi 2"

@app.route("/changelogs")
def changelogs():
    return "hi 3"

if __name__ == "__main__":
    app.run(debug=True)