# -*- coding:utf-8 -*-
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)


@app.route('/')
def index():

    return '<a href="#">发送邮件</a>'


@app.route('/mail')
def send_mail():
    msg = Message(subject='邮件主题', recipients=['zhangqianjuns@163.com'])
    msg.body = '邮件的body'
    msg.html = '<h1>哈哈哈哈哈哈</h1>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')