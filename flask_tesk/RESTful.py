# -*- coding:utf-8 -*-
"""
REST ful API 设计
    域名：尽量将API部署在专用域名之下或放在主域名下（https://api.example.com）
    版本：应该将API的版本号放入URL中（https://api.example.com/v1/）
    路径：路径表示API的具体网址。每个网址代表一种资源。 资源作为网址，网址中不能有动词只能有名词，一般名词要与数据库的表名对应。而且名词要使用复数。
        （https://api.example.com/v1/zoos）
    标准HTTP方法：对于资源的具体操作类型，由HTTP动词表示。常用的有：
        GET     SELECT ：从服务器获取资源。
        POST    CREATE ：在服务器新建资源。
        PUT     UPDATE ：在服务器更新资源。
        DELETE  DELETE ：从服务器删除资源。
    过滤信息：如果资源数据较多，服务器不能将所有数据一次全部返回给客户端。API应该提供参数，过滤返回结果。
        （http://www.example.com/goods?page=2&per_page=20）
    状态码：服务器向用户返回的状态码和提示信息，常用的有：
        200 OK  ：服务器成功返回用户请求的数据
        201 CREATED ：用户新建或修改数据成功。
        202 Accepted：表示请求已进入后台排队。
        400 INVALID REQUEST ：用户发出的请求有错误。
        401 Unauthorized ：用户没有权限。
        403 Forbidden ：访问被禁止。
        404 NOT FOUND ：请求针对的是不存在的记录。
        406 Not Acceptable ：用户请求的的格式不正确。
        500 INTERNAL SERVER ERROR ：服务器发生错误。
    错误处理：一般来说，服务器返回的错误信息，以键值对的形式返回。
        {
            error: 'Invalid API KEY'
        }
    响应结果：针对不同操作，服务器向用户返回的结果应该符合相应的规范
    使用链接关联相关的资源：返回响应结果时提供链接其他API的方法，使客户端很方便的获取相关联的信息。
    其他：服务器返回的数据格式，应该尽量使用JSON，避免使用XML。

"""