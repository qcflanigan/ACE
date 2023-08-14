from cryptography.fernet import Fernet

key = Fernet.generate_key()

msg = b"OI, I am q. I go to alabama"

f = Fernet(key)

token = f.encrypt(msg)

print(token)

msge = f.decrypt(token)