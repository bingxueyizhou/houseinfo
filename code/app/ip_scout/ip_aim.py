import re
import requests


import code.app.ip_scout.app_project as app_project

v2log = None


class IPAim:
    __url = ""
    __parse = None

    def request_web(url):
        try:
            response = requests.get(url, headers={'Connection': 'close'})
            if response == None: return None
            return response.text
        except Exception as e:
            v2log.warning(e)
            v2log.warning("network error.")
        return None

    def __default_parse(url):
        html = IPAim.request_web(url)

        if html is None:
            return None

        ip = re.findall(u"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", html)
        if len(ip) <= 0:
            return None
        return ip[0]

    def __init__(self, url, parse=__default_parse):
        self.__url = url
        self.__parse = parse

        global v2log
        v2log = app_project.get_logger()

    def get_ip(self):
        return self.__parse(self.__url)

    def get_url(self):
        return self.__url

