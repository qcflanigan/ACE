import cryptography #importing general crypto library
from cryptography.fernet import Fernet  #allows us to generate random symmetric keys

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

#self-created hmac library to import hmac functionality
from my_hmac import hmac_new
import hashlib

import os
import base64
from hashlib import sha512
import random

#asymmetric libraries
from cryptography.hazmat.primitives.asymmetric import rsa, dsa      #can use to provide digital signatures/user authentication 
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

#libraries used for asymmetric signature
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def getMessage():           #function to read in message to encrypt from text file
    file1 = open("message.txt", 'rb')
    message = file1.read()
    file1.close()
    return message


#salt helps create unique output for same input
#outside scope of a function so multiple functions can access the salt
    #os.urandom is thought to already be cryptographically secure
salt = os.urandom(16)       #generate a 16 byte salt using os to differ output

    # uses hmac and the random salt
    #600000 iterations is the minimum amount recommended (time/security tradeoff)
    #used this method rather than hmac.new() so i can include the salt
#outside scope of a function so multiple functions can access the MAC
    #used for verify() function

MAC = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000, backend=default_backend())


def createUniqueKey(message):
    #uses 64 bit encoding and the MAC+salt to form
        #unique keys despite same input
    #works, as it generates different keys based on same input and includes padding
    uniqueKey = base64.urlsafe_b64encode(MAC.derive(message))
    #saveKey(uniqueKey)----------------------
    return uniqueKey


def saveKey(uniqueKey):     #save unique key to a file, check if saved properly
    file2 = open("key.txt", 'wb')
    file2.write(uniqueKey)         #write key to file, save and retrieve when needed for encryption
    file2.close()
    emptyVal = os.path.getsize("key.txt")
    if emptyVal != 0:
        print("Key saved successfully\n")
    else:
        print("Save of key was unsuccessfull")


#key pair used for asymmetric signatures
keyPair = RSA.generate(bits=1024)

#function to create signature for sender authentication
#sends using the private key, sha512 hashing
def createSignature():
    message = getMessage()
    messageHash = int.from_bytes(sha512(message).digest(), byteorder="big")
    signature = pow(messageHash, keyPair.d, keyPair.n)
    return signature


def encryptMessage(message):        #main encryption after designing unique key
    #reading unique key from key.txt
    file3 = open("key.txt", 'rb')
    key = file3.read()
    file3.close()

    #putting unique key into another layer on encryption using fernet
    #fernet uses amount of seconds since Jan 1 1970 to creation of key to generate unique key
    fernetKey = Fernet(key)


    #using double layered key to encrypt message in message.txt
    encryptMessage = fernetKey.encrypt(message)


    #writing encrypted message to its own file
    #can be sent on its own now as it is encrypted


    with open('encrypted.txt', 'wb') as f:
        f.write(encryptMessage)     #write encrypted message to a file 



    emptyVal = os.path.getsize("encrypted.txt")
    if emptyVal != 0:                               #check if enrypted message was written to file correctly
        print("Encrypted message saved successfully\n")
    else:
        print("Save of message was unsuccessfull")
    f.close()

    #end of symmetric encryption
#------------------------------------------------------------------------------------------------------
#beginning of asymmetric encryption of symmetric key

def genAsymKeys():
    #initialize rsa key pair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    #initialize public key
    public_key = private_key.public_key()   
    return private_key, public_key     
   

def serializeAsymKeys(private_key, public_key):
    #serialize keys first to then store them in a file for later use
    private_key = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    #storing public key in variable, encoding w serialization
    public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    #write/save private key
    with open('private_key.pem', 'wb') as f:        
        f.write(private_key)
    #write/save public key
    with open('public_key.pem', 'wb') as f:         
        f.write(public_key)


def loadAsymKeys():
    #read in private key
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())     
    #read in public key
    #must use serialization because we need the public_key() instance to decrypt and encrypt
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())     
    return private_key, public_key


def loadSymmetricKey():
    #symmetric key we want to asymmetrically encrypt, will read in from file
    symEnCrypyKeyFile = open("key.txt", 'rb')
    symEncryptKey = symEnCrypyKeyFile.read()
    symEnCrypyKeyFile.close()
    return symEncryptKey


#function to encrypt symmetric key using public key of RSA asymmetric encryption
def encryptKey(symEncryptKey, public_key):
    #using padding and sha256 system to encrypt message with public key
    #global encryptedKey
    encryptedKey = public_key.encrypt(symEncryptKey, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    #write encrypted key to its own file for saving/to load later
    with open("encryptedKey.txt", 'wb') as encryptedKeyFile:
        encryptedKeyFile.write(encryptedKey)
    encryptedKeyFile.close()
    return encryptedKey

#end of encryption code
#-------------------------------------------------------------------------------------------------------------------------------
#beginning of decryption functions

def getKey():           #function to open file and retrieve unique key
    keyFile = open('key.txt', 'rb')
    key = keyFile.read()
    keyFile.close()
    return key

#we want asymmetric decryption of symmetric key first so symmetric decryption has plain symmetric key(reverse order)
def decryptKey(encryptedKey):
    #read in private key
    #need to do again in this function since encrypt/decrypt have diff guiding functions - need to give decrypt() access to private key and encrypted key
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())    
    #using padding and sha256 hash to decrypt message with user's private key
    original_key = private_key.decrypt(encryptedKey, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return original_key

def getEncryptedMessage():      #function to open file and retrieve encrypted message
    with open('encrypted.txt', 'rb') as f:
        encryptedMessage = f.read()   
    f.close()
    return encryptedMessage

#main function to decrypt key using fernet algorithm 
def decryptMessage(key, encryptedMessage):             

    #using fernet library to decrypt the encrypted message with plain symmetric key
    fernet = Fernet(key)
    decryptedMessage = fernet.decrypt(encryptedMessage) #use fernet package to decrypt message with private unique key    

    #write/save decrypted message to a file
    with open('decrypted.txt', 'wb') as file:
            file.write(decryptedMessage)

    file.close()

    #make sure file isn't empty/saved info properly
    emptyVal = os.path.getsize("decrypted.txt")     

    if emptyVal != 0:                               #check if enrypted message was written to file correctly
        print("Decrypted message saved successfully\n")
    else:
        print("Save of message was unsuccessfull")


    print(decryptedMessage)
    print()
    return decryptedMessage

#function to verify the signature sent before encryption
#helps verify authentication of sender using the public key and sha51 hashing
def verifySignature():
    signature = createSignature()       #calls signature function to get the original signature from private key/sender
    message = getMessage()
    messageHash = int.from_bytes(sha512(message).digest(), byteorder="big")
    hashFromSignature = pow(signature, keyPair.e, keyPair.n)
    if messageHash == hashFromSignature:        #if hash from message == riginal private key hash, we can authenticate the user
        print("Signature is Valid!\n")
    else:
        print("Invalid Signature\n")

#The reciever would use this func to find hmac to compare the hmac sent to them
def solve_hmac(k, m):
    k = k.decode() #need both key and msg saved as strings to work
    m = m.decode()
    hmac = hmac_new(k, m, hashlib.sha256).encode() #find hmac
    return hmac #returns hexidecimal value in bytes

def save_hmac(hmac): #In regular application, this would be sent to user
    with open('hmac.txt', 'wb') as f:
            f.write(hmac) 
    f.close()

def verify_hmac(hmac):
    hmacFile = open("hmac.txt", 'rb')
    hmacBytes = bytes(hmacFile.read())        #open and read key file to use in verification
    hmacFile.close() 
    #Return true if solved Hmac matches the sent (saved in our case) one
    return True if hmacBytes == bytes(hmac) else False


def executeEncryptFunctions():
    message = getMessage()              #run functions for encryption 
    uniqueKey = createUniqueKey(message) #private key made and saved in key.txt
    saveKey(uniqueKey)
    hmac = solve_hmac(uniqueKey, message) #create HMAC with key & msg
    save_hmac(hmac) #send (or in our case save) it for reciever
    private_key, public_key = genAsymKeys()
    signature = createSignature()
    encryptMessage(message)

    #Asymmetric execution of encryption
    serializeAsymKeys(private_key, public_key)
    private_key, public_key = loadAsymKeys()
    symEncryptKey = loadSymmetricKey() 
    encryptedKey = encryptKey(symEncryptKey, public_key)

def executeDecryptFunctions():      #run functions for decryption, verify() gets run from decrypt() function
    private_key, public_key = loadAsymKeys()
    symEncryptKey = loadSymmetricKey()
    encryptedKey = encryptKey(symEncryptKey, public_key)
    key = decryptKey(encryptedKey)
    encryptedMessage = getEncryptedMessage()
    decryptedMessage = decryptMessage(key, encryptedMessage)
    verifySignature()
    hmac = solve_hmac(key, decryptedMessage) #find hmac to compare the one sent to verify authenticity
    if verify_hmac(hmac):
        print("Message authenticated via HMAC!!\n")    
    else:
        print("Message NOT authentic from original!\n")


#main function, ask user to encrypt or decrypt code -> sends to corresponding functions
def main():
    choice = input("Would you like to encrypt or decrypt the message.txt file?: ")
    print()
    if choice == "encrypt":         #user chooses to encrypt or decrypt the files, program directs the functions based on user choice
        executeEncryptFunctions()

    elif choice == "decrypt":
        executeDecryptFunctions()

    else:
        print("Invalid input. Please try again")


if __name__ == "__main__":
    main()