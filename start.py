# -*- coding:utf-8 -*-
import project
import time

from code.app.houseinfo.schedule import Schedule
from code.app.houseinfo.houseinfo_crawler import CrawlerHouse
from code.api.api_post import send_svchannel

# 引入日志模块
from code.comm.v2log import v2info


cd_crawler = CrawlerHouse()

def on_find_new(house_list):
    content = "新数据: %d 条记录" % len(house_list)
    print(content)

    for l in house_list:
        details = cd_crawler.get_page_details_from_url(l['url'])
        time.sleep(1)
        content += "\n "+l['title']+"|"+details['date']
        # content += "\n "+details['link']
        content += "\n "
    v2info.debug(content)
    if (0 != len(house_list)):
        # send_email(content, "成都房协信息(%s)" % (len(house_list)))
        send_svchannel(content, "成都房协信息(%s)" % (len(house_list)))
    return


def crawler_cd_house_data(pridata):
    v2info.info("[" + time.asctime() + "] 首页刷新中")
    cd_crawler.moving(on_find_new)
    return


def ocr_pictures(files):
    v2info.info("图形转化中")
    return


def analyze_data(data):
    v2info.info("分析数据中")
    return


def push_msg(data):
    v2info.info("发送消息:" + data)
    return


def main():
    # 初始化任务，每1小时触发一次爬虫类，爬虫类去重，获得新的链接
        # 如果发现消息，则调用file.py下载对应的文件，解压到指定目录，并转化成相应的图片
        # 转化图片后，调用Table类，转化成文字信息(是否人工介入)*难点
        # ...统计计算相关信息
        # ...推送相关信息，邮件
    schedule = Schedule()
    schedule.do(pri_data="Crawler", cb=crawler_cd_house_data,
                name="Crawler", interval=10)
    return


#import tkinter
if __name__ == '__main__':
    main()
    #top = tkinter.Tk()
    # 进入消息循环
    #top.mainloop()
