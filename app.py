from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Yt comment fix
with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting task'    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_content = request.form['content']
        task_to_update.content = task_content

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error updating task'
    else:
        return render_template('update.html', task=task_to_update)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        stmt = db.select(Todo.content).where(Todo.content.contains("Python"))
        result = db.session.execute(stmt).scalars().all()
        return render_template('search.html', result=result)
    
    else:
        return render_template('search.html')
        

    
if __name__ == "__main__": 
    app.run(debug=True)