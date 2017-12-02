# -*- coding:utf-8 -*-
from flask import Flask, render_template
from flask_mail import Mail, Message
from threading import Thread   # 线程

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
# 配置邮件：服务器／端口／安全套接字层／邮箱名／授权码
app.config['MAIL_SERVER'] = "smtp.163.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'zhangqianjuns@163.com'
app.config['MAIL_PASSWORD'] = "qwer1234"
app.config['MAIL_DEFAULT_SENDER'] = 'FlaskAdmin<zhangqianjuns@163.com>'

# 关联应用 初始化邮件对象
mail = Mail(app)


@app.route('/')
def index():
    return render_template('flask_send_email.html')


@app.route('/mail')
def send_mail():
    msg = Message(subject='邮件主题', recipients=['zhangqianjuns@163.com'])
    msg.body = 'msg的body'
    msg.html = '<h1>哈哈哈哈哈哈</h1>'
    t = Thread(target=asyn_send_email, args=(msg, ))
    t.start()
    return '发送成功'


def asyn_send_email(msg):
    try:
        with app.app_context():
            mail.send(msg)
    except Exception as e:
        print e
        return '发送失败'

if __name__ == '__main__':
    app.run(debug=True)
