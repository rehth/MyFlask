# -*- coding:utf-8 -*-
from flask import Flask, render_template, flash


app = Flask(__name__)

app.secret_key = 'sss'


@app.route('/')
def index():
    a = app.config
    # print a
    my_list = [1, 3, 4, 5, 6, 5, 3]
    my_name = 'ZhangQianJun'
    my_dict = {'name': u'张', 'age': 18}
    context = {
        'my_list': my_list,
        'my_name': my_name,
        'my_dict': my_dict,
        'money': "100000",
        'rule': '{{variable | filter_name(*args)}}'
    }
    return render_template('test_jinja2.html', **context)


# 自定义过滤器方法：app.add_template_filter(name, func)
@app.template_filter('limit')
def do_limit(order, start=0, end=-1):
    return order[start:end]


@app.route('/code')
def code():
    flash('flash test')
    return render_template('test_code.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')