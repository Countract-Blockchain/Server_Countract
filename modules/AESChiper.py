import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

import io

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        print(iv)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        print(iv)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # print(AES.block_size)
        # print(len(enc[AES.block_size:]))
        raw = cipher.decrypt(enc[AES.block_size:])
        print("=============")
        print(len(raw))
        return self._unpad(raw[:16]).decode('utf-8')
        #return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        #print("25")
        #print(type(s))
        # print(type((self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode('utf-8')))
        # print(type(s))
        print((self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode('utf-8'))
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode('utf-8')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
        return s