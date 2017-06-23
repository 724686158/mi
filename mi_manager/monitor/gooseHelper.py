# -*- coding: utf-8 -*-
from goose import Goose
from goose.text import StopWordsChinese

class GooseHelper():

    def __init__(self):
        self.english_goose = Goose()
        self.chinese_goose = Goose({'stopwords_class': StopWordsChinese})

    # 根据url获取新闻
    def get_news_of_urls(self, urls):
        data = []
        data.append(('url', '新闻标题', '新闻正文', '新闻类别'))
        for url in urls:
            article = self.english_goose.extract(url=url)
            title = article.title
            content = article.cleaned_text
            if len(content) == 0:
                print 'news in chinese'
                article = self.chinese_goose.extract(url=url)
                if len(title) == 0:
                    title = article.title
                    content = article.cleaned_text
                    t = (url, title, content)
                    data.append(t)
        return data
            