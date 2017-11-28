# -*- coding:utf-8 -*-
from flask import Flask, request, abort
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):
    # 异常捕捉
    return '页面找不到啦。。。。。 %s' % e


@app.route('/error')
def exceptions():
    # 抛出异常
    abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.224.138')
