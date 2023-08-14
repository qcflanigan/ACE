import cryptography #importing general crypto library
from cryptography.fernet import Fernet  #allows us to generate random symmetric keys

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import os
import base64

from symEncrypt import *

def getKey():           #function to open file and retrieve unique key
    keyFile = open('key.txt', 'rb')
    key = keyFile.read()
    keyFile.close()
    print(key)
    return key


def getEncryptedMessage():      #function to open file and retrieve encrypted message
    with open('encrypted.txt', 'rb') as f:
        encryptedMessage = f.read()   
    f.close()
    return encryptedMessage

def decryptMessage(key, encryptedMessage):            #main function to decrypt key using fernet algorithm  

    fernet = Fernet(key)

    decryptedMessage = fernet.decrypt(encryptedMessage) #use fernet package to decrypt message with private unique key     

    with open('decrypted.txt', 'wb') as file:
        file.write(decryptedMessage)

    file.close()
    emptyVal = os.path.getsize("decrypted.txt")
    if emptyVal != 0:                               #check if enrypted message was written to file correctly
        print("decrypted message saved successfully")
    else:
        print("Save of message was unsuccessfull")


    print(decryptedMessage)
    return decryptedMessage

def verifyMessage(decryptedMessage, key):  #use hmac verification to verify integrity of the message
    print()

def main():         #call main functions to decrypt message
    key = getKey()
    encryptedMessage = getEncryptedMessage()
    decryptedMessage = decryptMessage(key, encryptedMessage)
    verifyMessage(decryptedMessage, key)


if __name__ == "__main__":
    main()
