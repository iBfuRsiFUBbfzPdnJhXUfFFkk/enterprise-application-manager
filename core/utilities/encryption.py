from os import getenv

from cryptography.fernet import Fernet, InvalidToken

secret_key: str | None = getenv('ENCRYPTION_SECRET')
if secret_key is None:
    raise ValueError("ENCRYPTION_SECRET environment variable not set.")
cipher_suite: Fernet = Fernet(key=secret_key.encode())


def encrypt_secret(secret: str | None) -> str | None:
    if secret is None:
        return None
    encrypted_secret: bytes = cipher_suite.encrypt(data=secret.encode())
    return encrypted_secret.decode()


def decrypt_secret(encrypted_secret: str | None) -> str | None:
    if encrypted_secret is None:
        return None
    try:
        decrypted_secret: bytes = cipher_suite.decrypt(token=encrypted_secret.encode())
        return decrypted_secret.decode()
    except InvalidToken:
        return None
