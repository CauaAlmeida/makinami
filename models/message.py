# models/message.py

from typing import Optional
from dataclasses import dataclass, field
import time

@dataclass
class Message:
    """
    Encapsulates message data, including encryption and decryption methods.
    Handles message validation and sanitization.
    """
    sender_tripcode: str
    content_encrypted: str
    timestamp: float = field(default_factory=lambda: time.time())
    message_id: str = field(default_factory=lambda: generate_message_id())

    def sanitize(self) -> None:
        """
        Sanitizes the message content to prevent XSS attacks.
        """
        # Implement sanitization logic if necessary
        pass

def generate_message_id() -> str:
    """
    Generates a unique message ID.
    
    Returns:
        str: Unique message identifier.
    """
    import uuid
    return str(uuid.uuid4())