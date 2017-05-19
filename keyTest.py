import keyUtils
import pytest

message = "TESTING"
name = "jane"
(public_key,private_key) = keyUtils.generateKeys()

def test_signature():
    signature = keyUtils.generateSign(message,private_key)
    assert keyUtils.verifyMessage(message,signature,public_key) == True
    assert keyUtils.verifyMessage('NOT TESTING',signature,public_key) == False

def test_encryption():
    encryptedMessage = keyUtils.encryptMessage(message,public_key)
    assert keyUtils.decryptMessage(encryptedMessage,private_key) == message
    encryptedMessage = encryptedMessage[:-1] + b'X'
    assert keyUtils.decryptMessage(encryptedMessage,private_key) == ''

def test_PEMcreation():
	keyUtils.generatePEM(public_key,name,True)
	readKey = keyUtils.readPEM(name,True)
	assert readKey == public_key
	keyUtils.generatePEM(private_key,name,False)
	readKeyPrivate = keyUtils.readPEM(name,False)
	assert readKeyPrivate == private_key
