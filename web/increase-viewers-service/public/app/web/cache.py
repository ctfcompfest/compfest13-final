from flask import request
from urllib.parse import urlparse

import time

def set_cache_data(con, link, res):
    host = urlparse(link).netloc
    msg_log = f"{time.asctime()} {request.remote_addr} {host}"
    res_des = f"result:{host}"

    pipe = con.pipeline()
    pipe.incr('visitor')
    pipe.lpush('logs', msg_log)
    pipe.ltrim('logs', 0, 99)

    if link == None: return
    pipe.set(res_des, res, 60 * 15)
    pipe.execute()

def get_cache_data(con, link):
    res_des = f"result:{link}"
    return con.get(res_des)
