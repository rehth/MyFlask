# -*- coding:utf-8 -*-
from flask import Flask, request
from hashlib import sha1

app = Flask(__name__)

wechat_token = 'zhangqianjun'


@app.route('/')
def index():
    return 'index'


@app.route('/wechat8010')
def chat():
    # 接受数据
    """
    将token、timestamp、nonce三个参数进行字典序排序
    将三个参数字符串拼接成一个字符串进行sha1加密
    """
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    signature = request.args.get('signature')
    echostr = request.args.get('echostr')
    # 排序
    temp = [wechat_token, timestamp, nonce].sort()
    # hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
    temp = sha1(temp).hexdigest()
    # 验证
    if temp == signature:
        return echostr
    else:
        return ''


if __name__ == '__main__':
    # Flask应用程序实例的run方法启动WEB服务器
    app.run(port=8010)
