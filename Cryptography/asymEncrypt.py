from cryptography.hazmat.primitives.asymmetric import rsa       #can use to provide digital signatures/user authentication 
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random


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

    print(symEncryptKey)
    print()

    return symEncryptKey


#functio to encrypt symmetric key using public key of RSA asymmetric encryption
def encryptKey(symEncryptKey, public_key):
    #using padding and sha256 system to encrypt message with public key
    encryptedKey = public_key.encrypt(symEncryptKey, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

    #write encrypted key to its own file for saving/to load later
    with open("encryptedKey.txt", 'wb') as encryptedKeyFile:
        encryptedKeyFile.write(encryptedKey)

    print()
    print(encryptedKey)
    return encryptedKey

#symmetric key has been asymmetrically encrypted
#-----------------------------------------------------------------------------------------------------------------
#beginning decryption to get plain key back for symmetric decryption


def decryptKey(private_key, encryptedKey):
    #using padding and sha256 hash to decrypt message with user's private key
    original_key = private_key.decrypt(encryptedKey, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    
    print()
    print(original_key)



def main():
    private_key, public_key = genAsymKeys()
    serializeAsymKeys(private_key, public_key)
    private_key, public_key = loadAsymKeys()
    symEncryptKey = loadSymmetricKey()
    encryptedKey = encryptKey(symEncryptKey, public_key)

    decryptKey(private_key, encryptedKey)
    

if __name__ == "__main__":
    main()
