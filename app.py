from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

def get_db():
    return sqlite3.connect("todo.db")

@app.route("/")
def index():
    db = get_db() 
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]

    if len(task) > 0 and len(task) < 200:
        db = get_db()
        db.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        db.commit()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id=?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
    db.commit()

    app.run(host="0.0.0.0", port=5000)
