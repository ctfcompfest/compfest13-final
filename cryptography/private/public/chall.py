#!/usr/bin/env python3
from Crypto.Util.number import getPrime, inverse, bytes_to_long
from secret import FLAG
import math

d = getPrime(500)
flag = bytes_to_long(FLAG)

def get_public_key():
    global d
    while True:
        try:
            p = getPrime(512)
            q = getPrime(512)
            n = p * q
            totient = (p - 1) * (q - 1)
            e = inverse(d, totient)
            assert ((e % totient) * (d % totient)) % totient == 1
            return (e, n)
        except:
            continue

def encrypt(message):
    e, n = get_public_key()
    encrypted = pow(message, e, n)
    print('e =', hex(e))
    print('n =', hex(n))
    print('encrypted =', hex(encrypted))

def menu():
    print('1. Encrypt a message')
    print('2. Get encrypted flag')
    print('3. Exit')
    return input('> ')

if __name__ == '__main__':
    try:
        while True:
            choice = menu()
            if (choice == '1'):
                message = int(input('Your message (in hex): '), 16)
                encrypt(message)
            elif (choice == '2'):
                encrypt(flag)
            else:
                print('Bye.')
                break
    except:
        print('Something went wrong.')
