#!/usr/bin/python3
import nbt,io,re
import mca_reader as mcr

FILE = "../src/Hmm/region/r.-1.0.mca"
mca = mcr.Mca(FILE)

# Get Tags nbt tag using regex
RGX = r"""(?<=TAG_String: )(.*?)(?=\n)"""
string = ""
for x in [-15,-16,-17]:
    for y in [2,3]:
        chunk = nbt.nbt.NBTFile(buffer = io.BytesIO(mca.get_data(x,y)))
        string += chunk.pretty_tree() + "\n"
        
# Sort the image chunks based on index 
map_piece = re.findall(RGX,string)
map_lst = [None] * 8
for x in map_piece:
    num = int(x[0])
    byte_arr = [int(n,16) for n in x[3:-1].split(",")]
    map_lst[num] = byte_arr

# Export to final_map.dat file
map_bytes = []
for x in map_lst:
    map_bytes += x
map_nbt = nbt.nbt.NBTFile("template_map.dat")
map_nbt["data"]["colors"].value = bytearray(map_bytes)
map_nbt.write_file("final_map.dat")