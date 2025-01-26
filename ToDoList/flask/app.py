from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Home route: Displays the todo list
@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        data = Todo(title=todo_title, desc=todo_desc)
        db.session.add(data)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", allTodo=alltodo)

# Route to handle form submission
@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    desc = request.form.get("desc")
    todo = Todo(title=title, desc=desc)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("hello_world"))

# Route to show all todos in the console
@app.route("/delete/<int:sno>", methods=["GET", "POST"])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("hello_world"))

# Route to update the todo task
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for("hello_world"))
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True)
