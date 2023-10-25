from app import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(64), unique=True, nullable=False)
    steps = db.relationship('Steps', backref='profile', lazy='dynamic')

class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_description = db.Column(db.String(128), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

