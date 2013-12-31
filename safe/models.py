from django.db import models
from django.core import exceptions 
from safe import crypto
from safe.exceptions import *

class MetaInfoMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublicKey(MetaInfoMixin, models.Model):
    user = models.OneToOneField('auth.User')
    text = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s" % (self.user)

    def get_public_key(self):
        """
        return public key cipher object based on self.text
        """
        return crypto.get_key(self.text)
    
    def encrypt(self, clear_text):
        """
        param: clear_text String to encrypt
        """
        return crypto.encrypt(self.get_public_key(), clear_text)
    
    
class CredentialManager(models.Manager):
    
    def create_credential(self, name, slug, plain_secret, user, **kwargs):
        """
        param: name String - name of the credential to create
        param: slug Stirng - slug that is unique to Credential
        param: plain_secret String - password/secret to save
        param: user User - Django User to save the secret under
        param: *kwargs dict - dict containing the values of other Credential 
           fields
        returns: a Credential object with an foreign key UserSecret attached.
        """
        credential = Credential.objects.create(name=name, slug=slug, **kwargs)
        credential.get_or_create_usersecret(user, plain_secret)
        return credential


class Credential(MetaInfoMixin, models.Model):
    name = models.CharField(max_length=255,)
    slug = models.SlugField(max_length=255, unique=True)
    url = models.URLField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    login_name = models.CharField(u'Login/ID/Username', max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    objects = CredentialManager()

    def __unicode__(self):
        return "%s" % (self.name)
    
    def get_or_create_usersecret(self, user, plain_secret):
        """
        param: user User - Django User to create a UserSecret for
        param: plain_secret String - plain text of password/secret value
        returns a UserSecret object and a boolean of whether or not a new
          object was created. 
        """
        secret, created = UserSecret.objects.get_or_create(credential=self, user=user, )
        secret.encrypt(plain_secret)
        secret.save()
        return secret, created
    

class UserSecret(MetaInfoMixin, models.Model):
    credential = models.ForeignKey('safe.Credential', related_name="credentials")
    user = models.ForeignKey('auth.User')
    encrypted_secret = models.TextField(u"Password/Key/Secret", blank=True, null=True)
    
    def __unicode__(self):
        return "%s %s" % (self.credential, self.user)
    
    def encrypt(self, plain_secret):
        try:
            self.encrypted_secret = self.user.publickey.encrypt(plain_secret)
        except exceptions.ObjectDoesNotExist, e:
            raise EncryptionNoUserKeyException(e.message)
    