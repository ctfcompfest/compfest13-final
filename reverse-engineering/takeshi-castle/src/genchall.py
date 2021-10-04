# ;init
# \xf3\x0f\x1e\xfa\x55\x48\x89\xe5\x48\x89\x7d\xe8
# ; initiate ret var with [00 00 00 00] little endian
# \xc7\x45\xf8 [00 00 00 00]
# ; initiate tmp var with [00 00 00 00] little endian
# \xc7\x45\xfc [00 00 00 00]
#
# ; add tmp var with [00 00 00 00]
# \x81\x45\xfc [00 00 00 00]
# ; subtract tmp var with [00 00 00 00]
# \x81\x6d\xfc [00 00 00 00]
#
# ; mov rax, addr_array
# \x48\x8b\x45\xe8
# ; add rax, [00 00 00 00] little endian
# \x48\x05 [00 00 00 00]
# ; mov edx, tmp_var
# \x8b\x55\xfc
# ; mov arr[rax + [00]], dl
# \x88\x50\x00
# ; mov arr[rax + [01]], dh
# \x88\x70\x01
# ; shl edx, 0xf
# \xc1\xea\x0f
# ; mov arr[rax + [02]], dl
# \x88\x50\x02
# ; mov arr[rax + [03]], dh
# \x88\x70\x03
#
# ; return
# \x8b\x45\xf8\x5d\xc3
from random import randint, shuffle
import struct
import os

MIN_COL = 4
MAX_COL = 112
MIN_ROW = 2
MAX_ROW = 30

F_COL = -2
F_ROW = 18

CODEGRID_MAXLEN = 300

# Banyak tanda tanya di arena + finish
num_grid_max = 153

dC = [-6, 0, +6, +6, 0, -6]
dR = [-2, -4, -2, +2, +4, +2]

# imm* sizenya 32 bit hex little endian
# idx = row * <max_col> + col (all zero-based)
asm = {
    "init": b"\xf3\x0f\x1e\xfa\x55\x48\x89\xe5\x48\x89\x7d\xe8\xc7\x45\xf8\xff\xff\xff\xff\xc7\x45\xfc",
    "add": b"\x81\x45\xfc",
    "sub": b"\x81\x6d\xfc",
    "mov": b"\xc7\x45\xfc",
    "arr":[ b"\x48\x8b\x45\xe8\x48\x05", b"\x8b\x55\xfc\x88\x50\x00\x88\x70\x01\xc1\xea\x10\x88\x50\x02\x88\x70\x03"],
    "ret": b"\x8b\x45\xf8\x5d\xc3",
}

def get_asm(f, n = 0):
    try:
        if f == 'ret': return asm['ret']
        if f == 'arr': return asm['arr'][0] + struct.pack('<i', n) + asm['arr'][1]
        return asm[f] + struct.pack('<i', n)
    except:
        print(n)
        exit(-1)

func = [
    {   
        # xor with y
        "enc": (lambda x, y: x ^ (y & 0xff)),
        "dec": b"\xf3\x0f\x1e\xfa\x55\x48\x89\xe5\x48\x81\xec\x50\x01\x00\x00\x89\xbd\xbc\xfe\xff\xff\x48\x89\xb5\xb0\xfe\xff\xff\xc7\x45\xfc\x00\x00\x00\x00\xeb\x3a\x8b\x85\xbc\xfe\xff\xff\x48\x98\x48\x69\xd0\x2c\x01\x00\x00\x48\x8b\x85\xb0\xfe\xff\xff\x48\x01\xc2\x8b\x45\xfc\x48\x98\x0f\xb6\x04\x02\x8b\x95\xbc\xfe\xff\xff\x31\xc2\x8b\x45\xfc\x48\x98\x88\x94\x05\xc0\xfe\xff\xff\x83\x45\xfc\x01\x81\x7d\xfc\x2b\x01\x00\x00\x7e\xbd\x48\x8d\x85\xc0\xfe\xff\xff\x48\x89\x45\xf0\x48\x8b\x85\xb0\xfe\xff\xff\x48\x8b\x55\xf0\x48\x89\xc7\xff\xd2\xc9\xc3"
    }, {
        # flip bit
        "enc": (lambda x, y: x ^ 0xff),
        "dec": b"\xf3\x0f\x1e\xfa\x55\x48\x89\xe5\x48\x81\xec\x50\x01\x00\x00\x89\xbd\xbc\xfe\xff\xff\x48\x89\xb5\xb0\xfe\xff\xff\xc7\x45\xfc\x00\x00\x00\x00\xeb\x36\x8b\x85\xbc\xfe\xff\xff\x48\x98\x48\x69\xd0\x2c\x01\x00\x00\x48\x8b\x85\xb0\xfe\xff\xff\x48\x01\xc2\x8b\x45\xfc\x48\x98\x0f\xb6\x04\x02\xf7\xd0\x89\xc2\x8b\x45\xfc\x48\x98\x88\x94\x05\xc0\xfe\xff\xff\x83\x45\xfc\x01\x81\x7d\xfc\x2b\x01\x00\x00\x7e\xc1\x48\x8d\x85\xc0\xfe\xff\xff\x48\x89\x45\xf0\x48\x8b\x85\xb0\xfe\xff\xff\x48\x8b\x55\xf0\x48\x89\xc7\xff\xd2\xc9\xc3"
    }, {
        # circular left slide y times
        "enc": (lambda x, y: x >> (8-(y % 8)) | (x & ((1 << (8-(y % 8))) - 1)) << (y % 8)),
        "dec": b"\xf3\x0f\x1e\xfa\x55\x48\x89\xe5\x48\x81\xec\x50\x01\x00\x00\x89\xbd\xbc\xfe\xff\xff\x48\x89\xb5\xb0\xfe\xff\xff\x8b\x85\xbc\xfe\xff\xff\x99\xc1\xea\x1d\x01\xd0\x83\xe0\x07\x29\xd0\x89\x45\xf8\xc7\x45\xfc\x00\x00\x00\x00\xeb\x5a\x8b\x85\xbc\xfe\xff\xff\x48\x98\x48\x69\xd0\x2c\x01\x00\x00\x48\x8b\x85\xb0\xfe\xff\xff\x48\x01\xc2\x8b\x45\xfc\x48\x98\x0f\xb6\x04\x02\x88\x45\xef\x0f\xb6\x55\xef\x8b\x45\xf8\x89\xc1\xd3\xfa\x89\xd0\x89\xc6\x0f\xb6\x55\xef\xb8\x08\x00\x00\x00\x2b\x45\xf8\x89\xc1\xd3\xe2\x89\xd0\x09\xc6\x89\xf2\x8b\x45\xfc\x48\x98\x88\x94\x05\xc0\xfe\xff\xff\x83\x45\xfc\x01\x81\x7d\xfc\x2b\x01\x00\x00\x7e\x9d\x48\x8d\x85\xc0\xfe\xff\xff\x48\x89\x45\xf0\x48\x8b\x85\xb0\xfe\xff\xff\x48\x8b\x55\xf0\x48\x89\xc7\xff\xd2\xc9\xc3"
    }, {
        # circular right slide y times
        "enc": (lambda x, y: x >> (y % 8) | (x & ((1 << (y % 8)) - 1)) << (8 - (y % 8))),
        "dec": b"\xf3\x0f\x1e\xfa\x55\x48\x89\xe5\x48\x81\xec\x50\x01\x00\x00\x89\xbd\xbc\xfe\xff\xff\x48\x89\xb5\xb0\xfe\xff\xff\x8b\x85\xbc\xfe\xff\xff\x99\xc1\xea\x1d\x01\xd0\x83\xe0\x07\x29\xd0\x89\x45\xf8\xc7\x45\xfc\x00\x00\x00\x00\xeb\x5a\x8b\x85\xbc\xfe\xff\xff\x48\x98\x48\x69\xd0\x2c\x01\x00\x00\x48\x8b\x85\xb0\xfe\xff\xff\x48\x01\xc2\x8b\x45\xfc\x48\x98\x0f\xb6\x04\x02\x88\x45\xef\x0f\xb6\x55\xef\xb8\x08\x00\x00\x00\x2b\x45\xf8\x89\xc1\xd3\xfa\x89\xd0\x89\xc6\x0f\xb6\x55\xef\x8b\x45\xf8\x89\xc1\xd3\xe2\x89\xd0\x09\xc6\x89\xf2\x8b\x45\xfc\x48\x98\x88\x94\x05\xc0\xfe\xff\xff\x83\x45\xfc\x01\x81\x7d\xfc\x2b\x01\x00\x00\x7e\x9d\x48\x8d\x85\xc0\xfe\xff\xff\x48\x89\x45\xf0\x48\x8b\x85\xb0\xfe\xff\xff\x48\x8b\x55\xf0\x48\x89\xc7\xff\xd2\xc9\xc3"
    }, {
        # reverse
        "enc": (lambda x, y: int(bin(x)[2:].rjust(8, '0')[::-1], 2)),
        "dec": b"\xf3\x0f\x1e\xfa\x55\x48\x89\xe5\x48\x81\xec\x60\x01\x00\x00\x89\xbd\xac\xfe\xff\xff\x48\x89\xb5\xa0\xfe\xff\xff\xc7\x45\xfc\x00\x00\x00\x00\xe9\x9f\x00\x00\x00\xc7\x45\xf8\x08\x00\x00\x00\x8b\x85\xac\xfe\xff\xff\x48\x98\x48\x69\xd0\x2c\x01\x00\x00\x48\x8b\x85\xa0\xfe\xff\xff\x48\x01\xc2\x8b\x45\xfc\x48\x98\x0f\xb6\x04\x02\x0f\xbe\xc0\x89\x45\xf4\x8b\x85\xac\xfe\xff\xff\x48\x98\x48\x69\xd0\x2c\x01\x00\x00\x48\x8b\x85\xa0\xfe\xff\xff\x48\x01\xc2\x8b\x45\xfc\x48\x98\x0f\xb6\x04\x02\x89\xc2\x8b\x45\xfc\x48\x98\x88\x94\x05\xb0\xfe\xff\xff\xeb\x2d\x8b\x45\xfc\x48\x98\x0f\xb6\x84\x05\xb0\xfe\xff\xff\x0f\xb6\xc0\x01\xc0\x89\xc2\x8b\x45\xf4\x83\xe0\x01\x09\xd0\x89\xc2\x8b\x45\xfc\x48\x98\x88\x94\x05\xb0\xfe\xff\xff\xd1\x7d\xf4\x8b\x45\xf8\x8d\x50\xff\x89\x55\xf8\x85\xc0\x75\xc6\x83\x45\xfc\x01\x81\x7d\xfc\x2b\x01\x00\x00\x0f\x8e\x54\xff\xff\xff\x48\x8d\x85\xb0\xfe\xff\xff\x48\x89\x45\xe8\x48\x8b\x85\xa0\xfe\xff\xff\x48\x8b\x55\xe8\x48\x89\xc7\xff\xd2\xc9\xc3"
    },
]

def is_inside_arena(r, c):
	return ((MIN_ROW <= r <= MAX_ROW) and (MIN_ROW <= c <= MAX_COL))

def is_finished_coor(r, c):
	return (r == F_ROW and c == F_COL)

def coor_to_idx(r, c):
    if is_finished_coor(r, c):
        return num_grid_max - 1
    ret = c // 12 + 10 * ((r % 4) // 2) + (r - 1) // 4 * 19
    return ret

def idx_to_coor(i):
    if i == -1 or i == num_grid_max - 1:
        return F_ROW, F_COL
    g = i // 19
    ig = (i % 19) < 10
    r = 4 * g + 2 * (ig + 1)
    offset = 4 + 6 * (ig ^ 1)
    c = (i % 19 % 10) * 12 + offset
    return r, c

def generate_gridfunc(r, c, f, g, retinit = None):
    bcode = b""
    idx = coor_to_idx(r, c)
    seq = [i for i in range(6)]
    shuffle(seq)

    accum = randint(0, 255)
    bcode = bcode + get_asm('init', accum)
    if retinit != None:
        bcode = bcode[:15] + struct.pack('<i', retinit) + bcode[19:]
    for e in seq:
        if g[e] == 0: continue
        tR = r + dR[e]
        tC = c + dC[e]
        if not(is_inside_arena(tR, tC) or is_finished_coor(tR, tC)):
            continue
        diff = abs(accum - g[e])
        if diff > 2147483647:
            bcode = bcode + get_asm('mov', g[e])
        else:
            if accum > g[e]: tipe = 'sub'
            else: tipe = 'add'
            bcode = bcode + get_asm(tipe, diff)
        
        tidx = coor_to_idx(tR, tC) * CODEGRID_MAXLEN + len(asm['init']) - 7
        bcode = bcode + get_asm('arr', tidx)
        accum = g[e]
    bcode = bcode + get_asm('ret')
    return bytes([f(e, idx) for e in bcode])

def chex(s):
    ret = ''.join(["\\x{:02x}".format(e) for e in s])
    return ret

def printsource(obs_idxdec, decfunc, grid_func):
    decfunc_str = "char insdec[5][300] = {\n"
    for e in decfunc: decfunc_str = decfunc_str + f"  \"{e}\",\n"
    decfunc_str = decfunc_str[:-2] + "\n};\n"

    gridfunc_str = "char insgrid[][300] = {\n"
    for e in grid_func: gridfunc_str = gridfunc_str + f"  \"{e}\",\n"
    gridfunc_str = gridfunc_str[:-2] + "\n};\n"
    obsidx_str = "int insdec_idx[] = {" + str(obs_idxdec)[1:-1] + "};\n"

    txt = ""
    with open('takeshi.part1') as f:
        txt = f.read()
    txt += obsidx_str
    txt += decfunc_str
    txt += gridfunc_str

    with open('takeshi.part2') as f:
        txt += f.read()
    with open('takeshi.c', 'w+') as f:
        f.write(txt)
    os.system("./compile.sh takeshi.c")

def main():
    def disguise_val(idx):
        v = grid_val[idx]
        tmp = grid_idx_decfunc[idx]
        f = func[tmp]['enc']
        
        tmp = struct.pack('i', v)
        tmp = bytes([f(e, idx) for e in tmp])
        return struct.unpack('i', tmp)[0]

    def obsfucate(prn):
        return [-(e + 1) for e in prn]

    def get_adjval(r, c):
        retv = [0 for _ in range(6)]
        for i in range(6):
            tR, tC = r + dR[i], c + dC[i]
            if is_inside_arena(tR, tC) or is_finished_coor(tR, tC):
                idx = coor_to_idx(tR, tC)
                retv[i] = disguise_val(idx)
        return retv

    def DFS(pos, cost):
        grid_val[pos] = cost
        for nxt in adjlist[pos]:
            if grid_val[nxt[0]] != 0: continue
            DFS(nxt[0], cost + nxt[1])

    shuffle(func)
    decfunc = [chex(e["dec"]) for e in func]

    grid_idx_decfunc = [randint(0, len(func) - 1) for _ in range(num_grid_max)]
    grid_val = [0 for _ in range(num_grid_max)]
    grid_func = [b"" for _ in range(num_grid_max)]
    
    start_grid = list(map(int, input().split(" ")))
    monster_grid = list(map(int, input().split(" ")))
    adjlist = [[] for _ in range(num_grid_max)]
    
    try:
        while True:
            inp = input().split(" ")
            u, v = int(inp[0]), int(inp[1])
            cost = randint(0, 255)
            if len(inp) > 2:
                cost = ord(inp[2])
            adjlist[u].append([v, cost])
    except:
        pass
    
    for monster in monster_grid:
        grid_val[monster] = -1
    for start in start_grid:
        tmp = randint(0, 255)
        DFS(start, tmp)
    
    for i in range(num_grid_max):
        r, c = idx_to_coor(i)
        did = grid_idx_decfunc[i]
        adjv = get_adjval(r, c)
        # print(i, grid_idx_decfunc[i], grid_val[i], disguise_val(i), adjv)
        if i in start_grid:
            ret = generate_gridfunc(r, c, func[did]['enc'], adjv, grid_val[i])
        else:
            ret = generate_gridfunc(r, c, func[did]['enc'], adjv)
        grid_func[i] = chex(ret)

    obs_idxdec = obsfucate(grid_idx_decfunc)

    printsource(obs_idxdec, decfunc, grid_func)

if __name__ == "__main__":
    main()