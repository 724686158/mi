import redis
from tld import get_tld
import gentools
import json

HOST = '192.168.139.239'
PORT = 7001


def init():
    r13 = redis.Redis(HOST, PORT, 13)
    r14 = redis.Redis(HOST, PORT, 14)
    for url in r14.lrange(1, 0, -1):
        js = r13.get(get_tld(unicode(url, 'utf8')))
        js = js.replace("'", '"')
        js = js.replace('u"', '"')
        gentools.generate_spider(js)

if __name__ == '__main__':
    init()

