from app import create_app, db

app = create_app()

@app.cli.command('init_db')
def init_db():
    db.create_all()

if __name__ == '__main__':
    app.run()

