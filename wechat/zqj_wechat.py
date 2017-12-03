# -*- coding:utf-8 -*-
from flask import Flask, request
from hashlib import sha1
import xmltodict
import time
import urllib2
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

wechat_token = 'zhangqianjun'
APPID = 'wxbbcd170c7a248189'
APPSECRET = '20f6ced8039c897e097126839b85e6e7'


class AccessToken(object):
    """定义一个类：获取一个微信的assess_token"""
    __ACCESS_TOKEN = {
        'access_token': None,
        'expires_in': 0,
        'update_time': 0,
    }

    @classmethod
    def get_access_token(cls):
        # 如果存在则返回，不存在或已过期则重新查询在返回
        flag = int(time.time()) - cls.__ACCESS_TOKEN['update_time'] < cls.__ACCESS_TOKEN['expires_in']
        # 若access_token没有值或者已过期 需要重新查询
        if not (cls.__ACCESS_TOKEN['access_token'] or flag):
            """ https请求方式: GET
                https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
            """
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credenti" \
                  "al&appid=%s&secret=%s" % (APPID, APPSECRET)
            # 打开对应网址并读取数据
            response = urllib2.urlopen(url).read()
            # json-->dict
            # {"access_token":"ACCESS_TOKEN","expires_in":7200}/{"errcode":40013,"errmsg":"invalid appid"}
            response_dict = json.loads(response)
            # 如果返回的response正确 则添加到__ACCESS_TOKEN
            if 'access_token' in response_dict:
                cls.__ACCESS_TOKEN['access_token'] = response_dict['access_token']
                cls.__ACCESS_TOKEN['expires_in'] = response_dict['expires_in']
                cls.__ACCESS_TOKEN['update_time'] = int(time.time())
            else:
                return Exception('invalid appID or appSecret')
        # 返回access_token
        return cls.__ACCESS_TOKEN['access_token']


@app.route('/')
def index():
    """
        获取临时二维码ticket
        http请求方式: POST
        URL: https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=TOKEN POST数据格式：json
        POST数据例子：{"expire_seconds": 604800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": 123}}}
    """
    # 获取access_token
    access_token = AccessToken.get_access_token()
    url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % access_token
    data = {'expire_seconds': 259200, 'action_name': 'QR_SCENE', 'action_info': {'scene': {"scene_id": 666}}}
    # 请求并获取json数据
    # dict --> json
    data = json.dumps(data)
    # 请求指定的网址，获取ticket
    response = urllib2.urlopen(url, data).read()
    response_dict = json.loads(response)
    ticket = response_dict['ticket']
    # 返回一个带参数的二维码图片
    return '<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s">' % ticket


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
                res['MsgType'] = 'text'
                res['Content'] = xml_dict['Recognition']

            # 处理事件：subscribe(订阅)、unsubscribe(取消订阅)
            elif msg_type == 'event':
                if xml_dict['Event'] == 'subscribe':
                    res['MsgType'] = 'text'
                    #  扫描带参数二维码 用户未关注时，进行关注后的事件推送
                    # EventKey	事件KEY值，qrscene_为前缀，后面为二维码的参数值 Ticket
                    res['Content'] = '感谢你的关注 %s' % xml_dict['EventKey']
                elif xml_dict['Event'] == 'unsubscribe':
                    return 'success'

            else:
                print msg_type
                res['MsgType'] = 'text'
                res['Content'] = '暂未解析信息'

        else:
            # 处理其他HTTP请求方式
            res['MsgType'] = 'text'
            res['Content'] = '暂未解析信息'

        res = {'xml': res}
        return xmltodict.unparse(res)
    else:
        return '请求失败'

if __name__ == '__main__':
    # Flask应用程序实例的run方法启动WEB服务器
    app.run(port=8029)
