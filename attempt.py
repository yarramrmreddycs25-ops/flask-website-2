from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "messages.db")

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

def save_message(name, message):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, message FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/")
def root():
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()

        lines = [line.strip() for line in message.splitlines() if line.strip()]
        clean_message = "\n".join(lines)

        save_message(name, clean_message)

        return render_template("success.html", name=name)

    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")

        if user == ADMIN_USER and pw == ADMIN_PASS:
            session["admin"] = True
            return redirect("/messages")
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")

@app.route("/messages")
def messages():
    if not session.get("admin"):
        return redirect("/login")

    data = get_messages()
    return render_template("messages.html", messages=data)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
