# -*- coding:utf-8 -*-
import werkzeug.routing

"""
routing模块内部有：

- Rule类（用来构造不同的URL模式的对象）
- Map类（存储所有的URL规则）
- BaseConverter的子类(负责定义匹配规则)
- MapAdapter类（负责具体URL匹配的工作）

"""