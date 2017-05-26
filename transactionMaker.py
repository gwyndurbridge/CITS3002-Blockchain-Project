import keyUtils
import time
import json
import collections

def generateTransaction(sender,reciever,value,payment,change):
	senderPrivate = getPrivateKey(sender)
	transaction = {'sender':sender, 'receiver':reciever, 'value':value, 'payment': payment, 'change':change,'time':time.ctime()}
	transactionDump = json.dumps(transaction)
	print(transactionDump)
	signature = getSign(transactionDump,senderPrivate);
	fullTransaction = {'transaction':transaction,'signature':signature}
	return json.dumps(fullTransaction)

def getPubilicKey(name):
	return keyUtils.readPEM(name,True)

def getPrivateKey(name):
	return keyUtils.readPEM(name,False)

def getSign(message,key):
	return keyUtils.generateSign(message,key)

def checkSign(transactionString):
	transaction = json.loads(transactionString)
	signature = transaction['signature']
	return keyUtils.verifyMessage(json.dumps(transaction['transaction']),signature,getPubilicKey(transaction['transaction']['sender']))
