# coding=utf-8
import re


def calc_score(url):
    score = 0

    # 文章关键词
    PAT = ('news', 'article', 'story', 'content', 'xinwen', 'detail', 'view', 'a')
    for i in PAT:
        if i in url:
            score += 2

    # 类似 news_good_110
    for i in PAT:
        a = re.findall(i + r'[-_/]?[a-z0-9]+[-_/]\d+', url)
        if len(a) > 0:
            score += 2

    # 日期，年月
    a = re.findall(r'20[01]\d[-/_]?\d\d', url)
    if len(a) > 0:
        score += 2

    # 省略20的日期，年月日，新增识别不带前导零
    a = re.findall(r'1[0-7][-/_]?[0-1]?\d[-/_]?[0-3]?\d', url)
    if len(a) > 0:
        score += 2

    # 类似 abc-def-ghi-good-you-hehehe 的长串
    a = re.findall(r'([a-zA-Z]{2,12}-)+[a-zA-Z]{2,12}', url)
    if len(a) > 0:
        score += 1

    # 类似 /abc123-10086. 的串
    a = re.findall(r'/[a-z0-9]+[-_]\d+\.', url)
    if len(a) > 0:
        score += 1

    # 类似 /100sb86.html 的串
    a = re.findall(r'/[0-9a-z]{3,20}.s?htm', url)
    if len(a) > 0:
        score += 1

    return score


if __name__ == '__main__':
    with open('articles_urls.txt') as f:
        for i in f:
            i = i.strip()
            print calc_score(i), i
