# -*- coding:utf-8 -*-
from flask import Flask
from bp_list import bp_list

app = Flask(__name__)

# 注册蓝图 添加一个url前缀：/list
app.register_blueprint(bp_list, url_prefix='/list')


@app.route('/')
def index():
    return 'index'


@app.route('/detail')
def detail():
    return 'my detail page'

if __name__ == '__main__':
    # Flask应用程序实例的run方法启动WEB服务器
    print app.url_map
    app.run(debug=True)
