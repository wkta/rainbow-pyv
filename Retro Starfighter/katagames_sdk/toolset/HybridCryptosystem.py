#RSA_cryptography.py#Importing necessary modules
from Crypto.Cipher import Salsa20, PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify#The message to be encrypted
import random
from Crypto.Random import get_random_bytes


message = b'Public and Private keys encryption'  # Generating private key (RsaKey object) of key length of 1024 bits


class HybridCryptosystem:
    def __init__(self, key=None):
        if key is None:
            key = RSA.generate(2048)
        self.pr_key = key
    
    def crypt(self, plaintext):
        coolkey = get_random_bytes(32)
        #print(coolkey)
        
        cipher = Salsa20.new(key=coolkey)
        hiddenmsg = cipher.nonce + cipher.encrypt(bytes(plaintext.encode('ascii')))
        hiddenk = HybridCryptosystem.asym_crypt(bytes(coolkey), self.pr_key.public_key())
        return hiddenk, hiddenmsg

    def decrypt(self, info_pair):
        hiddenk, ciphertext_b = info_pair
        used_key_b = HybridCryptosystem.asym_decrypt(hiddenk, self.pr_key)
        #print(used_key_b)
        
        msg_nonce = ciphertext_b[:8]
        ciphertext = ciphertext_b[8:]
        
        cipher = Salsa20.new(key=used_key_b, nonce=msg_nonce)
        plain_txt = cipher.decrypt(ciphertext)
        return plain_txt

    @staticmethod
    def asym_crypt( plaintext, rsa_key):
        print(type(rsa_key))#Instantiating PKCS1_OAEP object with the public key for encryption
        cipher = PKCS1_OAEP.new(key=rsa_key)
        #
        #Encrypting the message with the PKCS1_OAEP object
        #cipher_text = cipher.encrypt(msg_b)
        #
        msg = cipher.encrypt(plaintext)
        return msg

    @staticmethod
    def asym_decrypt( ciphertext_b, rsa_key):
        print(type(rsa_key))  # Instantiating PKCS1_OAEP object with the public key for encryption
        cipher = PKCS1_OAEP.new(key=rsa_key)
        plain_txt = cipher.decrypt(ciphertext_b)
        return plain_txt
