from pathlib import Path

basedir = Path(__file__).parent.resolve()

class Config(object):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'app.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 
