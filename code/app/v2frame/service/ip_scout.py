

from code.app.ip_scout.scout import Scout
from code.app.post.server_channel import send_server_channel as send_svchannel

# 引入日志模块
import code.app.v2frame.app_project as v2frame
import code.app.ip_scout.app_project as app_scout

v2log = v2frame.get_logger()
ip_scout_service = None

class IPScoutService:
    __ip_scout = None

    @staticmethod
    def send_ip(list):
        if len(list) == 0:
            v2log.warning("get no ip.")

        send_svchannel("ip地址(%s)" % list[0])

    def __init__(self):
        self.__ip_scout = Scout(app_scout.get_app_data_path())

    def do(self):
        self.__ip_scout.handle(IPScoutService.send_ip, rand=True)


def run(pridata):
    global ip_scout_service
    if ip_scout_service is None:
        ip_scout_service = IPScoutService()
    ip_scout_service.do()