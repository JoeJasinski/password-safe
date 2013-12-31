class DecryptionException(Exception):
    pass

class DecryptionImportKeyException(DecryptionException):
    pass

class DecryptionBase64Exception(DecryptionException):
    pass

class EncryptionException(Exception):
    pass

class EncryptionImportKeyException(EncryptionException):
    pass

class EncryptionNoUserKeyException(EncryptionException):
    pass
