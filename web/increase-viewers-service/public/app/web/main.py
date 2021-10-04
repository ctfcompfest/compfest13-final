from flask import Flask, render_template, request, jsonify
from cache import get_cache_data, set_cache_data
from mailers import blast_email
from rss import parse_rss

import redis
import os

app = Flask(__name__)

REDIS_CONF = {
    "host": os.getenv('REDIS_HOST', 'localhost'),
    "port": int(os.getenv('REDIS_PORT', 6379))
}
conn = redis.Redis(host = REDIS_CONF['host'], port = REDIS_CONF['port'])

@app.route('/promote',methods = ['POST'])
def promote():    
    data = request.json
    try:
        link = data.get("link")
        rss = data.get("rss")
        if link == None or rss == None:
            raise Exception("Invalid form")
        old_res = get_cache_data(conn, link)
        if old_res == None:
            chan = parse_rss(rss)
            blast_email(chan)
        elif old_res == 0:
            raise Exception("Invalid RSS")
    except Exception as e:
        set_cache_data(conn, link, 0)
        return jsonify({"status": "error"}), 500
    set_cache_data(conn, link, 1)
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=False)