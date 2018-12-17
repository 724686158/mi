# -*- coding: utf-8 -*-
import time
import classifier
import jieba
import jieba.analyse
from goose import Goose
from goose.text import StopWordsChinese


class GooseHelper():

    '''
    还没有做线程方面的优化, 处理50个url的时间在60秒左右
    '''

    def __init__(self):
        self.english_goose = Goose()
        self.chinese_goose = Goose({'stopwords_class': StopWordsChinese})

    # 根据url获取新闻
    def get_news_of_urls(self, urls):
        start_time = time.time()
        data = []
        data.append(('url', '新闻标题', '新闻正文', '关键词', '新闻类别'))
        for url in urls:
            article_default = self.english_goose.extract(url=url)
            if article_default:
                title = article_default.title
                content = article_default.cleaned_text
                if len(content) == 0 or len(title) == 0:
                    article_chinese = self.chinese_goose.extract(url=url)
                    if article_chinese:
                        if len(content) == 0:
                            content = article_chinese.cleaned_text
                        if len(title) == 0:
                            title = article_chinese.title
                if len(title) == 0:
                    title = '爬取请求被拒绝, 请参考此网站的robots.txt'
                if len(content) == 0:
                    content = '爬取请求被拒绝, 请参考此网站的robots.txt'
                keywords = ''
                if len(content) > 0:
                    tags = jieba.analyse.extract_tags(content, topK=20, withWeight=5)
                    keywords = ''.join(tags[0][0]) + ' '.join(tags[1][0]) + ' '.join(tags[2][0])
                t = (url, title, content, keywords, classifier.get_type_of_news_by_content(content))
                data.append(t)
        end_time = time.time()
        print '耗时:' + str(end_time - start_time) + '秒'
        return data
