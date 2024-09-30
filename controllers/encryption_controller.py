# controllers/encryption_controller.py

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from typing import Tuple

class EncryptionController:
    """
    Handles encryption and decryption processes.
    Implements ECDH for key exchange and AES-256-GCM for message encryption.
    """

    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP384R1())
        self.public_key = self.private_key.public_key()

    def get_public_key_bytes(self) -> bytes:
        """
        Serializes the public key to bytes.
        
        Returns:
            bytes: Serialized public key.
        """
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def generate_shared_key(self, peer_public_key_bytes: bytes) -> bytes:
        """
        Generates a shared secret using peer's public key.
        
        Parameters:
            peer_public_key_bytes (bytes): Peer’s serialized public key.
        
        Returns:
            bytes: Derived shared key.
        """
        peer_public_key = serialization.load_pem_public_key(peer_public_key_bytes)
        shared_secret = self.private_key.exchange(ec.ECDH(), peer_public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'chat_app_key_exchange',
        ).derive(shared_secret)
        return derived_key

    def encrypt_message(self, shared_key: bytes, plaintext: str) -> Tuple[bytes, bytes]:
        """
        Encrypts a plaintext message using AES-256-GCM.
        
        Parameters:
            shared_key (bytes): The symmetric key.
            plaintext (str): The message to encrypt.
        
        Returns:
            Tuple[bytes, bytes]: The nonce and ciphertext.
        """
        import os
        nonce = os.urandom(12)
        encryptor = Cipher(
            algorithms.AES(shared_key),
            modes.GCM(nonce)
        ).encryptor()
        ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
        return nonce, ciphertext + encryptor.tag

    def decrypt_message(self, shared_key: bytes, nonce: bytes, ciphertext_with_tag: bytes) -> str:
        """
        Decrypts a ciphertext message using AES-256-GCM.
        
        Parameters:
            shared_key (bytes): The symmetric key.
            nonce (bytes): The nonce used during encryption.
            ciphertext_with_tag (bytes): The ciphertext concatenated with the tag.
        
        Returns:
            str: The decrypted plaintext.
        """
        tag = ciphertext_with_tag[-16:]
        ciphertext = ciphertext_with_tag[:-16]
        decryptor = Cipher(
            algorithms.AES(shared_key),
            modes.GCM(nonce, tag)
        ).decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode('utf-8')