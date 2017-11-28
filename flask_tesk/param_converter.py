# -*- coding:utf-8 -*-
from flask import Flask, redirect, url_for
from werkzeug.routing import BaseConverter
# 设置默认编码格式为utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


# 自定义转换器类
class MyConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(MyConverter, self).__init__(url_map)
        self.regex = args[0]

    # 匹配完成后，会将匹配结果传入函数做最后处理
    def to_python(self, value):
        # print type(value)  <type 'unicode'>
        value = value.encode("utf-8")
        # print type(value)
        return value

    # 问题？？？
    def to_url(self, value):
        print value
        return value

# 将自定义转换器类添加到转换器字典中
app.url_map.converters['re'] = MyConverter


# int：是一种flask中的转换器Converter，BaseConverter一个有6种
# fixed_digits:The default is variable length.
@app.route('/param/<int(fixed_digits=4):value>')
def param(value):
    print app.url_map
    return '参数测试： value=%s' % value


# 使用自定义converter完成使用正则来匹配路由
@app.route('/con/<re("\w{2}"):value>')
def my_re_converter(value):
    return '自定义转换器测试 value=%s' % value
    # return redirect(url_for('param', value=1111))


if __name__ == '__main__':
    # print app.url_map

    # print sys.getdefaultencoding()
    app.run(debug=True, host='192.168.224.138')
