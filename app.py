from flask import Flask, render_template, url_for, request, redirect
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

@app.route('/edit/<int:profile_id>', methods=['GET', 'POST'])
def edit_profile(profile_id):
    # Get the profile by ID
    profile = Profile.query.get_or_404(profile_id)

    # If it's a POST request, that means the form has been submitted and we need to update our data
    if request.method == 'POST':
        # Update profile details (add more as needed)
        profile.profile_name = request.form.get('profile_name')
        profile.program_no = request.form.get('program_no')
        profile.program_id = request.form.get('program_id')
        # ... (include other fields if they are to be edited)

        # Commit changes
        db.session.commit()

        # Redirect back to home after editing
        return redirect(url_for('home'))

    # If it's a GET request, we just render the edit page
    steps = profile.steps.all()
    return render_template('edit.html', profile=profile, steps=steps)

@app.route('/delete/<int:profile_id>', methods=['GET'])
def delete_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    db.session.delete(profile)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/', methods=['POST','GET'])
def home():
    profiles = Profile.query.all()
    current_date = datetime.today().strftime('%Y-%m-%d')
    error_message = None  # Initialize an error message to None
    
    if request.method == 'POST':
        profile_name = request.form.get('profile_name')
        program_no = request.form.get('program_no')
        program_id = request.form.get('program_id')

        # Check for duplicate profile_name
        existing_profile = Profile.query.filter_by(profile_name=profile_name).first()
        if existing_profile:
            error_message = "A profile with that name already exists. Please use a different name."

        else:
            # Assuming the program_no should be an integer
            # Convert it to int, but provide a default value of None if conversion fails
            try:
                program_no = int(program_no)
            except (TypeError, ValueError):
                program_no = None

            new_profile = Profile(
                profile_name=profile_name,
                program_no=program_no,
                program_id=program_id,
                issue_date=datetime.today()  # Setting the current date for issue_date
            )
            
            db.session.add(new_profile)
            db.session.commit()
            return redirect(url_for('home'))  # Redirect to homepage after adding the new profile

    return render_template("index.html", current_date=current_date, profiles=profiles, error=error_message)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
