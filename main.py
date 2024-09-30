# main.py

from flask import Flask, request, jsonify, session, redirect
from flask_socketio import SocketIO, join_room, leave_room, emit
from models.user import User
from models.chatroom import ChatRoom
from controllers.encryption_controller import EncryptionController
from controllers.moderation_controller import ModerationController
from services.redis_service import RedisService
from services.oauth_service import OAuthService
from utils.constants import ROLE_ADMIN, ROLE_MODERATOR, ROLE_JANITOR
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')
socketio = SocketIO(app)
redis_service = RedisService()
encryption_controller = EncryptionController()
moderation_controller = ModerationController(redis_service)
oauth_service = OAuthService(app)

# In-memory storage for chat rooms
chat_rooms = {}

@app.route('/')
def index():
    return "Welcome to the Secure Chat Application!"

@app.route('/login')
def login():
    return oauth_service.login()

@app.route('/authorize')
def authorize():
    return oauth_service.authorize()

@socketio.on('join')
def handle_join(data):
    """
    Handles a user joining a chat room.
    Expects data to contain 'room_id' and 'user_secret'.
    """
    room_id = data.get('room_id')
    user_secret = data.get('user_secret')

    # Check if user is globally banned
    tripcode = User.generate_tripcode(user_secret)
    if redis_service.get(f"global_banned:{tripcode}"):
        emit('error', {'message': 'You are banned from the chat application.'})
        return

    # Check if room exists or create it
    if room_id not in chat_rooms:
        chat_rooms[room_id] = ChatRoom(room_id)

    room = chat_rooms[room_id]

    # Check if user is banned in the room
    if redis_service.get(f"room:{room_id}:banned:{tripcode}"):
        emit('error', {'message': 'You are banned from this room.'})
        return

    # Create user and add to room
    user = User(user_secret)
    room.add_user(user)
    join_room(room_id)

    # Broadcast that a new user has joined
    emit('user_joined', {'mnemonic': user.mnemonic}, room=room_id)

@socketio.on('leave')
def handle_leave(data):
    """
    Handles a user leaving a chat room.
    Expects data to contain 'room_id' and 'user_secret'.
    """
    room_id = data.get('room_id')
    user_secret = data.get('user_secret')
    tripcode = User.generate_tripcode(user_secret)

    if room_id in chat_rooms:
        room = chat_rooms[room_id]
        user = next((u for u in room.users if u.tripcode == tripcode), None)
        if user:
            room.remove_user(user)
            leave_room(room_id)
            emit('user_left', {'mnemonic': user.mnemonic}, room=room_id)

@socketio.on('send_message')
def handle_send_message(data):
    """
    Handles sending a message to a chat room.
    Expects data to contain 'room_id', 'user_secret', 'nonce', and 'ciphertext'.
    """
    room_id = data.get('room_id')
    user_secret = data.get('user_secret')
    nonce = bytes.fromhex(data.get('nonce'))
    ciphertext_with_tag = bytes.fromhex(data.get('ciphertext'))

    tripcode = User.generate_tripcode(user_secret)

    # Check if user is muted or banned
    if redis_service.get(f"room:{room_id}:muted:{tripcode}"):
        emit('error', {'message': 'You are muted in this room.'})
        return
    if redis_service.get(f"room:{room_id}:banned:{tripcode}"):
        emit('error', {'message': 'You are banned from this room.'})
        return

    # Retrieve room
    if room_id not in chat_rooms:
        emit('error', {'message': 'Room does not exist.'})
        return
    room = chat_rooms[room_id]

    # Decrypt message (Note: According to assumptions, decryption is client-side.
    # Here, server just relays the encrypted message.)

    # Create message object
    message = Message(sender_tripcode=tripcode, content_encrypted=data.get('ciphertext'))
    room.broadcast_message(message)

    # Store message in Redis
    redis_service.hset(f"room:{room_id}:messages:{message.message_id}", "deleted", False)
    redis_service.set(f"room:{room_id}:messages:{message.message_id}", data.get('ciphertext'))

    # Broadcast to room
    emit('new_message', {
        'sender_mnemonic': room.users[-1].mnemonic,
        'content_encrypted': data.get('ciphertext'),
        'nonce': data.get('nonce'),
        'timestamp': message.timestamp,
        'message_id': message.message_id
    }, room=room_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)