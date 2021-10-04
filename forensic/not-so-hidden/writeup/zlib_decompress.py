from zipfile import ZipFile
import zlib
import os

os.chdir("hexstream\writeupcheck")
with open('compressedimg', "rb") as file:
    data = file.read()

data = b"\x78\x9c" + data + b"\x03\xb0\x2a\xb9"
data = zlib.decompress(data)

with open("flag.png", 'wb') as file:
    file.write(data)