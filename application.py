# application.py for Project2
# ---------------------------
# a Chat Room Application

# import packages
import os
from flask import render_template, request, redirect, url_for
from flask import Flask, session, jsonify
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
app.config['SESSION_TYPE'] = 'filesystem'
login = LoginManager(app)
Session(app)
socketio = SocketIO(app, manage_session=False)

users = {}
rooms = {}

# default route ----------------------------
@app.route("/")
def index():
    #session.clear()
    return render_template("index.html")

# signup route ------------------------------
@app.route('/signup', methods = ['POST'])
def signup():
    usern = request.form.get('name')
    print ("login: ", usern)
    session['username'] = usern
    return render_template("chatroom.html", username=usern)

# main -------------------------------------
if __name__ == "__main__":
    socketio.run(app, debug=True)
