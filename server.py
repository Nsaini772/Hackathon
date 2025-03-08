from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging
from google.cloud import speech
import base64

# Load API key from credit.json
client = speech.SpeechClient.from_service_account_file("etc/secrets/credit.json")

app = Flask(__name__)
socketio = SocketIO(app)

rooms = {}

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')
client = speech.SpeechClient()

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json['data']
    audio_content = base64.b64decode(data)

    # Prepare the audio for transcription
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )

    # Call Google's Voice to Text API
    response = client.recognize(config=config, audio=audio)

    # Process the API response
    transcription = response.results[0].alternatives[0].transcript if response.results else ''

    return jsonify({'transcription': transcription})

# Handle a new connection
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    rooms[request.sid] = room
    logging.info(f'Client {request.sid} joined room {room}')
    emit('join', {'sid': request.sid}, room=room)

# Handle disconnection
@socketio.on('disconnect')
def handle_disconnect():
    room = rooms.get(request.sid)
    if room:
        leave_room(room)
        del rooms[request.sid]
        logging.info(f'Client {request.sid} left room {room}')
        emit('leave', {'sid': request.sid}, room=room)

# Handle incoming offer from client
@socketio.on('offer')
def handle_offer(data):
    room = rooms.get(request.sid)
    if room:
        logging.info(f'Client {request.sid} sent offer to room {room}')
        emit('offer', data, room=room, include_self=False)

# Handle incoming answer from client
@socketio.on('answer')
def handle_answer(data):
    room = rooms.get(request.sid)
    if room:
        logging.info(f'Client {request.sid} sent answer to room {room}')
        emit('answer', data, room=room, include_self=False)

# Handle incoming ICE candidates from client
@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    room = rooms.get(request.sid)
    if room:
        logging.info(f'Client {request.sid} sent ICE candidate to room {room}')
        emit('ice-candidate', data, room=room, include_self=False)

if __name__ == '__main__':
    logging.info('Starting server on 0.0.0.0:5000')
    socketio.run(app, host='0.0.0.0', port=5000)
