import keyUtils
import time
import json
import collections

def generateTransaction(sender,reciever,value,payment,change):
	senderPrivate = getPrivateKey(sender)
	transaction = {'sender':sender, 'receiver':reciever, 'value':value, 'payment': payment, 'change':change,'time':time.ctime()}
	transactionDump = json.dumps(transaction)
	signature = getSign(transactionDump,senderPrivate);
	fullTransaction = {'transaction':transactionDump,'signature':signature}
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
	transactionInterior = json.loads(transaction['transaction'])
	return keyUtils.verifyMessage(transaction['transaction'],signature,getPubilicKey(transactionInterior['sender']))
