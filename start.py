# -*- coding:utf-8 -*-
import time

from service.sys.schedule import Schedule
## app
import code.app.v2frame.app_project as app_v2frame
import code.app.post.app_project as app_post
import code.app.houseinfo.app_project as app_houseinfo


def app_init():
    app_v2frame.app_init()
    sys_path = app_v2frame.get_app_path()
    app_post.app_init(sys_path + "/post")
    app_houseinfo.app_init(sys_path + "/houseinfo")

app_init()

## service
from service.proc.houseinfo import run as houseinfo_run




def main():

    # 初始化任务，每1小时触发一次爬虫类，爬虫类去重，获得新的链接
        # 如果发现消息，则调用file.py下载对应的文件，解压到指定目录，并转化成相应的图片
        # 转化图片后，调用Table类，转化成文字信息(是否人工介入)*难点
        # ...统计计算相关信息
        # ...推送相关信息，邮件
    schedule = Schedule()
    schedule.do(pri_data="HouseInfo", cb=houseinfo_run, name="HouseInfo", interval=3600)
    return


#import tkinter
if __name__ == '__main__':
    main()
    #top = tkinter.Tk()
    # 进入消息循环
    #top.mainloop()
