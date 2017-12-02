# -*- coding:utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['post'])
def index():
    # 获取数据request
    username = request.form.get('username')
    password = request.form.get('password')
    # 验证数据完整性
    if not all([username, password]):
        result = {
            'code': -2,
            'msg': u'数据不完整'
        }
        return jsonify(result)
    # 数据检验-登陆判断
    if username == 'python' and password == '1234':
        result = {
            'code': 0,
            'msg': u'登陆成功'
        }
        return jsonify(result)
    else:
        result = {
            'code': -1,
            'msg': u'用户名或密码错误'
        }
        return jsonify(result)

if __name__ == '__main__':
    # Flask应用程序实例的run方法启动WEB服务器
    app.run(debug=True)