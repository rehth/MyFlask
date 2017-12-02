# -*- coding:utf-8 -*-
from bp_list import bp_list
from flask import render_template


# 在这个蓝图对象上进行操作,注册路由
@bp_list.route('/list')
def g_list():
    return render_template('test_blueprint.html')


