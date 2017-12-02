# -*- coding:utf-8 -*-
import unittest
from wtf_sql import app, db, Author
# from flask_unit_test import app
# import json


# class MyFlaskUnitTest(unittest.TestCase):
#     """定义一个登陆单元测试类"""
#     def setUp(self):
#         # 该方法会首先执行，用于做测试前的准备工作，方法名为固定写法
#         self.client = app.test_client()
#
#     def tearDown(self):
#         # 该方法会在测试代码执行完后执行，用于做测试后的扫尾工作，方法名为固定写法
#         pass
#
#     def test_login_empty(self):
#         # 以test_开头的函数就是具体的测试代码 必须以test开头
#         response = self.client.post('/', data={})
#         # 接受返回数据/json
#         response_data = response.data
#         # 转换json-->dict
#         response_dict = json.loads(response_data)
#         # 断言是否有消息
#         self.assertIn('code', response_dict, '未接受到消息')
#         # 断言code == -2
#         self.assertEqual(-2, response_dict['code'], 'code错误')
#
#         # 测试username/password有一个为空的情况
#         response = self.client.post('/', data={'username': 'pass'})
#         # 接受返回数据/json
#         response_data = response.data
#         # 转换json-->dict
#         response_dict = json.loads(response_data)
#         # 断言是否有消息
#         self.assertIn('code', response_dict, '未接受到消息')
#         # 断言code == -2
#         self.assertEqual(-2, response_dict['code'], 'code错误')
#
#         response = self.client.post('/', data={'password': 'pass'})
#         # 接受返回数据/json
#         response_data = response.data
#         # 转换json-->dict
#         response_dict = json.loads(response_data)
#         # 断言是否有消息
#         self.assertIn('code', response_dict, '未接受到消息')
#         # 断言code == -2
#         self.assertEqual(-2, response_dict['code'], 'code错误')
#
#     def test_login_error(self):
#         # 用户名/密码错误的情况
#         response = self.client.post('/', data={'username': 'pass', 'password': '34'})
#         # 接受返回数据/json
#         response_data = response.data
#         # 转换json-->dict
#         response_dict = json.loads(response_data)
#         # 断言是否有消息
#         self.assertIn('code', response_dict, '未接受到消息')
#         # 断言code == -1
#         self.assertEqual(-1, response_dict['code'], 'code错误')
#
#         response = self.client.post('/', data={'username': 'pass', 'password': '1234'})
#         # 接受返回数据/json
#         response_data = response.data
#         # 转换json-->dict
#         response_dict = json.loads(response_data)
#         # 断言是否有消息
#         self.assertIn('code', response_dict, '未接受到消息')
#         # 断言code == -1
#         self.assertEqual(-1, response_dict['code'], 'code错误')
#
#         response = self.client.post('/', data={'username': 'python', 'password': '34'})
#         # 接受返回数据/json
#         response_data = response.data
#         # 转换json-->dict
#         response_dict = json.loads(response_data)
#         # 断言是否有消息
#         self.assertIn('code', response_dict, '未接受到消息')
#         # 断言code == -1
#         self.assertEqual(-1, response_dict['code'], 'code错误')
#
#     def test_login_pass(self):
#         response = self.client.post('/', data={'username': 'python', 'password': '1234'})
#         # 接受返回数据/json
#         response_data = response.data
#         # 转换json-->dict
#         response_dict = json.loads(response_data)
#         # 断言是否有消息
#         self.assertIn('code', response_dict, '未接受到消息')
#         # 断言code == -1
#         self.assertEqual(0, response_dict['code'], 'code错误')
#

class MyFlaskDBTest(unittest.TestCase):
    """定义一个数据库单元测试类"""
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/unit_test'
        db.create_all()

    def tearDown(self):
        # 关闭数据库连接
        db.session.remove()
        # 删除所有表
        db.drop_all()

    def test_author_add(self):
        author = Author(name='zzz')
        db.session.add(author)
        db.session.commit()

        author = Author.query.filter_by(name='zzz').first()
        self.assertIsNotNone(author, '数据添加失败')
        self.assertEqual(author.name, u'zzz', '添加错误')


