
# -*- coding:utf-8 -*-
import time

from code.app.houseinfo.houseinfo_crawler import CrawlerHouse
from code.app.post.server_channel import send_server_channel as send_svchannel

# 引入日志模块
import code.app.v2frame.app_project as v2frame
import code.app.houseinfo.app_project as app_houseinfo

v2log = v2frame.get_logger()

cd_crawler = CrawlerHouse(app_houseinfo.get_app_data_path())

def on_find_new(house_list):
    content = "新数据: %d 条记录" % len(house_list)
    v2log.info(content)

    for l in house_list:
        details = cd_crawler.get_page_details_from_url(l['url'])
        time.sleep(1)
        content += "\n "+l['title']+"|"+details['date']
        # content += "\n "+details['link']
        content += "\n "
    v2log.debug(content)
    if (0 != len(house_list)):
        # send_email(content, "成都房协信息(%s)" % (len(house_list)))
        send_svchannel("成都房协信息(%s)" % (len(house_list)), content)
    return


def crawler_cd_house_data():
    v2log.info("[" + time.asctime() + "] 首页刷新中")
    cd_crawler.moving(on_find_new)
    return


def ocr_pictures(files):
    v2log.info("图形转化中")
    return


def analyze_data(data):
    v2log.info("分析数据中")
    return


def push_msg(data):
    v2log.info("发送消息:" + data)
    return


def run(pridata):
    # 初始化任务，每1小时触发一次爬虫类，爬虫类去重，获得新的链接
        # 如果发现消息，则调用file.py下载对应的文件，解压到指定目录，并转化成相应的图片
        # 转化图片后，调用Table类，转化成文字信息(是否人工介入)*难点
        # ...统计计算相关信息
        # ...推送相关信息，邮件
    crawler_cd_house_data()
    return