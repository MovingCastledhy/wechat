#! /usr/bin/env python
# coding: utf-8

import sys
import requests
import json

# from datastore.mongo import dm


def get_token(app_id, app_secret):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(app_id, app_secret)
    result = requests.get(url)
    access_token = json.loads(result.content.decode()).get('access_token')
    print(access_token)
    return access_token


def get_formatter_list(formatters, keys):
    try:
        return [formatters[key] for key in keys]
    except (ValueError, KeyError):
        return []


def send_template(platform_name, openids, template_name, url, formatters):
    # send_template('nxzl0', openids, 'out_hospital', url, {'out_date': '2018年9月5日', 'patient_name': '王小瑶'})
    wechat = dm.Wechat.objects(name=platform_name).first()
    if wechat is None:
        return None
    access_token = get_token(wechat.appid, wechat.appsecret)
    sent_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token
    template_map = {
        'service_start': {
            'template_id': 'L3OxnRB-kFZwmwbNhLxDP3IzMpYsHzB5yd7N6KueKnA',
            'url': url,
            'data': {
                'first': {
                    'template': '你签约的全病程管理服务已开通，请您下载App并登录开始享受服务。', 'formatter': [],
                },
                'keyword1': {
                    'template': '{}', 'formatter': ['start_date'],
                },
                'keyword2': {
                    'template': '全病程管理服务', 'formatter': [],
                },
                'keyword3': {
                    'template': '您将获得在线问诊、在线购买药品、医生随访关怀、服药提醒、专家宣教等服务。帮助您提高治疗效率，早日康复。', 'formatter': [],
                },
                'keyword4': {
                    'template': '', 'formatter': [],
                },
                'remark': {
                    'template': '点击详情查看全病程管理服务。', 'formatter': [],
                },
            }
        },
        'out_hospital': {
            'template_id': 'LdMU0AHVcAqw8dkMtgXyJGi2yohwNjirfe5lAuO91dI',
            'url': url,
            'data': {
                'first': {
                    'template': '为了您能在出院后更快的康复，我们为您开启了院后的全病程管理服务。', 'formatter': [],
                },
                'keyword1': {
                    'template': '{}', 'formatter': ['patient_name'],
                },
                'keyword2': {
                    'template': '{}', 'formatter': ['out_date'],
                },
                'keyword3': {
                    'template': '', 'formatter': [],
                },
                'keyword4': {
                    'template': '', 'formatter': [],
                },
                'remark': {
                    'template': '点击详情查看全病程管理服务。', 'formatter': [],
                },
            }
        }
    }

    if template_name not in template_map:
        return
    template = template_map[template_name]
    for o in openids:
        message = {
            "touser": o,
            "template_id": template['template_id'],
            "url": template['url'],
            "data": {
                "first": {
                    "value": template['data']['first']['template'].format(
                        *get_formatter_list(formatters, template['data']['first']['formatter'])),
                    "color": template['data']['first'].get('color') or '#173177'
                },
                "keyword1": {
                    "value": template['data']['keyword1']['template'].format(
                        *get_formatter_list(formatters, template['data']['keyword1']['formatter'])),
                    "color": template['data']['keyword1'].get('color') or '#173177'
                },
                "keyword2": {
                    "value": template['data']['keyword2']['template'].format(
                        *get_formatter_list(formatters, template['data']['keyword2']['formatter'])),
                    "color": template['data']['keyword2'].get('color') or '#173177'
                },
                "keyword3": {
                    "value": template['data']['keyword3']['template'].format(
                        *get_formatter_list(formatters, template['data']['keyword3']['formatter'])),
                    "color": template['data']['keyword3'].get('color') or '#173177'
                },
                "keyword4": {
                    "value": template['data']['keyword4']['template'].format(
                        *get_formatter_list(formatters, template['data']['keyword4']['formatter'])),
                    "color": template['data']['keyword4'].get('color') or '#173177'
                },
                "remark": {
                    "value": template['data']['remark']['template'].format(
                        *get_formatter_list(formatters, template['data']['remark']['formatter'])),
                    "color": template['data']['remark'].get('color') or '#173177'
                }
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'encoding': 'utf-8',
        }
        response = requests.post(sent_url, json.dumps(message), headers=headers)
        print(response)


if __name__ == '__main__':
    openids = [
        'orTkYw__M9vrJ1YIDZW4VGJmoqLs',
        # 'orTkYw-Ba6lXwHWuIHwom-PgAqPI',
        # 'orTkYw2hNk_VioBaAa3LizoGu78I',
        # 'orTkYw47Shlf9vb-mHp7lMCIBqyY',
        # 'orTkYw-2_0Iv3pl02-q7MNN4pblk',
        # 'orTkYwx-g0SIhALcW-Pbxm0w_qwk',
    ]
    url = 'https://www.baidu.com'
    # send_template('nxzl0', openids, 'service_start', url, {'start_date': '2018年9月5日'})
    send_template('nxzl0', openids, 'out_hospital', url, {'out_date': '2018年9月5日', 'patient_name': '王小瑶'})





8888888