from django import forms
from safe import crypto
from safe.exceptions import *
from safe.models import Credential

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


class AddPublicKeyForm(forms.Form):
    pubkey = KeyField()


class AddCredentialForm(forms.ModelForm):
    secret = forms.CharField()
    class Meta:
        model = Credential
        widgets = {
          'tags': forms.Textarea(attrs={'rows':1, 'cols':30}),
        }
    def __init__(self, *args, **kw):
        super(AddCredentialForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'title',
            'login_name',
            'secret',
            'slug',
            'url',
            'tags',
            'notes',]