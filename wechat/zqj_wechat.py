# -*- coding:utf-8 -*-
from flask import Flask, request
from hashlib import sha1
import xmltodict
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

wechat_token = 'zhangqianjun'


@app.route('/')
def index():
    return 'index'


@app.route('/wechat8029', methods=['get', 'post'])
def chat():
    # 接受数据
    """
    将token、timestamp、nonce三个参数进行字典序排序
    将三个参数字符串拼接成一个字符串进行sha1加密
    """
    # 实现微信的接入 验证
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    signature = request.args.get('signature')
    echostr = request.args.get('echostr')
    # 排序
    temp = sorted([wechat_token, timestamp, nonce])
    # hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
    temp = ''.join(temp)
    temp = sha1(temp).hexdigest()
    # 验证
    if temp == signature:
        # 处理GET请求
        if request.method == 'GET':
            return echostr

        # 验证通过后 若不是GET请求则接受并处理数据
        xml_data = request.data
        xml_dict = xmltodict.parse(xml_data)['xml']
        to_username = xml_dict['FromUserName']
        from_username = xml_dict['ToUserName']
        msg_type = xml_dict['MsgType']

        # 构建返回数据模板
        res = {
            'ToUserName': to_username,
            'FromUserName': from_username,
            'CreateTime': int(time.time()),
            'MsgType': msg_type
        }
        # 处理POST请求
        if request.method == 'POST':
            """鹦鹉学舌"""
            # 处理文本消息
            if msg_type == 'text':
                res['Content'] = xml_dict['Content']

            elif msg_type == 'image':
                # 自助回复图片失败 MediaId是通过素材管理接口上传多媒体文件得到的。
                # 所以用原始的id是不可取的 失败
                res['MediaId'] = xml_dict['MediaId']

            elif msg_type == 'voice':
                # 接受语音并文字返回
                res['MsgType'] = 'text',
                res['Content'] = xml_dict['Recognition']

            # 处理事件：subscribe(订阅)、unsubscribe(取消订阅)
            elif msg_type == 'event':
                if xml_dict['Event'] == 'subscribe':
                    res['MsgType'] = 'text',
                    res['Content'] = '感谢你的关注'
                elif xml_dict['Event'] == 'subscribe':
                    return None

            else:
                print msg_type
                res['MsgType'] = 'text',
                res['Content'] = '暂未解析信息'

        else:
            # 处理其他HTTP请求方式
            res['MsgType'] = 'text',
            res['Content'] = '暂未解析信息'

        res = {'xml': res}
        return xmltodict.unparse(res)
    else:
        return None

if __name__ == '__main__':
    # Flask应用程序实例的run方法启动WEB服务器
    app.run(port=8029)
