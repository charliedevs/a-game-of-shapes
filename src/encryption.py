"""
File: encryption.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


Encrypts and decrypts binary data.

"""
from cryptography.fernet import Fernet

key = b"REaIOWIUaGqGv7kvCgq24ilu0BNQhGiGF2Ahq-f1Hv8="
f = Fernet(key)

#TODO: fix encryption. Getting cryptography.fernet.InvalidToken error

def encrypt(message):
    # Encrypt bytecode
    # return f.encrypt(message)
    return message


def decrypt(cipher):
    # Decrypt bytecode
    # return f.decrypt(cipher)
    return cipher
