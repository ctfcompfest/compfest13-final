from pwn import *
from Crypto.Util.number import long_to_bytes
import gmpy2
import os

LOCAL = 1
if LOCAL:
    p = process('../src/server/chall.py')
else:
    #p = remote('localhost', 2000)
    p = remote('103.152.242.243', 1524)

encrypted_flag = {}

def encrypt():
    p.recvuntil(b'> ')
    p.sendline(b'1')
    p.recvuntil(b': ')
    p.sendline(b'1')
    e = int(p.recvuntil(b'\n')[4:-1].decode(), 16)
    n = int(p.recvuntil(b'\n')[4:-1].decode(), 16)
    p.recvuntil(b'\n')
    return [e, n]

def get_flag():
    p.recvuntil(b'> ')
    p.sendline(b'2')
    encrypted_flag['e'] = int(p.recvuntil(b'\n')[4:-1].decode(), 16)
    encrypted_flag['n'] = int(p.recvuntil(b'\n')[4:-1].decode(), 16)
    encrypted_flag['flag'] = int(p.recvuntil(b'\n')[12:-1].decode(), 16)

get_flag()
print('encrypted flag:')
print(encrypted_flag)

public_keys = []
r = 100 # should satisfy the delta value so we can get the private key
i = 0
while i < r:
    public_keys.append(encrypt())
    public_keys = sorted(public_keys, key=lambda x : x[1])
    if (public_keys[-1] >= 2 * public_keys[0]):
        del public_keys[-1]
    else:
        i += 1
    print('public keys count:', i)

# create the matrix
M = int(gmpy2.iroot(public_keys[-1][1], 2)[0])
matrix = [[0 for j in range(r + 1)] for i in range(r + 1)]
matrix[0][0] = M
for i in range(r):
    matrix[0][i + 1] = public_keys[i][0]
    matrix[i + 1][i + 1] = -public_keys[i][1]

matrix = str(matrix).replace(',', '')
f = open('matrix', 'w')
f.write(matrix)
f.close()

# do LLL reduction, I use fplll (https://github.com/fplll/fplll)
res = os.popen('fplll -a lll matrix').read()
b1 = int(res.split(' ')[0][2:])
os.system('rm matrix')

# decrypt the encrypted flag
d = abs(b1) // M
print('Flag:', long_to_bytes(pow(encrypted_flag['flag'], d, encrypted_flag['n'])))
