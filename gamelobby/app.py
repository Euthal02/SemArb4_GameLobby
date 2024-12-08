from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, send_wildcard=True)
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}  # Speichert Spielerinformationen

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("join_lobby")
def join_lobby(data):
    name = data["name"]
    players[request.sid] = {"name": name, "score": 0}
    emit("update_players", list(players.values()), broadcast=True)

@socketio.on("join_game")
def join_game(data):
    name = data["name"]

@socketio.on("disconnect")
def disconnect():
    players.pop(request.sid, None)
    emit("update_players", list(players.values()), broadcast=True)

@socketio.on("update_score")
def update_score(data):
    if request.sid in players:
        players[request.sid]["score"] = data["score"]
    emit("update_players", list(players.values()), broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=80)
