# -*- coding:utf-8 -*-

import requests
import json
from conf.config_loader import CONF

# start 引入日志模块
import sys
import os
APP_PRO_HOME = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(APP_PRO_HOME + ".."))
from code.comm.v2log import v2log
# end  引入日志模块

SERVER_CHANNEL_URL = "https://sc.ftqq.com/"

def send_server_channel(title= "", content = None):
    conf = CONF.load_post_cfg()
    if conf["debug"]:
        if content:
            v2log.info("[svchannel]debug title: " + title + "\ncontent:\n" + content)
        else:
            v2log.info("[svchannel]debug title: " + title + "\ncontent:\nNone")
        return True

    # confirm svchannel protocol.
    sv_conf = None
    for p in conf["protocol"]:
        if p["name"] == "svchannel":
            sv_conf = p
            break
    if sv_conf is None:
        v2log.warn("[svchannel]conf don't exist, can't send: \n" + title)
        return False

    for key in sv_conf["keys"]:
        url = SERVER_CHANNEL_URL+key+".send"
        if content:
            body = ("text="+title+"&desp="+content)
        else:
            body = ("text="+title)
        headers = {'content-type': "application/x-www-form-urlencoded"}

        v2log.info(url)
        v2log.info(headers)
        v2log.info(body)
        #response = requests.post(url, data=json.dumps(body), headers=headers)
        response = requests.post(url, data=body.encode("utf-8"), headers=headers)

        # 返回信息
        ret = json.loads(response.text)
        if ret["errno"] != 0:
            v2log.warn("send failed. --> code:" + response.status_code + "\tresponse:" + response.text)
    return True



if __name__ == '__main__':
    send_server_channel("开发debug","测试二下")
