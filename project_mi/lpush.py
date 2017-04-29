import redis

try:
    r = redis.Redis(host="192.168.139.239", port=7001)
    r.delete("huxiu:start_urls")
    huxiuBaseUrl='https://www.huxiu.com'
    r.lpush("huxiu:start_urls", huxiuBaseUrl)
    print("success")
except Exception:
    print("failed")


