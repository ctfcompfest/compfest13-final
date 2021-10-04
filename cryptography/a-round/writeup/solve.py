from around import ARound, inv_shift_rows, inv_mix_columns, bytes2matrix, matrix2bytes, s_box
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long as bl, long_to_bytes as lb
from Crypto.Util.Padding import unpad
import hashlib

plaintexts = ['69688aa7921a6ce8cce0978a498c9534', '6c5fcc589f8c1434f091d2b9f998d984']
ciphertexts = ['f449e6fb3a8cd7bc15fac37263258c6f', '178a0d3d2b51d0797e75ab2d4b6d8eeb']
iv ='ca26d15af120695f03e5ddbf8829b5b2'
encrypted_flag = 'fe1f37da171cf09c0ff91261d3bf81bdc3811475857fe64fe00e7040327b46bab3220a9cab6b7fed9f76d560ac5eaa1c471a6b2b9057cf35b11035894ca5b480'

p1 = lb(int(plaintexts[0], 16))
p2 = lb(int(plaintexts[1], 16))

c1 = lb(int(ciphertexts[0], 16))
c2 = lb(int(ciphertexts[1], 16))

iv = lb(int(iv, 16))
encrypted_flag = lb(int(encrypted_flag, 16))

c_diff = lb(bl(c1) ^ bl(c2))
matrix_output_diff = bytes2matrix(c_diff)
inv_mix_columns(matrix_output_diff)
inv_shift_rows(matrix_output_diff)
output_diff = matrix2bytes(matrix_output_diff)

possible_key = [[] for i in range(16)]

for x in range(16):
    for i in range(256):
        for j in range(256):
            if (((i ^ j) == (p1[x] ^ p2[x])) and ((s_box[i] ^ s_box[j]) == output_diff[x])):
                possible_key[x].append(i ^ p1[x])

def get_next_key():
    for k0 in possible_key[0]:
        for k1 in possible_key[1]:
            for k2 in possible_key[2]:
                for k3 in possible_key[3]:
                    for k4 in possible_key[4]:
                        for k5 in possible_key[5]:
                            for k6 in possible_key[6]:
                                for k7 in possible_key[7]:
                                    for k8 in possible_key[8]:
                                        for k9 in possible_key[9]:
                                            for k10 in possible_key[10]:
                                                for k11 in possible_key[11]:
                                                    for k12 in possible_key[12]:
                                                        for k13 in possible_key[13]:
                                                            for k14 in possible_key[14]:
                                                                for k15 in possible_key[15]:
                                                                    yield bytes([k0, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15])

for checked_key in get_next_key():
    try:
        cipher = ARound(checked_key)
        if (cipher.encrypt_block(p1) == c1 and cipher.encrypt_block(p2) == c2):
            key = checked_key
            break
    except:
        pass

sha1 = hashlib.sha1()
sha1.update(str(key).encode())
print(key)
new_key = sha1.digest()[:16]

cipher = AES.new(new_key, AES.MODE_CBC, IV=iv)
flag = unpad(cipher.decrypt(encrypted_flag), 16)
print(flag.decode())
