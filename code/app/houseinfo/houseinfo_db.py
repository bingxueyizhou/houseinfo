#!/usr/bin/python3
import sqlite3
import os

import code.app.houseinfo.app_project as app_project
v2log = None

class HouseInfoDB:
    HOUSE_INFO_DB_HOME = os.path.dirname( os.path.realpath(__file__) )
    HOUSE_INFO_DB_PATH = HOUSE_INFO_DB_HOME+"/data/house_info.db"

    SQL_QUERY_TABLE_EXIST = "SELECT NAME FROM SQLITE_MASTER " \
                           "WHERE TYPE='table' AND NAME='%s'"
    # 房源表
    # ID HSID TITLE ZONE NAME EXTRA URL IN_TIME
    SQL_HOUSE_INFO_TABLE_NAME = "HOUSE_INFO"
    SQL_CREATE_HOUSE_INFO_TABLE = "CREATE TABLE IF NOT EXISTS `HOUSE_INFO` (" \
                                  "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                                  "HSID NOT NULL," \
                                  "TITLE TEXT NOT NULL," \
                                  "ZONE TEXT," \
                                  "NAME TEXT," \
                                  "EXTRA TEXT," \
                                  "URL TEXT," \
                                  "IN_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP );"
    SQL_QUERY_HOUSE_INFO_TABLE = "SELECT * FROM `HOUSE_INFO` WHERE HSID='%s';"
    SQL_INSERT_HOUSE_INFO_TABLE = "INSERT INTO HOUSE_INFO (HSID, TITLE, ZONE, NAME, EXTRA, URL) " \
                                  "VALUES('%s', '%s', '%s', '%s', '%s', '%s');"
    # 房源详情表
    # ID HSID MARKETING
    SQL_CREATE_HOUSE_DETAILS_TABLE = "CREATE TABLE IF NOT EXISTS `HOUSE_DETAILS` (" \
                                     "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                                     "HSID INTEGER NOT NULL," \
                                     "MARKETING DATE);"
    SQL_INSERT_HOUSE_DETAILS_TABLE = "INSERT INTO `HOUSE_DETAILS` (HSID, MARKETING) VALUES('%s', '%s') ;"
    SQL_QUERY_HOUSE_DETAILS_TABLE = "SELECT * FROM `HOUSE_DETAILS` WHERE HSID=%s"

    # 查询所有
    SQL_QUERY_ALL_HOUSE_INFO = "select * from HOUSE_INFO left outer join HOUSE_DETAILS "\
                                "on HOUSE_INFO.HSID = HOUSE_DETAILS.HSID;"

    def touch(self, path):
        with open(path, 'a'):
            os.utime(path, None)

    def check_dirs(self):
        basedir = os.path.dirname(self.HOUSE_INFO_DB_PATH)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        if os.path.exists(self.HOUSE_INFO_DB_PATH):
            self.touch(self.HOUSE_INFO_DB_PATH)

    def create_db_table_if_not_exist(self, table_name, create_sql):
        res = self.conn.execute(self.SQL_QUERY_TABLE_EXIST%(table_name) )
        is_exist = False
        for row in res:
            if row[0] is table_name:
                is_exist = True
            break
        if is_exist == False:
            self.conn.execute(create_sql)
            v2log.info("create table %s" % table_name)

    def create_db_table(self):
        self.conn.execute(self.SQL_CREATE_HOUSE_INFO_TABLE)
        self.conn.execute(self.SQL_CREATE_HOUSE_DETAILS_TABLE)

    def close(self):
        self.conn.close()
        self.conn = None

    def __init__(self, path=None):
        global v2log
        v2log = app_project.get_logger()

        self.conn = None
        if path is not None:
            self.HOUSE_INFO_DB_HOME = path
        self.HOUSE_INFO_DB_PATH = self.HOUSE_INFO_DB_HOME + "/db/house_info.db"

        self.check_dirs()

        if self.conn is None:
            self.conn = sqlite3.connect(self.HOUSE_INFO_DB_PATH)
        if self.conn is None:
            v2log.warn("opened house info database failed.")
        else:
            self.conn.cursor()
            self.create_db_table()
            v2log.info("opened house info database successfully.")


    # ID TITLE ZONE NAME EXTRA URL DATE
    def add_house_info(self, hsid, title, zone, name, extra, url):
        self.conn.execute(self.SQL_INSERT_HOUSE_INFO_TABLE %
                          (hsid, title, zone, name, extra, url))
        self.conn.commit()

    # ID TITLE ZONE NAME EXTRA URL DATE
    def query_house_info(self, hsid):
        res = self.conn.execute(self.SQL_QUERY_HOUSE_INFO_TABLE % hsid)
        for row in res:
            if row[1] == hsid:
                ret = dict()
                ret['id'] = row[0]
                ret['hsid'] = row[1]
                ret['title'] = row[2]
                ret['zone'] = row[3]
                ret['name'] = row[4]
                ret['extra'] = row[5]
                ret['url'] = row[6]
                ret['in_time'] = row[7]
                return ret
        return None

    def add_house_details(self, hsid, marketing):
        self.conn.execute(self.SQL_INSERT_HOUSE_DETAILS_TABLE % (hsid, marketing) )
        self.conn.commit()

    def query_house_details(self, hsid):
        #print(self.SQL_QUERY_HOUSE_DETAILS_TABLE % hsid )
        res = self.conn.execute(self.SQL_QUERY_HOUSE_DETAILS_TABLE % hsid)
        for row in res:
            if row[1] == hsid:
                ret = dict()
                ret['id'] = row[0]
                ret['hsid'] = row[1]
                ret['marketing'] = row[2]
                return ret
        return None

    def query_all_house_info(self):
        sql_res = self.conn.execute(self.SQL_QUERY_ALL_HOUSE_INFO)
        result = []
        for row in sql_res:
            cell = dict()
            cell['id'] = row[0]
            cell['hsid'] = row[1]
            cell['title'] = row[2]
            cell['zone'] = row[3]
            cell['name'] = row[4]
            cell['extra'] = row[5]
            cell['marketing'] = row[10]
            cell['url'] = row[6]
            cell['in_time'] = row[7]
            result.append(cell)
        return result

if __name__ == "__main__":
    db = HouseInfoDB()
    ret = db.query_all_house_info()
    for cell in ret:
        print(cell)