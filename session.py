from flask import Flask 
from flask_session import Session


app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

def login_user(user):
    