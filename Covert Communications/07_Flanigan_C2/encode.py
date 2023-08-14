
from PIL import Image
import sys

def genData(data):
		newdata = []
		for i in data:
			newdata.append(format(ord(i), '08b'))
		return newdata


def modPixel(pixel, data):

	datalist = genData(data)
	lendata = len(datalist)
	imgdata = iter(pixel)

	for i in range(lendata):
		pix = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1
			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1
		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]


def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)
	for pixel in modPixel(newimg.getdata(), data):
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1


def encrypt(data, description):
	print(f"{len(description)} and {len(data)}")
	while len(description) > len(data):
		data += data
	data = data[:len(description)]
	description = description.encode()
	msg = data.encode()
	encrypted_msg = bytearray(msg[i] ^ description[i % len(description)] for i in range(len(msg)))
	print("Encrypted:", encrypted_msg)
	return encrypted_msg.decode() #Back to strings now

#Takes in the photo's description and its encrypted string 
def decrypt(encrypted_data, description):
	while len(description) > len(encrypted_data):
		encrypted_data += encrypted_data
	encrypted_data = encrypted_data[:len(description)]
	description = description.encode() #Encode to bytes for the XOR
	msg = encrypted_data.encode()
	# XOR every byte of encrypted_msg with key to decrypt
	decrypted_msg = bytearray(msg[i] ^ description[i % len(description)] for i in range(len(msg)))

	return decrypted_msg.decode()

# Encode data into image
def stegEncode():
	img = input("Image filename: ")
	image = Image.open(img, 'r')

	data = input("Enter data to be encoded : ")
	if (len(data) == 0):
		raise ValueError('You need data to encode it')

	key = input("Enter in your post's title: ")

	newimg = image.copy()
	data = encrypt(key, data)
	encode_enc(newimg, data)

	new_img_name = input("Output filename (don't add the extension): ")
	new_img_name += '.png'
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def stegDecode():
	img = input("Image filename: ")
	image = Image.open(img, 'r')
	key = input("Enter in your post's title: ")
	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return decrypt(key, data)

# Driver Code
if __name__ == '__main__' :
	if len(sys.argv) > 1:
		if sys.argv[1] == "-e":
			stegEncode()
		elif sys.argv[1] == "-d":
			print("Decoded word : " + stegDecode())

	print("Usage:")
	print(" -e\tEncode text into an image")
	print(" -d\tDecode an image to get the text")