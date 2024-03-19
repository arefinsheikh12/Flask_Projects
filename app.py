from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Arefin Sheikh/Desktop/Projects/Todo2/test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.DateTime, nullable=True)
    tasks_to_be_done = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Todo %r>' % self.id

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def Task():
    if request.method == 'POST':
        date_str = request.form['date']
        time_str = request.form['time']
        task_content = request.form['tasks_to_be_done']
        completed = bool(request.form.get('completed'))
        

    # Convert date and time strings to datetime object
        
        date = datetime.strptime(date_str, '%Y-%m-%d')
        time = datetime.strptime(time_str, '%H:%M')

        new_task = Todo(date=date, time=time, tasks_to_be_done=task_content, completed=completed)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') 
        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date, Todo.time).all()
        print(type(tasks))
        return render_template('Task.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.tasks_to_be_done = request.form['tasks_to_be_done']
        # Update the completion status based on checkbox input
        task.completed = 'completed' in request.form
        

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
    
if __name__ == "__main__":
    app.run(debug=True)
