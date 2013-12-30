from django.contrib import admin
from safe.models import PublicKey 

class PublicKeyAdmin(admin.ModelAdmin):
    pass

admin.site.register(PublicKey, PublicKeyAdmin)