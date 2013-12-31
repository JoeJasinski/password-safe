from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64decode
from safe.exceptions import *

def get_key(text):
    try:
        key = RSA.importKey(text)
    except ValueError, e:
        raise EncryptionImportKeyException(e.message)
    key_cipher = PKCS1_OAEP.new(key)
    return key_cipher 


def encrypt(public_key, clear_text):
    """
    param: public_key PublicKey to encrypt with
    param: clear_text String to encrypt
    return encrypted string
    """
    ciphertext = public_key.encrypt(clear_text.encode("utf-8"))
    return ciphertext.encode('base64')


def decrypt(self, private_key_string, ciphertext):
    '''
    param: private_key_string string of your private key
    param: ciphertext String to be decrypted
    return decrypted string
    '''
    try:
        private_key = RSA.importKey(private_key_string) 
    except ValueError, e:
        raise DecryptionImportKeyException(e.message)
    private_key = PKCS1_OAEP.new(private_key) 
    try:
        decrypted = private_key.decrypt(b64decode(ciphertext)) 
    except TypeError, e:
        raise DecryptionBase64Exception(e.message)
    return decrypted