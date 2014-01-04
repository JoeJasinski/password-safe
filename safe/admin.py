from django.contrib import admin
from safe.models import PublicKey, Credential, UserSecret

class PublicKeyAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    readonly_fields = ['created', 'modified']
    list_display = ['user',  'created', 'modified']

class UserSecretInline(admin.StackedInline):
    model = UserSecret
    extra = 0
    raw_id_fields = ['user']
    readonly_fields = ['encrypted_secret', 'created', 'modified']

class CredentialAdmin(admin.ModelAdmin):
    inlines = [UserSecretInline,]
    list_display = ['title', 'slug', 'tags', 'login_name',  'created', 'modified']
    readonly_fields = ['created', 'modified']


admin.site.register(PublicKey, PublicKeyAdmin)
admin.site.register(Credential, CredentialAdmin)