from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

# Display a task


@app.route('/', methods=['GET', 'POST'])
def home():
    # Get all tasks from the database
    tasks = Task.query.all()

    # Render the index.html template and pass the tasks to it
    return render_template('index.html', tasks=tasks)

# Add a task


@app.route('/add', methods=['POST'])
def add_task():
    # Get the title of the new task from the POST request
    title = request.form.get('title')

    # Create a new task with the title
    new_task = Task(title=title)

    # Add the new task to the database
    db.session.add(new_task)

    # Commit the changes
    db.session.commit()

    # Redirect the user to the home page after adding the task
    return redirect(url_for('home'))

# Delete a task


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Get the task with the given id
    task = Task.query.get(task_id)

    # Delete the task from the database
    db.session.delete(task)

    # Commit the changes
    db.session.commit()

    # Redirect the user to the home page after deleting the task
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
