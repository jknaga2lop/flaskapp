from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Given and inferred columns
    profile_name = db.Column(db.String(60), nullable=False)
    program_no = db.Column(db.Integer)
    program_id = db.Column(db.String)
    revision_number = db.Column(db.Integer)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    acid_fill_type = db.Column(db.String)
    total_time = db.Column(db.Float)
    total_ah = db.Column(db.Float)
    preparer = db.Column(db.String)
    checker = db.Column(db.String)
    approver = db.Column(db.String)
    controller = db.Column(db.String)
    steps = db.relationship('Step', back_populates='profile', lazy='dynamic')

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Columns for the Step model
    step_process = db.Column(db.String, nullable=False)   # (1) Named as 'step_process' to avoid naming conflict with 'step' method
    current = db.Column(db.Float)                         # (3) Assuming float for decimal precision
    time = db.Column(db.Float)                            # (4) Assuming float for duration in hours/minutes
    ah_step = db.Column(db.Float)                         # (5) AH/step
    cumulative_ah = db.Column(db.Float)                   # (6)
    
    # Foreign Key to link Step with Profile
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    
    # Relationship to reference the associated Profile object from a Step object
    profile = db.relationship('Profile', back_populates='steps')

@app.route('/', methods=['POST','GET'])
def home():
    current_date = datetime.today().strftime('%Y-%m-%d')
    return render_template("index.html", current_date=current_date)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
