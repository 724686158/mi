# -*- coding: utf-8 -*-
import json
from flask import Flask, render_template, jsonify, request, current_app, redirect
import redis
from monitor_settings import *
from gen_spiderInitfile import *
import dat_service
import url_extract_tools

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/static/index.html')


@app.route('/monitor')
def monitor():
    return render_template('index.html',
                           timeinterval=TIMEINTERVAL,
                           stats_keys=STATS_KEYS,
                           spider_name=request.args.get('spider_name'))


@app.route('/ajax')
def ajax():
    key = request.args.get('key')
    result = current_app.r.lrange(key, -POINTLENGTH, -1)[::POINTINTERVAL]
    if not current_app.spider_is_run:
        # spider is closed
        return json.dumps(result).replace('"', ''), 404
    return json.dumps(result).replace('"', '')


@app.route('/signal')
def signal():
    signal = request.args.get('sign')
    if signal == 'closed':
        current_app.spider_is_run = False
    elif signal == 'running':
        current_app.spider_is_run = True
    return jsonify('')


@app.route('/gen_spider', methods=['GET', 'POST'])
def gen_spider():
    jsonstr = request.form.get('json_result', '')
    js = dict(json.loads(jsonstr))
    start_urls = list(js['start_urls'])
    spider_name = url_extract_tools.extract_main_url(start_urls)
    dat_service.save_data(spider_name, jsonstr)
    generate_spider_init(jsonstr)
    return jsonify('ok')


@app.route('/add_ips', methods=['GET', 'POST'])
def add_ips():
    jsonstr = request.form.get('ips', '')
    ips_array = json.loads(jsonstr)['ips']
    print ips_array
    with open('static/valid_proxy.txt', 'w') as f:
        for i in ips_array:
            f.write(i + '\n')
    return jsonify('ok')


@app.route('/target_urls', methods=['GET', 'POST'])
def target_urls():
    jsonstr = request.form.get('urls', '')
    urls_array = json.loads(jsonstr)['urls']
    print dat_service.split_target_urls(urls_array)
    return jsonify('ok')


@app.route('/get_spider_names', methods=['GET'])
def get_spider_names():
    return jsonify(dat_service.get_spider_count_from_db())


@app.before_first_request
def init():
    current_app.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    current_app.spider_is_run = True if current_app.r.get('spider_is_run') == '1' else False


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
