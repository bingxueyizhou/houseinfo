# -*- coding:utf-8 -*-

import requests
import json
from config import CONF

SERVER_CHANNEL_URL = "https://sc.ftqq.com/"

def send(title= "", content = None):
    conf = CONF.load_server_channel_cfg()
    if conf["debug"]:
        if content:
            print("debug title: "+title+"\ncontent:\n"+content)
        else:
            print("debug title: " + title + "\ncontent:\nNone")
        return True

    for key in conf["keys"]:
        url = SERVER_CHANNEL_URL+key+".send"
        if content:
            body = ("text="+title+"&desp="+content)
        else:
            body = ("text="+title)
        headers = {'content-type': "application/x-www-form-urlencoded"}

        print(url)
        print(headers)
        print(body)
        #response = requests.post(url, data=json.dumps(body), headers=headers)
        response = requests.post(url, data=body.encode("utf-8"), headers=headers)

        # 返回信息
        ret = json.loads(response.text)
        if ret["errno"] != 0:
            print("send failed. --> code:"+response.status_code+"\tresponse:"+response.text)
    return True



if __name__ == '__main__':
    send("开发debug","测试二下")
