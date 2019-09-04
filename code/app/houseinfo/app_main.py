import sys

import code.app.houseinfo.app_project as houseinfo_project
from code.app.houseinfo.houseinfo_crawler import CrawlerHouse
from code.app.houseinfo.houseinfo_db import HouseInfoDB

def show_db():
    db = HouseInfoDB()
    ret = db.query_all_house_info()
    for cell in ret:
        print(cell)

def main():
    if sys.argv[0] == "show_db":
        show_db()
        return
    house = CrawlerHouse(houseinfo_project.get_app_data_path())
    house.moving()


if __name__ == '__main__' :
    houseinfo_project.app_init()
    main()