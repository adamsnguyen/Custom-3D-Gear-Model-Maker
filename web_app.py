from app import app, db
from app.models import User, Gear

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Gear': Gear}


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)