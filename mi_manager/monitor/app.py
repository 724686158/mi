# -*- coding: utf-8 -*-
import redis
import json
import os
import data_service
import settings
import url_extract_tools
import base64

from flask import Flask, render_template, jsonify, request, current_app, redirect, send_from_directory, abort
from gen_spiderInitfile_of_news import generate_spider_init

app = Flask(__name__)
app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__)) # app.py所在的目录
app.config['UPLOAD_FOLDER'] = 'upload' # 用文件夹‘upload’来存储新上传的文件

# 用于判断文件后缀

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ['txt','png','PNG','jpg','JPG','gif','GIF','xls','xlsx']

@app.route('/')
def index():
    return redirect('/static/v2/login.html')

@app.route('/static/v2/swaplayer')
def to_real_index():
    return redirect('/static/v2/starter.html')

@app.before_first_request
def init():
    current_app.r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.MONITOR_DB)

# 用于测试上传
@app.route('/test/upload')
def upload_test():
    return render_template('upload.html')

# 上传文件
@app.route('/api/upload',methods=['POST'],strict_slashes=False)
def api_upload():
    file_dir=os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f=request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f.save(os.path.join(file_dir,f.filename))  #保存文件到upload目录
        token = base64.b64encode(f.filename)
        print token
        return jsonify({"msg":"upload success","token":token})
    else:
        return jsonify({"errno":1001,"errmsg":"upload fail"})

@app.route('/api/download',methods=['GET'],strict_slashes=False)
def download():
    filename = request.args.get('filename')
    if filename is None:
        filename = 'swap.txt'
    if request.method=="GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload',filename,as_attachment=True)
        abort(404)


@app.route('/monitor')
def monitor():
    return render_template('index.html',
                           timeinterval=settings.TIMEINTERVAL,
                           stats_keys=settings.STATS_KEYS,
                           spider_name=request.args.get('spider_name'))

@app.route('/ajax')
def ajax():
    key = request.args.get('key')
    result = current_app.r.lrange(key, -settings.POINTLENGTH, -1)[::settings.POINTINTERVAL]
    return json.dumps(result).replace('"', '')

@app.route('/gen_spider', methods=['GET', 'POST'])
def gen_spider():
    jsonstr = request.form.get('json_result', '')
    js = dict(json.loads(jsonstr))
    start_urls = list(js['start_urls'])
    spider_name = url_extract_tools.extract_main_url(start_urls)
    data_service.save_data(spider_name, jsonstr)
    return jsonify('ok')

# 旧API, 勿用
'''
@app.route('/add_ips', methods=['GET', 'POST'])
def add_ips():
    jsonstr = request.form.get('ips', '')
    ips_array = json.loads(jsonstr)['ips']
    dat_service.save_proxys(ips_array)
    return jsonify('ok')
'''

@app.route('/target_urls', methods=['GET', 'POST'])
def target_urls():
    jsonstr = request.form.get('urls', '')
    urls_array = json.loads(jsonstr)['urls']
    data_service.split_target_urls(urls_array)
    return jsonify('ok')

@app.route('/get_spider_names', methods=['GET'])
def get_spider_names():
    return jsonify(data_service.get_spider_count_from_db())

@app.route('/start_work', methods=['GET'])
def get_start_work():
    # 初始化监控器数据
    data_service.init_monitor()
    # 初始化mysql数据库
    data_service.init_mysql()
    #
    data_service.exec_init_of_missions()
    #
    return jsonify('ok')

# 慎用
@app.route('/init_monitor', methods=['GET'])
def init_monitor():
    return jsonify(data_service.init_monitor())

# 在个API暂时没有实际意义
@app.route('/init_mysql', methods=['GET'])
def init_mysql():
    return jsonify(data_service.init_mysql())

@app.route('/get_table', methods=['GET'])
def get_table():
    table_name = request.args.get('table_name')
    if table_name is None:
        data_dic = []
    if(table_name == 'Article'):
        data_dic = data_service.get_data_from_mongo(table_name)
    elif(table_name == 'ECommerce' or table_name == 'ECommerceShop' or table_name == 'ECommerceShopComment' or table_name == 'ECommerceGood' or table_name == 'ECommerceGoodComment'):
        data_dic = data_service.get_data_from_mysql(table_name)
    return jsonify(data_dic)

# 获取电商爬虫名
@app.route('/get_ecommerce_spider_name', methods=['GET'])
def get_ecommerce_spider_name():
    data = data_service.get_ecommerce_spider_name()
    return jsonify(data)

# 获取新闻爬虫名
@app.route('/get_news_spider_name', methods=['GET'])
def get_news_spider_name():
    data = data_service.get_news_spider_name()
    return jsonify(data)

# 获取新闻爬虫描述
@app.route('/get_news_spider_describe', methods=['GET'])
def get_news_spider_describe():
    name = request.args.get('name')
    data = data_service.get_news_spider_describe(name)
    return jsonify(data)

# 获取爬虫配置
@app.route('/get_spider_info', methods=['GET'])
def get_spider_info():
    key = request.args.get('key')
    r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=settings.SPIDERS_DB)
    res = r.get(key)
    dic = eval(res)
    ss = json.dumps(dic)
    return ss


# 删除白名单中的一条记录，形式：/delte_spider?key=163.com
@app.route('/delte_spider', methods=['GET'])
def delect_news_in_whitelist():
    key = request.args.get('key')
    print key
    data_service.delete_news_in_whitelist(key)
    return jsonify('ok')

# 清空白名单
@app.route('/delte_all_spider', methods=['GET'])
def clear_whitelist():
    data_service.clear_whitelist()
    return jsonify('ok')


# 白名单批量导入，注意是POST，文本参数在变量txt里
@app.route('/batch_import_spider', methods=['POST'])
def batch_import_whitelist_of_news():
    txt = request.form.get('txt', '')
    try:
        data_service.batch_import_whitelist_of_news(txt)
        print '已批量导入..'
        return jsonify('ok')
    except:
        print '导入失败'

# 白名单批量导出
@app.route('/batch_export_spider', methods=['GET'])
def batch_export_whitelist_of_news():
    ans = data_service.batch_export_whitelist_of_news()
    return ans

# 代理IP批量导入
@app.route('/batch_import_proxy', methods=['POST'])
def batch_import_proxy():
    txt = request.form.get('txt', '')
    try:
        data_service.batch_import_proxys(txt)
        print '已批量导入..'
        return jsonify('ok')
    except:
        print '导入失败'

# 获取全部代理IP
@app.route('/get_all_proxy', methods=['GET'])
def get_all_proxy():
    data = data_service.get_all_proxy()
    return jsonify(data)

# 清空代理IP
@app.route('/delte_all_proxy', methods=['GET'])
def clear_proxys():
    data_service.clear_proxys()
    return jsonify('ok')

# 删除一个http代理，形式：/delte_proxy?proxy=http://36.97.145.29:9797
@app.route('/delte_proxy', methods=['GET'])
def delte_proxy():
    proxy = request.args.get('proxy')
    print proxy
    data_service.delte_proxy(proxy)
    return jsonify('ok')

# 清空去重用的redis数据库,此功能慎用
@app.route('/delte_filter_db', methods=['GET'])
def delte_filter_db():
    data_service.delte_filter_db()
    return jsonify('ok')

# 用于添加资源(redis,mysql,mongo)
@app.route('/add_resources', methods=['POST'])
def add_resources():
    jsonstr = request.form.get('json_result', '')
    dic = dict(json.loads(jsonstr))
    name = dic['name']
    type = dic['type']
    info_dic = dict(dic['detail'])
    if type == 'Redis':
        data_service.add_resources_redis(name, info_dic)
    elif type == 'Mysql':
        data_service.add_resources_mysql(name, info_dic)
    elif type == 'Mongo':
        data_service.add_resources_mongo(name, info_dic)
    return jsonify('ok')

# 获取所有资源的信息 如果带参数type, 则只返回一种类型的资源（可选值： Redis Mysql Mongo）
@app.route('/get_resources', methods=['GET'])
def get_resources():
    type = request.args.get('type')
    data = []
    if type:
        if type == 'Redis':
            data = data_service.get_resources_redis()
        elif type == 'Mysql':
            data = data_service.get_resources_mysql()
        elif type == 'Mongo':
            data = data_service.get_resources_mongo()
    else:
        data = data_service.get_resources_redis() + data_service.get_resources_mysql() + data_service.get_resources_mongo()
    return jsonify(data)

@app.route('/delete_resources', methods=['GET'])
def delete_resources():
    name = request.args.get('name')
    type = request.args.get('type')
    data_service.delete_resources(name, type)
    return jsonify('ok')



# 用于添加Settings
@app.route('/add_settings', methods=['POST'])
def add_settings():
    '''
    json example:
    {
        "name": "配置1",
        "detail": {
            "ROBOTSTXT_OBEY": true,
            "COOKIES_ENABLED": true,
            "RETRY_ENABLED": false,
            "HTTP_PROXY_ENABLED": true,
            "AUTOTHROTTLE_ENABLED": false,
            "AUTOTHROTTLE_START_DELAY": 1,
            "AUTOTHROTTLE_MAX_DELAY": 6,
            "DOWNLOAD_DELAY": 0.5,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 20,
            "DOWNLOAD_TIMEOUT": 10
        }
    }
    '''
    jsonstr = request.form.get('json_result', '')
    dic = dict(json.loads(jsonstr))
    name = dic['name']
    info_dic = dict(dic['detail'])
    data_service.add_settings(name, info_dic)
    return jsonify('ok')

@app.route('/delete_settings', methods=['GET'])
def delete_settings():
    name = request.args.get('name')
    data_service.delete_settings(name)
    return jsonify('ok')

# 获取所有设置的信息,包含名字和内容
@app.route('/get_settings', methods=['GET'])
def get_settings():
    data = data_service.get_settings()
    return jsonify(data)

# 获取所有设置的名字
@app.route('/get_settings_name', methods=['GET'])
def get_settings_name():
    data = data_service.get_settings_name()
    return jsonify(data)

# 用于添加子任务
@app.route('/add_submission', methods=['POST'])
def add_submission():
    '''
    {
        "name": "mission1_jd.com",
        "detail": {
            "spider_name": "jd.com",
            "father_mission_name": "mission1",
            "settings": "默认设置1",
            "priority": 5
        }
    }
    '''
    jsonstr = request.form.get('json_result', '')
    dic = dict(json.loads(jsonstr))
    name = dic['name']
    info_dic = dict(dic['detail'])
    data_service.add_submission(name, info_dic)
    return jsonify('ok')

# 获取所有子任务的信息,包含名字和内容
@app.route('/get_all_submission', methods=['GET'])
def get_all_submission():
    data = data_service.get_all_submission()
    return jsonify(data)

# 获取所有子任务的名字
@app.route('/get_all_submission_name', methods=['GET'])
def get_all_submission_name():
    data = data_service.get_all_submission_name()
    return jsonify(data)

# 根据名字获取子任务的信息, 包含名字和内容, 格式为字典的串
@app.route('/get_submission', methods=['GET'])
def get_submission():
    name = request.args.get('name')
    data = data_service.get_submission(name)
    return jsonify(data)

@app.route('/delete_submission', methods=['GET'])
def delete_submission():
    name = request.args.get('name')
    data_service.delete_submission(name)
    return jsonify('ok')

# 用于添加子任务
@app.route('/add_mission', methods=['POST'])
def add_mission():
    '''
    {
        "name": "mission",
        "detail": {
            "start_time": 1497706154.018272,
            "end_time": 1497702999.018272,
            "submission_list": [
                "submission1",
                "submission2"
            ],
            "resource_dic": {
                "core_reids": "useful_redis",
                "filter_redis": "useful_redis",
                "mongo": "useful_mongo",
                "mysql": "useful_mysql"
            },
            "weight": 0.8,
            "state": "STOP"
        }
    }
    '''
    jsonstr = request.form.get('json_result', '')
    dic = dict(json.loads(jsonstr))
    name = dic['name']
    info_dic = dict(dic['detail'])
    data_service.add_mission(name, info_dic)
    return jsonify('ok')

# 获取所有子任务的信息,包含名字和内容
@app.route('/get_all_mission', methods=['GET'])
def get_all_mission():
    data = data_service.get_all_mission()
    return jsonify(data)

# 获取所有子任务的名字
@app.route('/get_all_mission_name', methods=['GET'])
def get_all_mission_name():
    data = data_service.get_all_mission_name()
    return jsonify(data)

# 根据名字获取子任务的信息, 包含名字和内容, 格式为字典的串
@app.route('/get_mission', methods=['GET'])
def get_mission():
    name = request.args.get('name')
    data = data_service.get_mission(name)
    return jsonify(data)

@app.route('/delete_mission', methods=['GET'])
def delete_mission():
    name = request.args.get('name')
    data_service.delete_mission(name)
    return jsonify('ok')


@app.route('/get_default_submissions_by_target_urls', methods=['GET', 'POST'])
def get_default_submissions_by_target_urls():
    '''
    jsonstr = request.form.get('urls', '')
    urls_array = json.loads(jsonstr)['urls']
    data_service.classifier_urls(urls_array)
    submissions = []
    for spider in
    '''
    return jsonify('ok')

if __name__ == '__main__':
    # 产生包含ip和port的js文件
    text = 'POST_URL_PREFIX = "http://' + settings.APP_HOST + ':' + str(settings.APP_PORT) + '"'
    filename = os.getcwd() + settings.TEMP_PATH + '/static/const.js'
    with open(filename, 'w') as f:
        f.write(text.encode('utf8'))
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=False)
