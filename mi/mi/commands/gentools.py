# -*- coding: utf-8 -*-
import json
def arr2str(arr):
    return ', '.join(map(lambda x: "'" + x + "'", arr))

#新闻类爬虫模板
spider_template = \
"""# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import jieba.analyse
class Spider_%s(RedisCrawlSpider):
    name = '%s'
    redis_key = '%s:start_urls'
    allowed_domains = [%s]
    rules = [
        Rule(LinkExtractor(allow=(%s),deny=(%s)),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath(''%s'').extract()[0]
            content = ''.join(response.xpath(''%s'').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            tags = jieba.analyse.extract_tags(content, topK=20, withWeight=5)
            item['articleFirstTag'] = ''.join(tags[0][0])
            item['articleSecondTag'] = ''.join(tags[1][0])
            item['articleThirdTag'] = ''.join(tags[2][0])
            yield item
        except:
            self.logger.info('item in article failed')

"""
def generate_spider(jsonfile):
    print jsonfile
    print '111111111111111\n'
    print type(jsonfile)
    js = dict(json.loads(jsonfile))

    arr = (
        js['name'],
        js['name'],
        js['name'],
        arr2str(js['allowed_domains']),
        arr2str(js['rule_allow']),
        arr2str(js['rule_deny']),
        arr2str(js['xpath_title']),
        arr2str(js['xpath_content']))
    ok = spider_template % arr
    filename = "../spiders/" + 'spider_'+ js['name'] + '.py'
    with open(filename, 'w') as f:
        f.write(ok.encode('utf8'))
#爬虫初始化模板
spider_init_template = \
"""# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing %s_start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("%s:start_urls")
        r.delete("%s:dupefilter" + "0")
        r.delete("%s:requests")
        r.lpush("%s:start_urls", %s)
        print "pushing %s_start_url success"
    except Exception:
        print "pushing %s_start_url failed"
if __name__ == '__main__':
    init()
"""
def generate_spider_init(jsonfile):
    print jsonfile
    js = dict(json.loads(jsonfile))
    arr = (
        js['name'],
        js['name'],
        js['name'],
        js['name'],
        js['name'],
        arr2str(js['start_urls']),
        js['name'],
        js['name'])
    ok = spider_init_template % arr
    filename = "../commands/" + "spiderInit_" + js['name'] + ".py"
    with open(filename, 'w') as f:
        f.write(ok)

if __name__ == '__main__':
    sss = """{"name":"caijing","start_urls":["http://www.caijing.com.cn"],"allowed_domains":["caijing.com.cn"],"rule_allow":["caijing.com.cn/\\\\d{8}/\\\\d*"],"rule_deny":[".*photos.*",".*politics.*"],"xpath_title":["/html/body/div[@class='center']/div[@class='content']/div/div/div[@id='article']/h2/text()"],"xpath_content":["/html/body/div[@class='center']/div[@class='content']/div[@class='main']/div/div[@id='article']/div[@id='the_content']/p/text()"]}"""
    generate_spider(sss)
    generate_spider_init(sss)

