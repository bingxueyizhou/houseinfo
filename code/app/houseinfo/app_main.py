import sys

import code.app.houseinfo.app_project as houseinfo_project
from code.app.houseinfo.houseinfo_crawler import CrawlerHouse


def main():
    house = CrawlerHouse(houseinfo_project.get_app_data_path())
    house.moving()
    house.moving_to_fix_db()

if __name__ == '__main__' :
    houseinfo_project.app_init()
    main()