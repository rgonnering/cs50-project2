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

users = ['anonymous']
rooms = []
user = {"username": 'anonymous', "chatroom": "Open Forum"}



# default route ----------------------------
@app.route("/")
def index():
    global rooms
    # session setup
    print(session)
    if 'username' not in session:
        #usern = user['username']
        #room = user['chatroom']
        session['username'] = 'anonymous'
        print("index1a: username not in session")
    if 'chatroom' not in session:
        session['chatroom'] = "Open Forum"
        print("index1b: chatroom not in session")        
    if 'users' not in session:
        session['users'] = ['anonymous']
        print("index1c: users not in session")
    if 'rooms' not in session:
        session['rooms'] = ['Open Forum']
        rooms = ['Open Forum']
        print("index1d: rooms not in session")   
    if session['username'] not in session['users']:
        session['users'].append(session['username'])
    if session['chatroom'] not in session['rooms']:
        session['rooms'].append(session['chatroom'])  
    rooms = session['rooms']

    print("index2: user:", session['username'], "room:", session['chatroom'])
    print("index3: users:", session['users'], "rooms:", session['rooms'], rooms)
    return render_template("index.html")


# signin route ------------------------------
@app.route('/signin')
def signin():
    usern = session['username']
    print("signin", usern)
    return render_template("signin.html", user=usern)


# signup route ------------------------------
@app.route('/signup', methods = ['POST'])
def signup():
    global rooms
    usern = request.form.get('name')
    print('signup1a: usern=', usern, "users=", session['users'])
    if usern:
        print("su1")
        if usern not in session['users']:
            print("su2", session['users'])
            session['users'].append(usern)
            print("su3", session['users'])
    else:
        usern = 'anonymous'
    session['username'] = usern
    user = usern
    room = session['chatroom']
    users = session['users']
    rooms = session['rooms']
    print("s2: user:", session['username'], "room:", session['chatroom'])
    print("signup3: users:", session['users'], "rooms:", session['rooms'], rooms)
    return render_template("chatroom.html", user=user, room=room, users=users, rooms=rooms)


# signout route ------------------------------
@app.route('/signout')
def signout():
    global rooms
    rooms = session['rooms']
    user = session['username']
    msg = "You can continue as anonymous."
    print("signout1 user=", user, "users=", session['users'], "rooms=", rooms )
    if user != 'anonymous':
        session['users'].remove(user)
        msg = "You are signed out."
        print(msg)

    usern = 'anonymous'
    session['username'] = usern
    print("signout2 user=", usern, "users=", session['users'], session['rooms'], rooms, msg )
    return render_template("signout.html", username=session['username'], msg=msg)


# chatroom ------------------------------
@app.route('/chatroom', methods=['GET','POST'])
def chatroom():
    global rooms   #, users, user
    chatroom = session['chatroom']
    if request.method == 'POST':
        # Existing Chat Room
        existingRoom = request.form.get("select")
        # New Chat Room
        newChatRoom = request.form.get('newChatRoom')
        if existingRoom:
            chatroom = existingRoom
            print ("chatroom1: rooms=", existingRoom, rooms)
        elif newChatRoom:
            if newChatRoom not in session['rooms']:
                session['rooms'].append(newChatRoom)
            if newChatRoom not in rooms:
                rooms.append(newChatRoom)
            chatroom = newChatRoom
            print ("chatroom2: rooms=", session['rooms'], rooms)
    session['chatroom'] = chatroom
    print("chatroom4: chatroom=", chatroom, " rooms=", session['rooms'], rooms)
    #return render_template("chatroom.html", user=session['username'], room=session['chatroom'], users=session['users'], rooms=session['rooms'])
    return render_template("chatroom.html", user=session['username'], room=session['chatroom'], users=session['users'], rooms=rooms)


# chat ----------------------------------
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    usern = session['username']
    room = session['chatroom']
    print("chat: user=", usern, "room=", room, "rooms=", session['rooms'], rooms)
    return render_template("chat.html", user=usern, chatroom=room)

def messageReceived():
    print ('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    print("socketio.on: str(json) = ", str(json))
    #if json[message] == "":
    #    print ("my_event: No message" )
    socketio.emit('my response', json, callback=messageReceived)


# reset route ------------------------------
@app.route('/reset')
def reset():
    global rooms
    session['username'] = 'anonymous'
    session['chatroom'] = "Open Forum"
    session['users'] = ['anonymous']
    session['rooms'] = ['Open Forum']
    rooms  = ['Open Forum']
    print("reset: user:", session['username'], "room:", session['chatroom'])
    print("reset: users:", session['users'], "rooms:", session['rooms'], rooms)
    return render_template("index.html", username=session['username'], chatroom=session['chatroom'])


# main -------------------------------------
if __name__ == "__main__":
    socketio.run(app, debug=True)
