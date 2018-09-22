from appFolder import db, login_mangager
from datetime import datetime
from flask_login import UserMixin

@login_mangager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(40), nullable=False)
    last_login = db.Column(db.DateTime, nullable=False, default =  datetime.now())

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(20), nullable = False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Logs('{self.activity}', '{self.message}', '{self.timestamp}')"

class User_Id_Store(db.Model):
    store = db.Column(db.Integer,primary_key=True)

