#Encryption
from cryptography.fernet import Fernet

key = b"REaIOWIUaGqGv7kvCgq24ilu0BNQhGiGF2Ahq-f1Hv8="
f = Fernet(key)

#Encrypt bytecode
def encrypt(message):
    return f.encrypt(message)

#Decrypt bytecode
def decrypt(cipher):
    return f.decrypt(cipher)