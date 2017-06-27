# -*- coding:utf-8 -*-

import os
import re
import sys
import settings
from itertools import izip
from sklearn.externals import joblib
from sklearn.datasets.base import Bunch

from collections import OrderedDict

CATEGORIES = OrderedDict([
    ['business', []],
    ['politics', []],
    ['health', []],
    ['law', []],
    ['technology', []],
    ['entertainment', []],
    ['military', []],
    ['finance', []],
    ['sport', []]])

def clean(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_data(contents):
    all_data = []
    for content in contents:
        all_data.extend([clean(content)])
    return Bunch(categories=CATEGORIES.keys(),
                 values=None,
                 data=all_data)


def get_type_of_news_by_content(content):
    filename = os.getcwd() + settings.TEMP_PATH +'/training/1498569115.pkl'
    if not filename:
        print "No models found in %s" % 'training'
        sys.exit(1)
    # Load the models using the already generated .pkl file
    model = joblib.load(filename)
    data = get_data([content])
    data_weighted = model['vectorizer'].transform(data.data)
    data_weighted = model['feature_selection'].transform(data_weighted)
    prediction = model['clf'].predict(data_weighted)
    for text, prediction in izip(data.data, prediction):
        return CATEGORIES.keys()[prediction]