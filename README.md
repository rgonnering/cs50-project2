# Project 2

Web Programming with Python and JavaScript

A Flask Chat Application with SocketIO

To start:
    flask environment
    -----------------
    $ conda activate flask
    (flask) $ export FLASK_APP=application.py
    (flask) $ echo $FLASK_APP
        application.py
    (flask) $ export FLASK_DEBUG=1
    (flask) $ echo $FLASK_DEBUG
        1

Makesure ALL dependencies are installed
Run 
    (flask) $ pip3 install -r requirements.txt

Run flask
---------
    (flask) $ cd /path/folder_with_application.py
    (flask) $ flask run
        browser: 127.0.0.1:5000
OR
    (flask) $ flask run --host=0.0.0.0
        browser: http://192.168.1.3:5000/

git
---
(flask) $ git status
(flask) $ git add .
(flask) $ git status
(flask) $ git commit -m "firstchat chat works"
(flask) $ git push origin master


passing a variable from python to javascript
python:
    return render_template("chat.html", user=user, room=room)
javascript:
    // variable needs back quote
    var usern = `{{user}}
