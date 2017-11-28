# -*- coding:utf-8 -*-
from flask import Flask
from flask_script import Manager


# 创建application
app = Flask(__name__)
# 把Manger管理类和应用实例关联 使其可命令行运行(运行/shell/迁移)
manger = Manager(app)


@app.route('/')
def index():

    return u'测试flask_script的Manger'

if __name__ == '__main__':
    manger.run()
