import rsa

#Generate Privatekey, random

(private_key , public_key) = rsa.newkeys(2048)
print(private_key)
print(public_key)
