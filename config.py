
# use os.urandom(36) to create a key
import os
import binascii
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or binascii.hexlify(os.urandom(24))