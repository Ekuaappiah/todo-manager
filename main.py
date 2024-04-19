from flask import Flask, jsonify, render_template, request,redirect , url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lists.db'
db = SQLAlchemy()
db.init_app(app)


class Task(db.Model):
    id = mapped_column(Integer, primary_key=True)
    task_name = mapped_column(String(50))
    description = mapped_column(String(50))
    due_date = mapped_column(String(50))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    tasks = db.session.execute(db.select(Task)).scalars()
    return render_template("index.html", tasks=tasks)


@app.route("/add-task", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        task = Task(
            task_name = request.form['task-name'],
            description = request.form['description'],
            due_date = request.form['due-date']
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit-task/<int:task_id>", methods=['GET','POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.task_name = request.form['task-name']
        task.description = request.form['description']
        task.due_date = request.form['due-date']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit_task.html", task=task)


@app.route("/delete-task/<int:task_id>", methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)


