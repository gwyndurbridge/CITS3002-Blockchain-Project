import rsa
import hashlib

def generateKeys():
	return rsa.newkeys(2048)

#Should use senders private key for signature creation
def generateSign(message,key):
	byteMessage = message.encode('utf8')
	#print(rsa.sign(byteMessage, key, 'SHA-256'))
	return int.from_bytes(rsa.sign(byteMessage, key, 'SHA-256'),byteorder='little')
#Should use senders public key to verify signature
def verifyMessage(message,intSignature,key):
	try:
		byteMessage = message.encode('utf8')
		signature = intSignature.to_bytes(256,byteorder='little')
		#print(signature)
		rsa.verify(byteMessage,signature,key)
		return True
	except Exception as e:
		print('VERFICATION FAILED - Incorrect message')
		return False
#Should use recievers public key to encrypt - DEPRACATED for SSL
def encryptMessage(message,key):
	byteMessage = message.encode('utf8')
	return rsa.encrypt(byteMessage,key)
#Should use recievers private to dencrypt- DEPRACATED for SSL
def decryptMessage(byteMessage,key):
	try:
		message = rsa.decrypt(byteMessage,key).decode('utf8')
		return message
	except Exception as e:
		print('DECRYPTION FAILED')
		return ''
#Allows for keys to be shared as a pem file
def generatePEM(key,name,isPublic):
	toWrite = key.save_pkcs1()
	if isPublic:
		fileName = 'certs/'+name+'Public'+'.pem'
	else:
		fileName = 'certs/'+name+'Private'+'.pem'
	with open(fileName,'wb') as f:
		f.write(toWrite)

def readPEM(name,isPublic):
	if isPublic:
		fileName = 'certs/'+name+'Public'+'.pem'
	else:
		fileName = 'certs/'+name+'Private'+'.pem'
	with open(fileName,'rb') as f:
		keyData = f.read()
	if isPublic:
		return rsa.PublicKey.load_pkcs1(keyData)
	else:
		return rsa.PrivateKey.load_pkcs1(keyData)

def generateFullPEM(name):
	(public_key,private_key) = generateKeys()
	generatePEM(public_key,name,True)
	generatePEM(private_key,name,False)
