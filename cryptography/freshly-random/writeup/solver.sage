#!/usr/bin/env sage
from pwn import *
from Crypto.Util.number import GCD, long_to_bytes
from .MTRecover import MT19937Recover
from hashlib import sha256

def gcd(a, b): 
    while b:
        a, b = b, a % b
    return a.monic()

def attack(n, e, pad1, pad2, ct1, ct2):
    R.<X> = PolynomialRing(Zmod(n))
    p1 = (X + pad1) ^ e - ct1
    p2 = (X + pad2) ^ e - ct2
    return -gcd(p1, p2).coefficients()[0]

def random(rand):
    randbits = [rand.getrandbits(32) << 32 * i for i in reversed(range(0, 6))]
    return randbits[0] | randbits[1] | randbits[2] | randbits[3] | randbits[4] | randbits[5]

p = process(["python3", "rsa-1.py"])
ct = []

random_output = []

for i in range(104):
    p.recvuntil("> ")
    p.sendline("1")
    p.recvuntil(": ")
    j = int(p.recvuntil("\n")[:-1].decode('utf-8'), 16)
    random_output.append(int(j >> 160))
    for k in range(4, 0, -1):
        random_output.append(int((j >> (32 * k)) & 0xFFFFFFFF))
    random_output.append(int(j & 0xFFFFFFFF))

rec = MT19937Recover()
rand = rec.go(random_output)

pad1 = int(sha256(long_to_bytes(random(rand))).hexdigest(), 16)
pad2 = int(sha256(long_to_bytes(random(rand))).hexdigest(), 16)

p.recvuntil("> ")
p.sendline("2")

p.recvuntil("e: ")
e = int(p.recvuntil("\n")[:-1], 16)
print("e: " + hex(e))
p.recvuntil("N: ")
N = int(p.recvuntil("\n")[:-1], 16)
print("N: " + hex(N) + "\n")

p.recvuntil("Your encrypted flag is: ")
ct.append(int(p.recvuntil("\n")[:-1], 16))
print("ct_1: " + hex(ct[len(ct) - 1]))

p.recvuntil("> ")
p.sendline("2")
p.recvuntil("Your encrypted flag is: ")
ct.append(int(p.recvuntil("\n")[:-1], 16))
print("ct_2: " + hex(ct[len(ct) - 1]))

print()
print("[+] Flag: " + long_to_bytes(attack(N, e, pad1, pad2, ct[0], ct[1])).decode('utf-8'))
print()

p.close()
