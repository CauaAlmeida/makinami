# models/user.py

import hashlib
import base58
from utils.helpers import generate_mnemonic

class User:
    """
    Represents a user in the chat application.
    Handles tripcode and mnemonic generation.
    """

    def __init__(self, secret: str):
        self.secret = secret
        self.tripcode = self.generate_tripcode(secret)
        self.mnemonic = generate_mnemonic(self.tripcode)
        self.session = None  # To be managed by SessionManager

    @staticmethod
    def generate_tripcode(secret: str) -> str:
        """
        Generates a tripcode from a user-provided secret.
        
        Parameters:
            secret (str): The user's secret passphrase.
            
        Returns:
            str: A Base58-encoded tripcode derived from the secret.
        """
        sha256_hash = hashlib.sha256(secret.encode('utf-8')).digest()
        tripcode = base58.b58encode(sha256_hash).decode('utf-8')[:44]
        return tripcode