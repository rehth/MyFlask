# -*- coding:utf-8 -*-
from flask import Blueprint

# 创建一个蓝图对象,指定静态文件夹,注册模版过滤器
# 蓝图就是类似于一个小模块，可能有自己的静态文件夹和模板文件夹，默认没有像Flask初始化时候帮我们指定
# 注意点：如果主目录中的模板文件夹有与当前模块下的模板文件相同的话，那么优先会使用主目录下的
bp_list = Blueprint('bp_list', __name__,
                    static_folder='static',
                    template_folder='templates',
                    static_url_path='/sys')

from blueprint_list import *
