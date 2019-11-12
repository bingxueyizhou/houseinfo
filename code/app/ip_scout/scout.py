import os
import re
import random

import code.app.ip_scout.app_project as app_project
from code.app.ip_scout.ip_aim import IPAim
from code.app.ip_scout.ip_db import IPDB


## some ip function
# http://m.ip138.com/
def get_ip138_ip(url):
    html = IPAim.request_web(url)
    if html is None: return None
    ip = re.findall(u"\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\]", html)
    if len(ip) <= 0: return None
    return ip[0][1:-1]


# http://ip.chinaz.com/
def get_chinaz_ip(url):
    html = IPAim.request_web(url)
    if html == None: return None

    re_stage_1 = re.findall(u"<dd.*>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}</dd>", html)
    if len(re_stage_1) <= 0: return None

    ip = re.findall(u"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", re_stage_1[0])
    if len(ip) <= 0: return None
    return ip[0]


# http://ip.cn/
def get_ipcn_ip(url):
    html = IPAim.request_web(url)
    if html is None: return None

    re_stage_1 = re.findall(u"</span>: [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}</span>", html)
    print()
    if len(re_stage_1) <= 0: return None

    ip = re.findall(u"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", re_stage_1[0])
    if len(ip) <= 0: return None
    return ip[0]


class Scout:
    IP_SCOUT_HOME = os.path.dirname( os.path.realpath(__file__) )
    __ip_aim = None
    __ip_db = None
    IP_LIST = []

    def __init__(self, path=None):
        if path is not None:
            self.IP_SCOUT_HOME = path
        app_project.app_init(self.IP_SCOUT_HOME)

        global v2log
        v2log = app_project.get_logger()

        self.__ip_db = IPDB(self.IP_SCOUT_HOME+"/user_data")

        ## ip list must init after app_init
        self.IP_LIST = [
            IPAim("http://2000019.ip138.com/", get_ip138_ip),
            IPAim("http://ip.chinaz.com/", get_chinaz_ip),
            IPAim("http://ip.cn/", get_ipcn_ip),
            IPAim("http://members.3322.org/dyndns/getip")
        ]

    @staticmethod
    def is_ip(ip):
        if ip is None:
            return False
        test = re.findall(u"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip)
        if len(test) <= 0: return False
        return True

    def __ip_handle_tail(self, cb=None, ret_list=[]):
        if cb is not None:
            if len(ret_list) == 0:
                cb(ret_list)
                return

            # get first cell in list
            ip_in_process = ret_list[0]

            # get first cell in db
            ip_in_db = self.__ip_db.query_last_record()
            if (ip_in_db is not None) and (ip_in_db['ip'] == ip_in_process):
                v2log.info("ip %s never change."%(ip_in_process))
                cb([])
                return

            self.__ip_db.add_ip_record(ip_in_process)
            cb(ret_list)
        return


    # ["ip"]
    def handle(self, callback=None, rand=False):
        ret_list = []
        if rand:
            test_id = (random.randint(0, len(self.IP_LIST)-1))
            ado = self.IP_LIST[test_id]
            ip = ado.get_ip()
            if Scout.is_ip(ip):
                v2log.info("parse %s success. ip is %s"%(ado.get_url(), ip))
                ret_list.append(ip)
            else:
                v2log.warning("parse %s fail."%(ado.get_url()))

            self.__ip_handle_tail(callback, ret_list)
            return

        for ado in self.IP_LIST:
            ip = ado.get_ip()
            if Scout.is_ip(ip):
                v2log.info("parse %s success. ip is %s"%(ado.get_url(), ip))
                ret_list.append(ip)
            else:
                v2log.warning("parse %s fail."%(ado.get_url()))

        self.__ip_handle_tail(callback, ret_list)
