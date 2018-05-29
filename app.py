from flask import Flask, render_template, request
from flask_socketio import SocketIO
import json
from random import randint

tokensAndUsers = {}
games = {}
users = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return render_template('client.html')


@app.route('/game')
def profile():
    token = request.args['token']
    sid = request.args["sid"]
    userGame = users[token]
    if userGame['user1'] == sid:
        toUser = userGame['user1']
    else:
        toUser = userGame['user2']
    socketio.emit("ready", room=toUser)
    return render_template("client.html", token=token)


@socketio.on('createGame')
def createGame(clientData):
    users[clientData["token"]] = {"game": clientData["game"],
                                  "user1": clientData["user1"],
                                  "user2": ""
                                  }


@socketio.on('newConnection')
def generateToken(sid):
    token = tokenGenerator()
    tokensAndUsers[token] = {"user1": sid,
                             "user2": ""}
    socketio.emit('sendToken', token, room=sid)


@socketio.on('getGame')
def getGame(data):
    game = users[data["token"]]
    users[data["token"]]["user2"] = data["sid"]
    socketio.emit('sendGame', game, room=data["sid"])


@socketio.on('move')
def message(moveData):
    fromUser = moveData["sid"]
    token = moveData['token']
    move = moveData["move"]
    userGame = users[token]
    print("-------------", userGame)
    if userGame['user1'] == fromUser:
        toUser = userGame['user2']
    else:
        toUser = userGame['user1']
    socketio.emit('move', move, room=toUser)


@socketio.on('leave')
def deleteClientFromClientDict(token):
    user1 = users[token]["user1"]
    user2 = users[token]["user2"]
    socketio.emit('redirect', {'url': "http://192.168.16.100:8000/"}, room=user1)
    socketio.emit('redirect', {'url': "http://192.168.16.100:8000/"}, room=user2)


@socketio.on('disconnected')
def deleteClientFromClientDict(data):
    print("---------------", data)


def tokenGenerator():
    stringLength = 30

    stringArray = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                   'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                   'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                   'Y', 'Z', '!', '?']
    rndString = ""

    for i in range(1, stringLength):
        rndNum = randint(0, stringLength - 1)
        rndString = rndString + stringArray[rndNum]

    return rndString


if __name__ == '__main__':
    socketio.run(app, "192.168.16.100", 8000, debug=True)
