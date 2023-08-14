import socket, pyDH, base64, sys, os, hashlib, binascii, time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
dhAlice = pyDH.DiffieHellman()
alicePK = dhAlice.gen_public_key()
bobPK = 0
shared = 0

msgFile = open("message.txt", 'rb')
msg = msgFile.read()
msgFile.close()

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
	#print(hmac_new(secret_key, message, hashlib.sha256))

	#https://medium.com/@ashiqgiga07/cryptography-with-python-hashing-d0b7dbf7767
	#https://vegibit.com/how-to-use-hmac-in-python/https://datatracker.ietf.org/doc/html/rfc2104
	
def asymKE():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Establish a socket connections
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		
		# Receive Bob's public key & send Alice's
		bobPK = int(conn.recv(1024))
		conn.sendall(str(alicePK).encode('utf8'))
		s.close()
		
		# Calulate the shared (symmetric) key
		shared = bytes(dhAlice.gen_shared_key(bobPK)[:-21]+"=",'utf8')

		sharedKeyFile = open("sharedKey.txt", 'wb')
		sharedKeyFile.write(shared)
		sharedKeyFile.close()

		#print("shared key: ", shared)
		print()

		return Fernet(shared)
		
def sendMsg(f, toSend):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		temp = f.encrypt(toSend)

		encryptedMessageFile = open("encrypted.txt", 'wb')
		encryptedMessageFile.write(temp)
		encryptedMessageFile.close()

		conn.sendall(temp)
		s.close()
		
def signMsg(toSend):
	PORT = 63001
	private_key = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048,
	)
	
	#Generate the signature
	signature = private_key.sign(
		toSend,
		padding.PSS(
		    mgf=padding.MGF1(hashes.SHA256()),
		    salt_length=padding.PSS.MAX_LENGTH
		),
		hashes.SHA256()
	)

	# Retrieve the public key in the PEM form as bytes
	PKtoSend = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

	# Socket set up
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		
		# These print statements were added for debugging purposes yet when they're not here the code chooses not to run. I don't know why
		# and I've already lost hours of my life trying to figure it out so they're just gonna stay
		#print(signature)
		#print(len(signature))
		
		# Send the signature stuff
		conn.sendall(bytes(str(len(signature)),'utf8')) # Size of the signature (used for the .recv buffer size)
		conn.sendall(signature) # The signature
		#conn.sendall(msg) # The original message		
		s.close()
		# For some reason, the PEM bytes would only occasionally send, so I made them into a file instead
		f = open("foo.pem", "w")
		f.write(PKtoSend.decode("utf8"))
		f.close()
		
print("Beginning key exchange")
f = asymKE()
print(f"Sending:\n\"{msg.decode('utf8')}\"")
sendMsg(f, msg)
print("Sending signature")
signMsg(msg)
print("Sending HMAC")
HMAC = hmac_new(str(shared), msg.decode('utf8'), hashlib.sha256)
#print("HMAC: ", HMAC)
print()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Establish a socket connections
		s.bind((HOST, 63002))
		s.listen()
		conn, addr = s.accept()
		conn.sendall(bytes(HMAC,'utf8'))
		s.close()
print("====END====")
		
	
		
