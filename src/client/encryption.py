"""
File: encryption.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


Encrypts and decrypts binary data.

"""
from cryptography.fernet import Fernet

key = b"REaIOWIUaGqGv7kvCgq24ilu0BNQhGiGF2Ahq-f1Hv8="
f = Fernet(key)


def encrypt(message):
    # Encrypt bytecode
    return f.encrypt(message)


def decrypt(cipher):
    # Decrypt bytecode
    return f.decrypt(cipher)
