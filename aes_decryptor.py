# Reference https://stackoverflow.com/questions/11567290/cryptojs-and-pycrypto-working-together
from Crypto.Cipher import AES
from Crypto import Random
import base64
import sys

BLOCK_SIZE = 16

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + chr(length)*length

def unpad(data):
    return data[:-data[-1]]

def assure_length_16(key):
    if len(key)>16:
        key = key[0:16]
    if len(key)<16:
        key = key + '0'*(16-len(key))
    return key

def decrypt(encrypted, key):
    key = assure_length_16(key)

    encrypted = base64.b64decode(encrypted)
    IV = encrypted[:BLOCK_SIZE]
    aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, IV)
    return unpad(aes.decrypt(encrypted[BLOCK_SIZE:])).decode('utf-8')

if __name__ == '__main__':
    message_to_decrypt = sys.argv[1]
    key = sys.argv[2]
    print(decrypt(message_to_decrypt, key))
