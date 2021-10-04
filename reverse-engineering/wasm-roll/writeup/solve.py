import os, re

# Require WABT module
os.system("wasm-decompile ../build/index.wasm -o index.c")

# Read flag based on reversing .wasm file
f = open("index.c")
a = f.readlines()

# the flag is on "data d_a" with +10 shifted
flag = ("".join([x.strip().strip('"') for x in a[846:854]])).replace("\\00", "")
flag = bytes(re.sub(r"\\([\w]{2})",r"\\x\1",flag), "utf-8").decode("unicode_escape")
flag = "".join([chr(ord(x)-10) for x in flag])
print(flag)