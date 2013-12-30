from django.db import models
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util import asn1
from base64 import b64decode

class PublicKey(models.Model):
    user = models.ForeignKey('auth.User')
    text = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s" % (self.user)

    def encrypt(self, clear_text):
        '''
        param: clear_text String to encrypt
        '''
        public_key = RSA.importKey(self.text)
        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(clear_text.encode("utf-8"))
        return ciphertext.encode('base64')
    
    
    def decrypt(self, private_key_string, ciphertext):
        '''
        param: private_key_string string of your private key
        param: ciphertext String to be decrypted
        return decrypted string
        '''
        rsakey = RSA.importKey(private_key_string) 
        rsakey = PKCS1_OAEP.new(rsakey) 
        decrypted = rsakey.decrypt(b64decode(ciphertext)) 
        return decrypted