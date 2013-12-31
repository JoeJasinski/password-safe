from django import forms
from safe import crypto
from safe.exceptions import *

class KeyField(forms.Field):
    def to_python(self, value):
        return value

    def validate(self, value):
        super(KeyField, self).validate(value)
        # try to import it as an RSA key
        try:
           crypto.get_key(value)
        except EncryptionImportKeyException, e:
            raise forms.ValidationError("Failed to import key: %s" % (e.message))
        return value
    
    #def clean(self, value):
    #    try:
    #        value = super(KeyField, self).clean(value)
    #    except EncryptionImportKeyException, e:
    #        raise forms.ValidationError("Failed to import key: %s" % (e.message))
    #    return value
    
class AddPublicKeyForm(forms.Form):
    pubkey = KeyField()
