# -*- coding:utf-8 -*-

from flask import Flask, make_response, session, request

app = Flask(__name__)
# 设置密匙
app.secret_key = 'aaa'


@app.route('/')
def index():
    # cookie的设置及取值
    name = request.cookies.get('name')
    response = make_response('set_cookie: name= %s ' % name, 200)
    # response.headers['X-Parachutes'] = 'parachutes are cool'
    # set_cookie(self, key, value='', max_age=None, expires=None,
    #                path='/', domain=None, secure=False, httponly=False)
    response.set_cookie('name', 'zhang', max_age=3600)
    return response


@app.route('/session')
def demo():
    # 设置session及取值 前提是： 设置了密匙secret_key
    # 类似一个字典 若value的类型为列表等，具有相应的属性
    age = session.get('age')
    session.modified = True
    return 'set session age=%s' % age


if __name__ == '__main__':
    app.run(debug=True, host='192.168.224.138')
