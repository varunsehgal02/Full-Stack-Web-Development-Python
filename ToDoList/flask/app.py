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
@app.route("/")
def hello_world():
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
@app.route("/show")
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return "Check console for database content."

if __name__ == "__main__":
    app.run(debug=True)
