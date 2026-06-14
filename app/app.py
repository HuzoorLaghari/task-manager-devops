from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "database/tasks.db"


# -----------------------------
# Database Initialization
# -----------------------------
def init_db():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    )

    tasks = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks
    )


# -----------------------------
# Add Task
# -----------------------------
@app.route("/add", methods=["POST"])
def add_task():

    title = request.form["title"]

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(title) VALUES (?)",
        (title,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -----------------------------
# Complete Task
# -----------------------------
@app.route("/complete/<int:id>")
def complete_task(id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -----------------------------
# Delete Task
# -----------------------------
@app.route("/delete/<int:id>")
def delete_task(id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -----------------------------
# Start Application
# -----------------------------
if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
