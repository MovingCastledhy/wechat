# -*- coding:utf-8 -*-

from flask import Flask, request, make_response
import hashlib
import xmltodict
import time

app = Flask(__name__)

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
            """收发消息接口"""
            req_xml = request.data
            req = xmltodict.parse(req_xml)['xml']
            if "text" == req.get("MsgType"):
                resp = {
                    "ToUserName": req.get("FromUserName", ""),
                    "FromUserName": req.get("ToUserName", ""),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": req.get("Content", "")
                }
            else:
                resp = {
                    "ToUserName": req.get("FromUserName", ""),
                    "FromUserName": req.get("ToUserName", ""),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "费文本"
                }
            resp_xml = xmltodict.unparse({"xml": resp})
            return resp_xml

            # resp_data = request.data
            # resp_dict = xmltodict.parse(resp_data).get('xml')
            #
            # # 如果是文本消息
            # if 'text' == resp_dict.get('MsgType'):
            #     response = {
            #         "ToUserName": resp_dict.get('FromUserName'),
            #         "FromUserName": resp_dict.get('ToUserName'),
            #         "CreateTime": int(time.time()),
            #         "MsgType": "text",
            #         "Content": resp_dict.get('Content'),
            #     }
            #     print(resp_dict.get('Content'))

            # else:
            #     response = {
            #     "ToUserName": resp_dict.get('FromUserName'),
            #     "FromUserName": resp_dict.get('ToUserName'),
            #     "CreateTime": int(time.time()),
            #     "MsgType": "text",
            #     "Content": u"哈哈哈哈",
            # }
            #
            # return make_response(response)
    else:
        return 'errno', 403

if __name__ == '__main__':
    app.run()