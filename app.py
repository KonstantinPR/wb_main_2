import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.secret_key = 'xyz1b9zs8erh8be1g8-vw4-1be89tsdfsdf4er1v'

#  to solve problems connection with SQLAlchemy > 1.4 in heroku
uri_old = os.getenv("DATABASE_URL")  # or other relevant config var
uri = os.environ.get('DATABASE_URL')
print(f"uri in __init__ {uri}")

if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri or 'postgresql://postgres:19862814@localhost:8000/wb_main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/add_user')
def add_user():
    new_user = User(username='new_user',
                    email='new_user@example.com',
                    email2='new_user@example.com',
                    email3='new_user@example.com')
    db.session.add(new_user)
    db.session.commit()

    return 'User added!'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    email2 = db.Column(db.String(120), index=True, unique=True)
    email3 = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


if __name__ == '__main__':
    app.run(debug=True)
