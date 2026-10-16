import sqlite3 as sql
from pathlib import Path
from flask import Flask, render_template, redirect, url_for
import timeago
import time
from datetime import datetime

app = Flask(__name__)

folder = Path(__file__).resolve().parent
db = "forum.db"


def get_db():
    conn = sql.connect(folder/db)
    conn.row_factory = sql.Row
    conn.execute("pragma foreign_keys = on")
    return conn

def init_db():
    conn = get_db()

    conn.execute("""create table if not exists forum_posts (
    post_id integer primary key,
    posted_unix integer not null default (cast(unixepoch('subsec') * 1000 as integer)),
    original_poster text not null,
    title text not null,
    category text not null default 'General' check(category in ('Announcements', 'Help', 'Showcase', 'Resources', 'General', 'Forum Feedback')),
    solved integer not null default 0 check(solved in (0, 1))
    )""")
    conn.execute("""create table if not exists forum_comments (
    comment_id integer primary key,
    post_id integer not null,
    posted_unix integer not null default (cast(unixepoch('subsec') * 1000 as integer)),
    author text not null,
    body text not null,
    solution integer not null default 0 check(solution in (0, 1)),
    foreign key (post_id) references forum_posts (post_id)
    )""")
    conn.execute("create unique index if not exists single_solution on forum_comments (post_id) where solution = 1")

    conn.commit()
    conn.close()

init_db()

def time_ago(ms_unix):
    if not ms_unix:
        return ""

    past_date = datetime.fromtimestamp(ms_unix/1000)
    now = datetime.now()

    return timeago.format(past_date, now)

@app.route("/home")
def to_home():
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/community")
def community():
    return redirect(url_for("forum"))

@app.route("/forum")
def forum():
    conn = get_db()
    posts = conn.execute("""select p.*, count(c.comment_id) as reply_count, max(c.posted_unix) as active_unix
    from forum_posts p
    left join forum_comments c on p.post_id = c.post_id
    group by p.post_id order by post_id desc limit 30""").fetchall()
    conn.close()

    for post in posts:
        post["time_ago"] = time_ago(post["posted_unix"])

    return render_template("forum.html", posts=posts, min_post=posts[-1] if posts else None, max_post=posts[0] if posts else None)

@app.route("/forum/post/<int:pid>")
def view_forum_post():
    return pid

@app.route("/releases")
def download_page():
    return "hi 2"

@app.route("/changelogs")
def changelogs():
    return "hi 3"

if __name__ == "__main__":
    app.run(debug=True)