from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))

@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    selected_user = request.form.get("selected_user") if request.method == "POST" else (users[0].name if users else None)
    tasks = Task.query.join(User).filter(User.name == selected_user).all() if selected_user else []
    return render_template('index.html', users=users, selected_user=selected_user, tasks=tasks)

@app.route('/add_user', methods=['POST'])
def add_user():
    user_name = request.form.get('new_user')
    if user_name and not User.query.filter_by(name=user_name).first():
        new_user = User(name=user_name)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Task.query.get(id)
    task.name = request.form['name']
    task.description = request.form['description']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

