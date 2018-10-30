# -*- coding:utf-8 -*-

from flask import Flask, request, make_response
from flask import current_app, json, abort, redirect, url_for, session, g, Response
import hashlib
import xmltodict
import time
from template import *

app = Flask(__name__)

APP_ID = 'wx52aca0ee0b6a6769'
APP_SECRET = '3336b036596e817abc9a965bb78fd71a'
WECHAT_TOKEN = "donghaiyan"


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

        """模板消息"""
        access_token = get_token(APP_ID,APP_SECRET)
        current_app.logger.info(access_token)
        sent_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token
        message = {
            "touser": 'oW4bJ1fvxaeGg2Bqhd4-gzaS4EJE',
            "template_id": "ngqIpbwh8bUfcSsECmogfXcV14J0tQlEpBO27izEYtY",
            "url": "http://weixin.qq.com/download",
            "topcolor": "#FF0000",

            "data": {

                "User": {

                    "value": "黄先生",

                    "color": "#173177"

                },

                "Date": {

                    "value": "06月07日 19时24分",

                    "color": "#173177"

                },

                "CardNumber": {

                    "value": "0426",

                    "color": "#173177"

                },

                "Type": {

                    "value": "消费",

                    "color": "#173177"

                },

                "Money": {

                    "value": "人民币260.00元",

                    "color": "#173177"

                },

                "DeadTime": {

                    "value": "06月07日19时24分",

                    "color": "#173177"

                },

                "Left": {

                    "value": "6504.09",

                    "color": "#173177"

                }

            }
        }

        # 推送消息
        # if not access_token is None:
            # conn = httplib.HTTPConnection("api.weixin.qq.com:80")  # 微信接口链接
            # headers = {"Content-type": "application/json"}  # application/x-www-form-urlencoded
            # params = ({'touser': "oEGZ4johnKOtayJbnEVeuaZr6zQ0",  # 用户openid
            #            'template_id': 'AtFuydv8k_15UGZuFntaBzJRCsHCkjNm1dcWD3A-11Y',  # 模板消息ID
            #            'url': 'http://www.710.so',  # 跳转链接
            #            "topcolor": "#667F00",  # 颜色
            #            "data": {  # 模板内容
            #                "first": {"value": "尊敬的710.so : 您的网站http://www.710.so (192.168.1.1) 有异常访问",
            #                          "color": "#173177"},
            #                "keyword1": {"value": "访问时间 2015-04-05 15:30:59 访问IP 192.168.1.2", "color": "#173177"},
            #                "keyword2": {"value": "访问链接 http://www.710.so", "color": "#173177"},
            #                "remark": {"value": "访问频率 10/s", "color": "#173177"}
            #            }
            #            }
            #           )
            # conn.request("POST", "/cgi-bin/message/template/send?access_token=" + access_token,
            #              json.JSONEncoder().encode(params), headers)  # 推送消息请求
            # response = conn.getresponse()
            # data = response.read()  # 推送返回数据
            # if response.status == 200:
            #     print
            #     'success'
            #     print
            #     data
            # else:
            #     print
            #     'fail'
            # conn.close()

            headers = {
                'Content-Type': 'application/json',
                'encoding': 'utf-8',
            }
            response = requests.post(sent_url, json.dumps(message), headers=headers)
            print(response)




    else:
        return 'errno', 403

if __name__ == '__main__':
    app.run()