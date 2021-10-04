import os
import psutil

PROC = ["crond", "redis-server"]
CMD = {
    "crond": "crond",
    "redis-server": "docker-entrypoint.sh redis-server redis.conf"
}

def reset_redis():
    os.system("redis-cli config rewrite")

def main():
    illegal = []
    reset_redis()
    proc_set = set(PROC)
    for p in psutil.process_iter():
        if p.name() in proc_set:
            proc_set.remove(p.name())
        else:
            illegal.append(str(p.pid))
    for p in proc_set:
        os.system(CMD[p])

    illegal = ' '.join(illegal)
    os.system(f"kill -9 {illegal}")

if __name__ == "__main__":
    main()