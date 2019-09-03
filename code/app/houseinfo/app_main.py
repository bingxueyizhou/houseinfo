
import code.app.houseinfo.app_project as houseinfo_project
from code.app.houseinfo.houseinfo_crawler import CrawlerHouse

if __name__ == '__main__' :
    houseinfo_project.app_init()
    house = CrawlerHouse(houseinfo_project.get_app_data_path())
    house.moving()