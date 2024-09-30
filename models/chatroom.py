# models/chatroom.py

from typing import List, Dict
from models.user import User
from models.message import Message

class ChatRoom:
    """
    Manages users within a room.
    Handles message broadcasting and room-specific logic.
    """

    def __init__(self, room_id: str):
        self.room_id = room_id
        self.users: List[User] = []
        self.messages: List[Message] = []
        self.encryption_keys = self.generate_encryption_keys()

    def generate_encryption_keys(self) -> Dict[str, str]:
        """
        Generates unique encryption keys for the room.
        
        Returns:
            Dict[str, str]: Encryption keys.
        """
        import os
        return {
            'public_key': base58.b58encode(os.urandom(32)).decode('utf-8'),
            'private_key': base58.b58encode(os.urandom(32)).decode('utf-8')
        }

    def add_user(self, user: User) -> None:
        """
        Adds a user to the chatroom.
        
        Parameters:
            user (User): The user to add.
        """
        self.users.append(user)

    def remove_user(self, user: User) -> None:
        """
        Removes a user from the chatroom.
        
        Parameters:
            user (User): The user to remove.
        """
        self.users.remove(user)

    def broadcast_message(self, message: Message) -> None:
        """
        Broadcasts a message to all users in the room.
        
        Parameters:
            message (Message): The message to broadcast.
        """
        self.messages.append(message)
        for user in self.users:
            # Implement message sending logic, e.g., via WebSockets
            pass
