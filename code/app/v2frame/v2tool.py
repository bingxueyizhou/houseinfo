## frame part:app init first
## init example
# import code.app.a.app_project as app_a
# def app_init:
#     app_a.app_init(sys_path+"a")
# app_init()
from code.app.v2frame.v2tool_cmd_cell import ToolCMDCell
import code.app.v2frame.app_project as app_v2frame
import code.app.houseinfo.app_project as app_houseinfo


def app_init():
    app_v2frame.app_init()
    sys_path = app_v2frame.get_app_path()
    app_houseinfo.app_init(sys_path + "/houseinfo")
    # more app...


app_init()

## tools import example:
# from package.a import A
# def tool_a:
#     do_something():
#
# cmd_array = [ToolCMDCell("cmd_a", tool_a, ["cmd description"]),]
from code.app.houseinfo.houseinfo_db import HouseInfoDB


def houseinfo_show_db(argv):
    db = HouseInfoDB(app_houseinfo.get_app_data_path())
    ret = db.query_all_house_info()
    for cell in ret:
        print(cell)


cmd_array = [
    # ToolCMDCell( cmd, function, [help1, help2, ...], )
    ToolCMDCell("houseinfo_show_db", houseinfo_show_db, ["houseinfo_show_db   # to show all houseinfo data in db."]),
]


def handle_tool_cmd(cmd, argv):
    for c in cmd_array:
        if c.get_cmd() == cmd:
            c.func(argv)
            return True

    return False
