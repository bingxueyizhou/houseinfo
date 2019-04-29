# -*- coding:utf-8 -*-
import requests
import time
import subprocess
import os
import codecs
import sys
import multiprocessing
import signal
import re
import json
from config import CONF

# print sys.getdefaultencoding()

app_conf   = CONF.load_email_cfg()

# 主要的URL
HOUSE_URL = 'https://www.cdfangxie.com/Infor/type/typeid/36.html'
#<span class="sp_name"><a title="新都区|东湖郡（5月8日开始登记）" target="_blank" href="/Infor/index/id/4199.html">新都区|东湖郡（5月8日开始登记）</a></span>
# 刷新时间
REFRESH_TIME = 5

class HouseCell(dict):
    def __init__(self, span=None):
        if None != span:
            self.span_to_elment(span)

    def reset_all_element(self, title, zone, name, url, extra=""):
        self.title = title
        self.zone  = zone
        self.name  = name
        self.url   = url
        self.extra = extra
        return

    def span_to_elment(self, span):
        # get title
        title = re.findall(r"title=\".*?\"", span)
        self.title = str(title[0][7:-1])

        # get zone, name and extra
        skip_1 = self.title.index("|")
        self.zone = self.title[0:skip_1]
        try:
            skip_2 = self.title.rindex("（")
            self.name = self.title[skip_1+1:skip_2]
            self.extra = self.title[skip_2+1:-1]
        except Exception as e:
            self.extra = ""
            self.name = self.title[skip_1+1:]

        # get url
        url = re.findall(r"href=\".*?\"", span)
        self.url = "https://www.cdfangxie.com%s"%str(url[0][6:-1])

    def __getattr__(self, name):
        if name in self:
            return self[name]
        n = HouseCell()
        super(HouseCell, self).__setitem__(name, n)
        return n

    def __getitem__(self, name):
        if name not in self:
            super(HouseCell, self).__setitem__(name,dict())
        return super(HouseCell, self).__getitem__(name)

    def __setattr__(self, name, value):
        super(HouseCell, self).__setitem__(name,value)


class CrawlerHouse(object):
    is_debug = True

    def __init__(self):
        self.home = HOUSE_URL
        self.time = REFRESH_TIME * 59 # 秒 -> 分鍾
        self.response = None
        self.current_json = dict()
        self.header = {'Connection': 'close'}
        self.infolist = []
        self.filedir  = './crawler'
        self.filename = 'data.json'
        self.init_dir()

    # file operation
    def init_dir(self):
        if not os.path.isdir(self.filedir):
            os.makedirs(self.filedir)

    def exist_data_file(self):
        if self.filename in os.listdir(self.filedir):
            return True
        else:
            return False

    def save_json(self):
        with codecs.open(self.filedir + "/" + self.filename, 'w', encoding='utf-8') as json_f:
            data = json.dumps(self.infolist, ensure_ascii=False)
            json_f.write(data)

    def read_json(self):
        self.infolist = []
        try:
            with codecs.open(self.filedir + "/" + self.filename, 'r', encoding='utf-8') as json_f:
                self.current_json = json.loads(json_f.read())
            for span in self.current_json:
                cell = HouseCell()
                cell.reset_all_element(span["title"], span["zone"], span["name"], span["url"], span["extra"])
                self.infolist.append(cell)
        except Exception as e:
            return []
        return self.current_json

    def save_ori_html(self, response, filename='./crawler/debug.html'):
        if not self.is_debug : return
        if response == None  : return

        with open(filename, 'w') as file:
            file.write(str(response.text.encode("utf-8")))

    # logic process
    def moving(self, on_new=None):
        if not self.exist_data_file():
            response      = self.request_web(self.home)
            self.infolist = self.home_page_to_list(response)

            if on_new != None:
                on_new(self.infolist)

            self.save_json()
            self.read_json()
        else:
            _last_list    = self.read_json()
            response      = self.request_web(self.home)
            self.infolist = self.home_page_to_list(response)

            diff = self.__list_diff(_last_list,self.infolist)

            if on_new != None and len(diff) != 0:
                on_new(diff)
            self.save_json()


    def request_web(self, url):
        response = None
        try:
            return requests.get(url, headers = self.header)
        except Exception as e:
            response = None
            print(e)
            print("network error.")
        return response

    def __list_diff(self, old, new):
        result = []
        flag   = False
        for a in new:
            for b in old:
                if a['title'] == b['title']: flag = True
            if not flag: result.append(a)
            flag = False
        return result

    def home_page_to_list(self, homepage):
        __list = []
        if homepage == None:
            return __list
        list = re.findall(r"<span class=\"sp_name\">.*?</span>", homepage.text)
        for span in list:
            cell = HouseCell(span)
            __list.append(cell)
        return __list

    def get_page_details_from_url_version_2018_11_15(self, url):
        file_link = None
        response = self.request_web(url)
        self.save_ori_html(response)
        file_link = re.findall(u"http(?:s)?://.*\.rar",response.text)
        # tmp_str = re.findall(u"href=\".*?\" target=\"_blank\">购房登记规则及房源表点击下载",response.text);
        date      = re.findall(u"(?:<span>上市时间</span>:)([0-9]{4}-[0-9]{2}-[0-9]{2})(?:</span>)", response.text)
        if len(file_link) == 0 or len(date) == 0:
            return {"link":"","date":""}
        return {"link":file_link[0],"date":date[0]}

    def get_page_details_from_url(self, url):
        file_link = None
        response = self.request_web(url)
        if app_conf['debug']:
            self.save_ori_html(response)
        # tmp_str = re.findall(u"href=\".*?\" target=\"_blank\">购房登记规则及房源表点击下载",response.text);
        date      = re.findall(u"(?:<span>上市时间</span>:)([0-9]{4}-[0-9]{2}-[0-9]{2})(?:</span>)", response.text)
        if len(date) == 0:
            return {"date":""}
        return {"date":date[0]}


if __name__ == '__main__':
    house = CrawlerHouse()
    print(house.get_page_details_from_url("https://www.cdfangxie.com/Infor/index/id/4989.html"))
    #house.moving();
