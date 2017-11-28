# -*- coding:utf-8 -*-
from flask import Flask, redirect, json, jsonify, current_app, url_for


# Flask函数接收一个参数name，它会指向程序所在的模块
"""
import_name: 模块名
static_url_path: 静态文件访问前缀
static_folder: 默认‘static’
template_folder: 默认‘templates’
"""
app = Flask(__name__, static_folder='static', template_folder='templates')

# flask配置信息加载的3种常见方式
# app.config['DEBUG'] = True

# app.config.from_pyfile('flask_conf.py')


class MyConf(object):
    DEBUG = True
    PYTHON = 'TRUE'
app.config.from_object(MyConf)


# 装饰器的作用是将路由映射到视图函数index
# 使用 methods 参数指定可接受的请求方式 默认(HEAD, OPTIONS, GET)
@app.route('/', methods=['get'])
def index():
    print app.url_map
    # 取出配置信息 app.config.get(key) 2种
    print app.config.get('PYTHON')
    # current_app 指当前对象所属的app
    print current_app.config.get('PYTHON')
    # Flask调用视图函数后，可以返回内容有：字符串或HTML模版
    return 'hello word!'


@app.route('/')
def index2():
    # 同一路由指向两个不同的函数，在匹配过程中，至上而下依次匹配
    return 'index2'


@app.route('/baidu')
def baidu():
    # 重定向redirect示例 'https://www.baidu.com'
    print url_for('index2')
    return redirect(url_for('p', value=1200))


@app.route('/p/<value>')
def p(value):
    return u'测试redirect/url_for value=%s' % value


@app.route('/json')
def js():
    # 返回json数据
    json_data = {'name': 'zhang', 'age': 18}
    # 该方式返回的不是标准的json数据
    # return json.dumps(json_data)
    # jsonfy可以返回标准的json数据
    # ACSII 排序
    return jsonify(json_data)

if __name__ == '__main__':
    # Flask应用程序实例的run方法启动WEB服务器

    app.run(host='192.168.224.138')
