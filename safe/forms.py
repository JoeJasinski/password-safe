import hashlib
from django import forms
from safe import crypto
from safe.exceptions import *
from safe.models import Credential


class KeyField(forms.Field):

    def __init__(self, *args, **kw):
        kwargs = {'widget': forms.Textarea(attrs={'style': "width:100%;"})}
        kwargs.update(kw)
        super(KeyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return value

    def validate(self, value):
        super(KeyField, self).validate(value)
        # try to import it as an RSA key
        try:
            crypto.get_key(value)
        except EncryptionImportKeyException as e:
            raise forms.ValidationError("Failed to import key: %s" % (e.message))
        return value


_hashit = lambda s: hashlib.sha1(s).hexdigest()


class CreatePublicKeyForm(forms.Form):
    pubkey = KeyField()

    def __init__(self, *args, **kw):
        show_privkey = kw.pop('show_privkey', None)
        super(CreatePublicKeyForm, self).__init__(*args, **kw)
        self.fields['pubkey'].widget.attrs['rows'] = "6"
        self.fields['pubkey'].widget.attrs['id'] = "pubkey"
        if show_privkey:
            self.fields['privkey'] = KeyField(required=False)
            self.fields['privkey'].widget.attrs['rows'] = "15"
            self.fields['privkey'].widget.attrs['id'] = "privkey"
            self.fields.keyOrder = ['privkey', 'pubkey']
        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    @classmethod
    def calculate_hash(cls, value):
        return _hashit(value)

    def clean(self):
        cleaned_data = super(CreatePublicKeyForm, self).clean()
        cleaned_data['hash'] = CreatePublicKeyForm.calculate_hash(
            cleaned_data['pubkey'])
        return cleaned_data


class CreateUpdateCredentialForm(forms.ModelForm):

    class Meta:
        model = Credential
        widgets = {
            'tags': forms.Textarea(attrs={'rows': 1, 'cols': 30}),
        }
        fields = '__all__'

    def __init__(self, edit=False, *args, **kw):
        super(CreateUpdateCredentialForm, self).__init__(*args, **kw)
        if not edit:
            self.fields['secret'] = forms.CharField()
        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})
        self.fields.keyOrder = ['title', 'login_name'] + \
            [x for x in ['secret'] if not edit] +  \
            ['url', 'tags', 'notes']


class SearchTagField(forms.Form):

    q = forms.CharField(required=False)
