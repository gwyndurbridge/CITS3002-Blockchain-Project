import keyUtils
import pytest

message = "TESTING"
name = "jane"
(public_key,private_key) = keyUtils.generateKeys()

def test_signature():
    signature = keyUtils.generateSign(message,private_key)
    assert keyUtils.verifyMessage(message,signature,public_key) == True
    assert keyUtils.verifyMessage('NOT TESTING',signature,public_key) == False
