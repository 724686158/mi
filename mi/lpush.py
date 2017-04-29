import redis
import mi.settings as settings
print "pushing start_url......"
try:
    r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)
    r.delete("mi_huxiu:start_urls")
    r.delete("huxiu:dupefilter0")
    r.delete("huxiu:requests")

    huxiu_base_url = 'https://www.huxiu.com'
    r.lpush("mi_huxiu:start_urls", huxiu_base_url)
    print "pushing start_url success"
except Exception:
    print "pushing start_url failed"