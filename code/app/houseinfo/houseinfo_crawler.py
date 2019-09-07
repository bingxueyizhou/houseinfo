# -*- coding:utf-8 -*-
import requests
import time
import re
import os

import code.app.houseinfo.app_project as app_project
from code.app.houseinfo.houseinfo_db import HouseInfoDB
v2log = None

# print sys.getdefaultencoding()
app_conf = dict()
app_conf['debug'] = True

# 主要的URL
HOUSE_URL = 'https://www.cdfangxie.com/Infor/type/typeid/36.html'
#<span class="sp_name"><a title="新都区|东湖郡（5月8日开始登记）" target="_blank" href="/Infor/index/id/4199.html">新都区|东湖郡（5月8日开始登记）</a></span>
# 刷新时间
REFRESH_TIME = 5

class HouseCell(dict):
    def __init__(self, span=None):
        if None != span:
            self.span_to_elment(span)

    def reset_all_element(self, hsid, title, zone, name, url, extra=""):
        self.title = title
        self.zone  = zone
        self.name  = name
        self.url   = url
        self.hsid = hsid
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

        # get hsid
        hsid = re.findall(r"[0-9]+\.html", url[0])
        self.hsid = hsid[0][:-5]

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
    CRAWLER_HOUSE_HOME = os.path.dirname( os.path.realpath(__file__) )
    is_debug = True
    db = None

    def __init__(self, path=None):
        self.home = HOUSE_URL
        self.time = REFRESH_TIME * 59 # 秒 -> 分鍾
        self.response = None
        self.current_json = dict()
        self.header = {'Connection': 'close'}

        if path is not None:
            self.CRAWLER_HOUSE_HOME = path
        self.datadir  = self.CRAWLER_HOUSE_HOME + '/data/crawler'
        self.init_datadir()
        self.init_db()

        global v2log
        v2log = app_project.get_logger()


    # file operation
    def init_datadir(self):
        if not os.path.isdir(self.datadir):
            os.makedirs(self.datadir)

    # db operation
    def init_db(self):
        if self.db is None:
            self.db = HouseInfoDB(path=self.CRAWLER_HOUSE_HOME)

    def save_ori_html(self, response, filename=CRAWLER_HOUSE_HOME+'/crawler/debug.html'):
        if not self.is_debug : return
        if response == None  : return

        with open(filename, 'w') as file:
            file.write(str(response.text.encode("utf-8")))

    def update_db(self):
        return

    # logic process
    def moving(self, on_new=None):
        self.init_db()
        diff_list = []
        # get info and translate to list
        response = self.request_web(self.home)
        home_list = self.home_page_to_list(response)

        # DB process
        v2log.info("web get: %s"%home_list)
        for info in home_list:
            # step 1: check if it exists in db. if in, skip.
            query_ret = self.db.query_house_info(info["hsid"])
            if query_ret is not None:
                continue

            # step 2: if not, add it. And keep different data in array .
            self.db.add_house_info(info["hsid"], info["title"], info["zone"], info["name"], info["extra"], info["url"])
            diff_list.append(info)

        for info in diff_list:
            # step 3: loop difference array to parse details.
            details = self.get_page_details_from_url(info["url"])
            if details is None:
                continue

            v2log.info("update house id=%s, details=%s" % (info["hsid"], query_ret))
            # step 4: save details to db.
            self.db.add_house_details(info["hsid"], details["date"], details["area"])
            time.sleep(2)

        # step 5: callback
        if on_new is not None:
            on_new(diff_list)

        self.db.close()

    def request_web(self, url):
        response = None
        try:
            return requests.get(url, headers = self.header)
        except Exception as e:
            response = None
            v2log.warn(e)
            v2log.warn("network error.")
        return response

    def __list_diff(self, old, new):
        result = []
        flag = False
        for a in new:
            for b in old:
                if a['title'] == b['title']: flag = True
            if not flag: result.append(a)
            flag = False
        return result

    def home_page_to_list(self, homepage):
        __list = []
        if homepage is None:
            return __list
        cell_list = re.findall(r"<span class=\"sp_name\">.*?</span>", homepage.text)
        for span in cell_list:
            cell = HouseCell(span)
            __list.append(cell)
        return __list

    def get_page_details_from_url(self, url):
        file_link = None
        response = self.request_web(url)
        if response is None:
            return None
        date = re.findall(u"(?:<span>上市时间</span>:)([0-9]{4}-[0-9]{2}-[0-9]{2})(?:</span>)", response.text)
        if len(date) == 0:
            return None

        area = re.findall(u"(?:<span>\):)([0-9\.]+)(?:</span>)", response.text)
        if len(area) == 0:
            return None
        return {"date":date[0], "area":area[0]}

if __name__ == '__main__' :
    house = CrawlerHouse()
    # print(house.get_page_details_from_url("https://www.cdfangxie.com/Infor/index/id/4989.html"))
    house.moving()
