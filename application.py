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
rooms = ['Open Forum']
user = 'anonymous'
room = 'Open Forum'

# default route ----------------------------
@app.route("/")
def index():
    #session.clear()
    print("index")
    return render_template("index.html")

# signin route ------------------------------
@app.route('/signin')
def signin():
    global user
    print("signin", user)
    return render_template("signin.html", user=user)

# signup route ------------------------------
@app.route('/signup', methods = ['POST'])
def signup():
    global users
    global user
    print('signup1: ', users, rooms)
    usern = request.form.get('name')
    print('signup1a: usern=', usern, "users=", users)
    if usern:
        print("su1")
        if usern not in users:
            
            print("su2", users)
            users.append(usern)
            print("su3", users)
    else:
        usern = 'anonymous'
        
    session['username'] = usern
    user = usern
    print ("signup2: user=", user, "usern=", usern, "users=",users, session['username'])
    print ("signup3: rooms=", rooms, "room=", room)
    return render_template("chatroom.html", user=user, room=room, users=users, rooms=rooms)

# signout route ------------------------------
@app.route('/signout')
def signout():
    global user
    global users
    msg = "You can continue as anonymous."
    print("signout1 user=", user, "users=", users, rooms )
    if user != 'anonymous':
        users.remove(user)
        msg = "You are signed out."
        print(msg)
    print(msg)
    user = 'anonymous'
    print("signout2 user=", user, "users=", users, rooms, msg )
    return render_template("signout.html", username=user, msg=msg)

# chatroom ------------------------------
@app.route('/chatroom', methods=['GET','POST'])
def chatroom():
    global room
    if request.method == 'POST':

        # Selected Existing Chat Room
        existingRoom = request.form.get("select")
        newChatRoom = request.form.get('newChatRoom')
        if existingRoom:
            chatroom = existingRoom
            print ("chatroom1: rooms=", existingRoom, rooms)
        elif newChatRoom:
            rooms.append(newChatRoom)
            chatroom = newChatRoom
            print ("chatroom2: rooms=", newChatRoom, rooms)
        else:
            chatroom = room
            print ("chatroom3: chatroom=",  chatroom, " rooms=", rooms)
        room =  chatroom

    else:
        print("chatroom4: chatroom=", room, " rooms=", rooms)
    return render_template("chatroom.html", user=user, room=room, users=users, rooms=rooms)


# chat ----------------------------------
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    print("chat: user=", user, "room=", room,)
    return render_template("chat.html", user=user, room=room)
    #return render_template("chat.html", user=user, room=room, msg=msg)


#def messageReceived(methods=['GET', 'POST']):
def messageReceived():
    print ('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    print("socketio.on: str(json) = ", str(json))
    socketio.emit('my response', json, callback=messageReceived)




# main -------------------------------------
if __name__ == "__main__":
    socketio.run(app, debug=True)
