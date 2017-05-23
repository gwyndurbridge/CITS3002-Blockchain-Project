import rsa

def generateKeys():
    return rsa.newkeys(2048)

#Should use senders private key for signature creation
def generateSign(message,key):
    byteMessage = message.encode('utf8')
    return rsa.sign(byteMessage, key, 'SHA-1')

#Should use senders public key to verify signature
def verifyMessage(message,signature,key):
    try:
        byteMessage = message.encode('utf8')
        rsa.verify(byteMessage,signature,key)
        return True
    except Exception as e:
    	print('VERFICATION FAILED - Incorrect message')
    	return False
#Should use recievers public key to encrypt
def encryptMessage(message,key):
    byteMessage = message.encode('utf8')
    return rsa.encrypt(byteMessage,key)
#Should use recievers private to dencrypt
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
        fileName = name+'Public'+'.pem'
    else:
        fileName = name+'Private'+'.pem'
    with open(fileName,'wb') as f:
        f.write(toWrite)

def readPEM(name,isPublic):
    if isPublic:
        fileName = name+'Public'+'.pem'
    else:
        fileName = name+'Private'+'.pem'
    with open(fileName,'rb') as f:
        keyData = f.read()
    if isPublic:
        return rsa.PublicKey.load_pkcs1(keyData)
    else:
        return rsa.PrivateKey.load_pkcs1(keyData)
