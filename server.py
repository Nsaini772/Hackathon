from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Serve the frontend HTML
@app.route('/')
def index():
    return render_template('index.html') 

# Handle incoming offer from client
@socketio.on('offer')
def handle_offer(offer):
    print("Received offer:", offer)
    emit('offer', offer, broadcast=True)

# Handle incoming answer from client
@socketio.on('answer')
def handle_answer(answer):
    print("Received answer:", answer)
    emit('answer', answer, broadcast=True)

# Handle incoming ICE candidates from client
@socketio.on('ice-candidate')
def handle_ice_candidate(candidate):
    print("Received ICE candidate:", candidate)
    emit('ice-candidate', candidate, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

