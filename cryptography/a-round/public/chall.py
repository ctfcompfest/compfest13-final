from around import ARound
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib 
import os

key = os.urandom(AES.block_size)
cipher = ARound(key)

p = []
c = []

for _ in range(2):
    plaintext = os.urandom(16)
    p.append(plaintext.hex())
    ciphertext = cipher.encrypt_block(plaintext)
    c.append(ciphertext.hex())

flag = open("flag.txt", "rb").read()   
sha1 = hashlib.sha1()
sha1.update(str(key).encode())
new_key = sha1.digest()[:16]
iv = os.urandom(AES.block_size)
cipher = AES.new(new_key, AES.MODE_CBC, IV=iv)
encrypted_flag = cipher.encrypt(pad(flag, 16))

print('plaintexts =', p)
print('ciphertexts =', c)
print('iv =\'' + iv.hex() + '\'')
print('encrypted_flag = \'' + encrypted_flag.hex() + '\'')