# services/redis_service.py

import redis
from typing import Any, Optional

class RedisService:
    """
    Manages interactions with the Redis database.
    """

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> None:
        """
        Sets a key-value pair in Redis.
        
        Parameters:
            key (str): The key.
            value (Any): The value.
            ex (Optional[int]): Expiration time in seconds.
        """
        self.client.set(key, value, ex=ex)

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value by key from Redis.
        
        Parameters:
            key (str): The key.
        
        Returns:
            Optional[Any]: The value if exists, else None.
        """
        return self.client.get(key)

    def hset(self, name: str, key: str, value: Any) -> None:
        """
        Sets a field in a hash stored at key.
        
        Parameters:
            name (str): The name of the hash.
            key (str): The field name.
            value (Any): The value to set.
        """
        self.client.hset(name, key, value)

    def exists(self, key: str) -> bool:
        """
        Checks if a key exists in Redis.
        
        Parameters:
            key (str): The key to check.
        
        Returns:
            bool: True if exists, False otherwise.
        """
        return self.client.exists(key)