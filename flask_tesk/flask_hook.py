# -*- coding:utf-8 -*-
from flask import Flask, request

app = Flask(__name__)


# 在处理第一个请求前运行
@app.before_first_request
def before_first_request():
    print app.url_map


# 在每次请求前运行
@app.before_request
def before_request():
    print request.url
"""
    在每个请求之前，执行 before_request() 上绑定的函数。
 如果这些函数中的某个返回了一个响应，其它的函数将不再被调用。
 任何情况 下，无论如何这个返回值都会替换视图的返回值
"""


# 如果没有未处理的异常抛出，在每次请求后运行
@app.after_request
def after_request(response):
    print 'success'
    return response
"""
    视图的返回值之后会被转换成一个实际的响应对象
并交给 after_request() 上绑定的函数适当地替换或修改它
"""


@app.teardown_request
def teardown_request(exception):
    print u'发现异常：%s' % exception
"""
    在请求的最后，会执行 teardown_request() 上绑定的函 数。
这总会发生，即使在一个未处理的异常抛出后或是没有请求前处理器执行过
（例如在测试环境中你有时会想不执行请求前回调）
"""


@app.route('/')
def index():
    # try:
    #     print 1/0
    # except ZeroDivisionError as e:
    #     print e
    return 'index', 666

if __name__ == '__main__':
    app.run(debug=True, host='192.168.224.138')