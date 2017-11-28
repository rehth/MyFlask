# -*- coding:utf-8 -*-
from flask import Flask, request
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/request', methods=['post'])
def test_request_property():
    a = request.form.get('password')
    b = request.url
    # c = request.files.get('pic')
    # c.save('./pp.png')
    d = request.data
    print d
    return 'go'


if __name__ == '__main__':
    app.run(debug=True, host='192.168.224.138')

