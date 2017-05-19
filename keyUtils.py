import rsa

#Generate Privatekey, random
def generateKeys():
    return rsa.newkeys(2048)

def generateSign(message,key):
    return rsa.sign(message, key, 'SHA-256')

def verifyMessage(message,signature,key):
    try:
        rsa.verfiy(message,signature,key)
        return True
    except Exception as e:
        print('VERFICATION FAILED')
        return False

print(private_key)
print(public_key)
