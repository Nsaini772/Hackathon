from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

# Store the room information
rooms = {}

# Serve the frontend HTML
@app.route('/')
def index():
    return render_template('index.html')

# Handle a new connection
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    rooms[request.sid] = room
    emit('join', {'sid': request.sid}, room=room)

# Handle disconnection
@socketio.on('disconnect')
def handle_disconnect():
    room = rooms.get(request.sid)
    if room:
        leave_room(room)
        del rooms[request.sid]
        emit('leave', {'sid': request.sid}, room=room)

# Handle incoming offer from client
@socketio.on('offer')
def handle_offer(data):
    room = rooms.get(request.sid)
    if room:
        emit('offer', data, room=room, include_self=False)

# Handle incoming answer from client
@socketio.on('answer')
def handle_answer(data):
    room = rooms.get(request.sid)
    if room:
        emit('answer', data, room=room, include_self=False)

# Handle incoming ICE candidates from client
@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    room = rooms.get(request.sid)
    if room:
        emit('ice-candidate', data, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

