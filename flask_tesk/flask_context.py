# -*- coding:utf-8 -*-
# 请求上下文(request context)
# 应用上下文(application context)
# 原因：Flask的设计理念之一就是多应用的支持。当在一个应用的请求上下文环境中，
# 需要嵌套处理另一个应用的相关操作时，“请求上下文”显然就不能很好地解决问题了
# 请求上下文：保存了客户端和服务器交互的数据
# 应用上下文：flask 应用程序运行过程中，保存的一些配置信息
"""
application 指的就是当你调用app = Flask(__name__)创建的这个对象app；
request 指的是每次http请求发生时，WSGI server(比如gunicorn)调用Flask.__call__()之后，在Flask对象内部创建的Request对象；
application 表示用于响应WSGI请求的应用本身，request 表示每次http请求；
application的生命周期大于request，一个application存活期间，可能发生多次http请求，所以，也就会有多个request

"""
"""
在Flask类中，每次请求都会调用这个request_context函数。这个函数则会创建一个_RequestContext对象。
每个_RequestContext对象的创建对应一个Request对象的创建，所以，每个http请求对应一个Request对象

值得注意的是：这个对象在创建时，将Flask实例的本身作为实参传入_RequestContext自身，因此，
self.app = Flask()
这种方式实现了多个request context对应一个application context 的目的
Flask通过_RequestContext将App与Request关联起来
"""

"""
“请求上下文”是一个上下文对象，可以使用with语句构造一个上下文环境。
进入上下文环境时，_request_ctx_stack这个栈(LocalStack栈)中会推入一个_RequestContext对象。
推入栈中的_RequestContext对象有一些属性，包含了请求的的所有相关信息。
    例如app、request、session、g、flashes。还有一个url_adapter，这个对象可以进行URL匹配。
在with语句构造的上下文环境中可以进行请求处理。当退出上下文环境时，_request_ctx_stack这个栈会销毁刚才存储的上下文对象。

保证了请求处理过程不被干扰，而且请求上下文对象保存在LocalStack栈中，也很好地实现了线程/协程的隔离
"""
