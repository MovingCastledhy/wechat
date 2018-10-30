# -*- coding:utf-8 -*-

from flask import Flask, request, make_response
from flask import current_app, json, abort, redirect, url_for, session, g, Response
import hashlib
import xmltodict
import time
import requests
from template import *

app = Flask(__name__)

APP_ID = 'wx52aca0ee0b6a6769'
APP_SECRET = '3336b036596e817abc9a965bb78fd71a'
WECHAT_TOKEN = "donghaiyan"
OPEN_ID = "oW4bJ1fvxaeGg2Bqhd4-gzaS4EJE"

@app.route('/wx_flask', methods=['GET', 'POST'])
def wechat():
    args = request.args

    signature = args.get('signature')
    timestamp = args.get('timestamp')
    nonce = args.get('nonce')
    echostr = args.get('echostr')

    # 1. 将token、timestamp、nonce三个参数进行字典序排序
    temp = [WECHAT_TOKEN, timestamp, nonce]
    temp.sort()
    # 2. 将三个参数字符串拼接成一个字符串进行sha1加密
    temp = "".join(temp)
    # sig是我们计算出来的签名结果
    sig = hashlib.sha1(temp.encode('utf-8')).hexdigest()

    # 3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if sig == signature:
        # 根据请求方式.返回不同的内容 ,如果是get方式,代表是验证服务器有效性
        # 如果POST方式,代表是微服务器转发给我们的消息
        if request.method == "GET":
            return echostr
        else:

            # """收发消息接口，收到文本原封不动返回"""
            # req_xml = request.data
            # req = xmltodict.parse(req_xml)['xml']
            # if "text" == req.get("MsgType"):
            #     resp = {
            #         "ToUserName": req.get("FromUserName", ""),
            #         "FromUserName": req.get("ToUserName", ""),
            #         "CreateTime": int(time.time()),
            #         "MsgType": "text",
            #         "Content": req.get("Content", "")
            #     }
            # else:
            #     resp = {
            #         "ToUserName": req.get("FromUserName", ""),
            #         "FromUserName": req.get("ToUserName", ""),
            #         "CreateTime": int(time.time()),
            #         "MsgType": "text",
            #         "Content": "费文本"
            #     }
            # resp_xml = xmltodict.unparse({"xml": resp})
            # return resp_xml

            # """模板消息"""
            # access_token = get_token(APP_ID, APP_SECRET)
            access_token = "15_VI6fAvm9ZUbK-zk8rIIybA7nfDqB3qb72OZjgEzu7oYfeCFteLjhZDr5P7AcS742KwI9CcSUEZGWMYBQikrSyxyeDD2UBhFMrnDqZlJpgL1QIIQhUb3boJ8cvVJcITrd3g5nA9WvYXLVmdjbDGDjADAXAX"
            sent_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token
            message = {
                "touser": OPEN_ID,
                "template_id": "D7Mh7UKcUVSDFp9py7ebtrIxM-Z8QBm90j9RiOAs5aQ",
                "url": "www.baidu.com",

                "data": {
                    "first": {
                        "value": "尊敬的客户，您的订单已支付成功",
                        "color": "#173177"
                    },
                    "keyword1": {
                        "value": "2018款背包",
                        "color": "#173177"
                    },
                    "keyword2": {
                        "value": "20180930",
                        "color": "#173177"
                    },
                    "keyword3": {
                        "value": "199元",
                        "color": "#173177"
                    },
                    "keyword4": {
                        "value": "20180930 17:11",
                        "color": "#173177"
                    },
                    "remark": {
                        "value": "感谢您的光临",
                        "color": "#173177"
                    }
                }
            }

            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(sent_url, json.dumps(message), headers=headers)
            print(response)




    # else:
    #     return 'errno', 403

if __name__ == '__main__':
    app.run()