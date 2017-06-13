# -*- coding: utf-8 -*-
import re
from tld import get_tld
def calc_score(url):
    score = 0
    # 先去除url内的域名部分
    domain = get_tld(url, fail_silently=True)
    url = url.replace(domain, '')

    # 文章关键词
    PAT = ('news', 'article', 'story', 'content', 'xinwen', 'detail', 'view', 'edition', 'essay', '/a/', 'p=', 'id=', 'archives', 'newsshow', '/a-')
    for i in PAT:
        if i in url:
            score += 2
            # 类似 news_xxxx_110
            a = re.findall(i + r'[-_/]?\w*[-_/]?\d+', url)
            if len(a) > 0:
                score += 2

    # 日期,年月
    a = re.findall(r'20[01]\d[-/_]?\d\d', url)
    if len(a) > 0:
        score += 2

    # 省略20的日期,年月日,新增识别不带前导零
    a = re.findall(r'1[0-7][-/_]?[0-1]?\d[-/_]?[0-3]?\d', url)
    if len(a) > 0:
        score += 2

    # 类似 /yule/3344.html 或者 /yule/3344-2.html 的串
    a = re.findall(r'/[a-zA-Z0-9]{4,}/\d{2,}[-/_]?\d?.s?htm', url)
    if len(a) > 0:
        score += 2

    # 类似 www.ftchinese.com/interactive/9183, 在域名后面直接接单词段, 再接三位以上数字段, 并直接结尾
    a = re.findall(r'./[a-zA-Z0-9]{3,}/\d{3,}$', url)
    if len(a) > 0:
        score += 2

    # 类似 abc-def-ghi-xxx-XXx-xxxxXXXxxx 的长串
    a = re.findall(r'([a-zA-Z0-9]{2,12}-)+[a-zA-Z]{2,12}', url)
    if len(a) > 0:
        score += 1

    # 类似 /sin86.html 的串
    a = re.findall(r'/[0-9a-zA-Z]{3,20}.s?htm', url)
    if len(a) > 0:
        score += 1

    # 类似 /100xx86.html 的串
    a = re.findall(r'/[0-9a-zA-Z]{3,20}.s?htm', url)
    if len(a) > 0:
        score += 1

    # 含有3位以上数字串,且数字串右侧带.html
    a = re.findall(r'/[0-9]{3,}.s?htm', url)
    if len(a) > 0:
        score += 1

    # 含有3位以上数字串,且数字串右侧带/,且以此结束
    a = re.findall(r'/[0-9]{3,}/$', url)
    if len(a) > 0:
        score += 1
        
    # 含有3位以上数字串,且以此结束
    a = re.findall(r'/[0-9]{3,}$', url)
    if len(a) > 0:
        score += 1
    return score