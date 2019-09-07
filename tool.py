# -*- coding:utf-8 -*-
import sys

## app
import code.app.v2frame.app_project as app_v2frame
import code.app.houseinfo.app_project as app_houseinfo


def app_init():
    app_v2frame.app_init()
    sys_path = app_v2frame.get_app_path()
    app_houseinfo.app_init(sys_path + "/houseinfo")


app_init()

# tools modules
# tools functions
# module handle what
from code.app.houseinfo.houseinfo_db import HouseInfoDB


def houseinfo_show_db():
    db = HouseInfoDB(app_houseinfo.get_app_data_path())
    ret = db.query_all_house_info()
    for cell in ret:
        print(cell)


def handle_one_cmd(cmd):
    if cmd == "houseinfo_show_db":
        houseinfo_show_db()


def main():
    if len(sys.argv) == 2:
        handle_one_cmd(sys.argv[1])


if __name__ == '__main__':
    main()
