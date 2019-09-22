from code.comm.v2schedule import Schedule
## frame part:app init first
## init example
# import code.app.a.app_project as app_a
# def app_init:
#     app_a.app_init(sys_path+"a")
# app_init()
import code.app.v2frame.app_project as app_v2frame
import code.app.post.app_project as app_post
import code.app.houseinfo.app_project as app_houseinfo
import code.app.ip_scout.app_project as app_ipscout


def app_init():
    app_v2frame.app_init()
    sys_path = app_v2frame.get_app_path()
    app_post.app_init(sys_path + "/post")
    app_houseinfo.app_init(sys_path + "/houseinfo")
    app_ipscout.app_init(sys_path + "/ipscout")
    # more app...


app_init()

## frame part: service init
## init example
# import service.proc.a as run_a
# def app_main_run():
#     schedule = Schedule()
#     schedule.do(pri_data="a", cb=run_a, name="a", interval=3600)
#     return
from code.app.v2frame.service.houseinfo import run as run_houseinfo
from code.app.v2frame.service.ip_scout import run as run_ip_scout


def app_main_run():
    schedule = Schedule()
    schedule.do(pri_data="HouseInfo", cb=run_houseinfo, name="HouseInfo", interval=3600)
    schedule.do(pri_data="ip_scout", cb=run_ip_scout, name="ip_scout", interval=3600*24)
    # more service ...

    return
