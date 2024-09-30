# controllers/moderation_controller.py

from services.redis_service import RedisService
from models.user import User
from models.message import Message

class ModerationController:
    """
    Provides methods for deleting messages, muting, banning, and room management.
    """

    def __init__(self, redis_service: RedisService):
        self.redis = redis_service

    def delete_message(self, room_id: str, message_id: str, moderator: User) -> bool:
        """
        Marks a message as deleted.
        
        Parameters:
            room_id (str): The ID of the room.
            message_id (str): The ID of the message.
            moderator (User): The moderator performing the action.
        
        Returns:
            bool: Success status.
        """
        key = f"{room_id}:messages:{message_id}"
        if self.redis.exists(key):
            self.redis.hset(key, "deleted", True)
            return True
        return False

    def mute_user(self, room_id: str, user_tripcode: str, duration: int) -> bool:
        """
        Mutes a user for a specified duration.
        
        Parameters:
            room_id (str): The ID of the room.
            user_tripcode (str): The tripcode of the user.
            duration (int): Mute duration in seconds.
        
        Returns:
            bool: Success status.
        """
        key = f"{room_id}:muted:{user_tripcode}"
        self.redis.set(key, "muted", ex=duration)
        return True

    def ban_user(self, room_id: str, user_tripcode: str) -> bool:
        """
        Bans a user from a room.
        
        Parameters:
            room_id (str): The ID of the room.
            user_tripcode (str): The tripcode of the user.
        
        Returns:
            bool: Success status.
        """
        key = f"{room_id}:banned:{user_tripcode}"
        self.redis.set(key, "banned")
        return True

    def ban_user_globally(self, user_tripcode: str) -> bool:
        """
        Bans a user globally across all rooms.
        
        Parameters:
            user_tripcode (str): The tripcode of the user.
        
        Returns:
            bool: Success status.
        """
        key = f"global_banned:{user_tripcode}"
        self.redis.set(key, "banned")
        return True