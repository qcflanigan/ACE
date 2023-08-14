import socket, pyDH, base64, sys, os, hashlib, binascii, time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
dhBob = pyDH.DiffieHellman()
bobPK = dhBob.gen_public_key()
alicePK = 0
shared = 0

def hmac_new(key, msg, hasher):
    block_size = 64  # Block size for SHA-1, SHA-224, or SHA-256
    ipad = 0x36  # Inner pad value = 54
    opad = 0x5c  # Outer pad value = 92

    if len(key) > block_size:
        key = hasher(key.encode("utf-8")).digest()
    #byt = hex(msg[int(len(msg)/2)])
    else:
        i = 0
        #While key is shorter than block_size (64)
        while len(key) < block_size:
            #Add a character from the end of msg, go left to right
            key += (msg[-(i % len(msg)) - 1])
            i += 1
        key.encode("utf-8")

    #XOR the value of the key to the ipad
        #value of key found from getting the hexidecimal of the key and converting to int
    inner = bytearray((int(binascii.hexlify(x.encode()).decode(),16) ^ ipad) for x in key)
    #Add msg to right side of inner
    inner.extend(msg.encode("utf-8"))

    outer = bytearray((int(binascii.hexlify(x.encode()).decode(),16) ^ opad) for x in key)
    #hash inner, get value from has object with digest, add it to right of outer
    outer.extend(hasher(inner).digest())

    #hash outer and return hexidecimal value
    hmac_val = hasher(outer).hexdigest()
    return hmac_val #returns as string

	# Example usage:
	# secret_key = "my_secret_key"
	# message = "Hello, world!"
	# print(hmac_new(secret_key, message, hashlib.sha256))

	#https://medium.com/@ashiqgiga07/cryptography-with-python-hashing-d0b7dbf7767
	#https://vegibit.com/how-to-use-hmac-in-python/https://datatracker.ietf.org/doc/html/rfc2104
	
def asymKE():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Set up socket
		s.connect((HOST, PORT))
		
		# Send Bob's public key, retrieve Alice's, and calculate the shared (symmetric) key
		s.sendall(str(bobPK).encode('utf8'))
		alicePK = int(s.recv(1024))	
		s.close()	
		shared = bytes(dhBob.gen_shared_key(alicePK)[:-21]+"=",'utf8')
		
		return Fernet(shared)
		
def recMsg(f):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))		
		toDec = s.recv(1024)
		s.close()

		decryptedMsg = f.decrypt(toDec)

		decMsgFile = open("decrypted.txt", 'wb')
		decMsgFile.write(decryptedMsg)
		decMsgFile.close()


		return decryptedMsg
		
def verifyMsg(toCheck):
	PORT = 63001
	#Set up the server
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		signatureSize = int((s.recv(3)).decode('utf8')) # Without the size of the signature in bytes, the next .recv would receive too much and cause an error
		#print(signatureSize) # 
		signedDoc = s.recv(signatureSize)
		#origDoc = s.recv(1024)
		s.close()
	time.sleep(1)
	f = open("foo.pem", "r")
	temp2 = f.read()
	#print(temp2)
	#print(signedDoc)
	#print(str(signedDoc[:-len(origDoc)]))
	publicKey = serialization.load_pem_public_key(bytes(temp2,'utf8'))
	#print(isinstance(publicKey, rsa.RSAPublicKey))
	try:
		publicKey.verify(
			signedDoc,		#verifying the signed message with the original message to verify sender authenticity
			msg,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA256()),
				salt_length=padding.PSS.MAX_LENGTH
			),
			hashes.SHA256()
		)
		return True
	except:
		return False
		
print("Beginning key exchange")
f = asymKE()
time.sleep(1)
msg = recMsg(f)
print(f"Received:\n\"{msg.decode('utf8')}\"")
time.sleep(1)
if (verifyMsg(msg)):
	print("Message was definitely sent by Alice")
else:
	print("The message was not sent by Alice")
print("Generating HMAC")
HMAC = hmac_new(str(shared), msg.decode('utf8'), hashlib.sha256)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, 63002))
	receivedHMAC = s.recv(1023) # Without the size of the signature in bytes, the next .recv would receive too much and cause an error
	#print(signatureSize)
	s.close()
if HMAC == receivedHMAC.decode('utf8'):
	print("Message integrity confirmed")
else:
	print("Message integrity violated")
print("====END====")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
