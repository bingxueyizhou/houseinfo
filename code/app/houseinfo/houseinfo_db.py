#!/usr/bin/python3
import os

import code.app.houseinfo.app_project as app_project
v2log = None

class HouseInfoDB:
    # outer define
    DB_OK = 0
    DB_ERROR = -1

    # inner value
    __conn = None

    # inner sql values
    HOUSE_INFO_DB_HOME = os.path.dirname( os.path.realpath(__file__) )
    HOUSE_INFO_DB_PATH = HOUSE_INFO_DB_HOME+"/data/house_info.db"

    SQL_QUERY_TABLE_EXIST = "SELECT NAME FROM SQLITE_MASTER " \
                            "WHERE TYPE='table' AND NAME='%s'"
    # 房源表
    # ID HSID TITLE ZONE NAME EXTRA URL IN_TIME
    SQL_HOUSE_INFO_TABLE_NAME = "HOUSE_INFO"
    SQL_CREATE_HOUSE_INFO_TABLE = "CREATE TABLE IF NOT EXISTS `HOUSE_INFO` (" \
                                  "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                                  "HSID INTEGER UNIQUE NOT NULL," \
                                  "TITLE TEXT NOT NULL," \
                                  "ZONE TEXT," \
                                  "NAME TEXT," \
                                  "EXTRA TEXT," \
                                  "URL TEXT," \
                                  "IN_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP );"
    SQL_QUERY_HOUSE_INFO_TABLE = "SELECT * FROM `HOUSE_INFO` WHERE HSID=%s;"
    SQL_INSERT_HOUSE_INFO_TABLE = "INSERT INTO HOUSE_INFO (HSID, TITLE, ZONE, NAME, EXTRA, URL) " \
                                  "VALUES('%s', '%s', '%s', '%s', '%s', '%s');"
    # 房源详情表
    # ID HSID MARKETING
    SQL_CREATE_HOUSE_DETAILS_TABLE = "CREATE TABLE IF NOT EXISTS `HOUSE_DETAILS` (" \
                                     "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                                     "HSID INTEGER UNIQUE NOT NULL," \
                                     "AREA REAL," \
                                     "MARKETING DATE);"
    SQL_INSERT_HOUSE_DETAILS_TABLE = "INSERT INTO `HOUSE_DETAILS` (HSID, MARKETING, AREA) VALUES('%s', '%s', '%s') ;"
    SQL_QUERY_HOUSE_DETAILS_TABLE = "SELECT * FROM `HOUSE_DETAILS` WHERE HSID=%s"

    # 查询所有
    SQL_QUERY_ALL_HOUSE_INFO = "select * from HOUSE_INFO left outer join HOUSE_DETAILS "\
                                "on HOUSE_INFO.HSID = HOUSE_DETAILS.HSID;"
    SQL_QUERY_ALL_HOUSE_INFO_HOLE = "select * from (" \
                                        "select " \
                                        "HOUSE_INFO.HSID as HSID, " \
                                        "NAME, URL, " \
                                        "HOUSE_DETAILS.HSID as E_HSID " \
                                        "from HOUSE_INFO left outer join HOUSE_DETAILS " \
                                            "on HOUSE_INFO.HSID = HOUSE_DETAILS.HSID" \
                                    ")  where E_HSID is null"

    # inner functions
    def __init__(self, path=None):
        global v2log

        # step 1: init frame work. and create dir and file.
        v2log = app_project.get_logger()
        if path is not None:
            self.HOUSE_INFO_DB_HOME = path
        self.HOUSE_INFO_DB_PATH = self.HOUSE_INFO_DB_HOME + "/db/house_info.db"
        self.__check_dirs()

        # step 2: try to connect database
        app_project.init_v2db(self.HOUSE_INFO_DB_PATH)
        self.__conn = app_project.get_v2db()

        # step 3: database first init.
        if self.__conn is None:
            v2log.warn("opened house info database failed.")
        else:
            self.__create_db_table()
            v2log.info("opened house info database successfully.")

    @staticmethod
    def __touch(path):
        with open(path, 'a'):
            os.utime(path, None)

    def __check_dirs(self):
        basedir = os.path.dirname(self.HOUSE_INFO_DB_PATH)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        if not os.path.exists(self.HOUSE_INFO_DB_PATH):
            self.__touch(self.HOUSE_INFO_DB_PATH)

    def __create_db_table_if_not_exist(self, table_name, create_sql):
        res = self.__conn.execute(self.SQL_QUERY_TABLE_EXIST % (table_name))
        is_exist = False
        for row in res:
            if row[0] is table_name:
                is_exist = True
            break
        if is_exist == False:
            self.__conn.execute(create_sql)
            v2log.info("create table %s" % table_name)

    def __create_db_table(self):
        self.__conn.execute(self.SQL_CREATE_HOUSE_INFO_TABLE)
        self.__conn.execute(self.SQL_CREATE_HOUSE_DETAILS_TABLE)

    # outer function
    def close(self):
        return

    """  ADD  """
    def add_house_info(self, hsid, title, zone, name, extra, url):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_INSERT_HOUSE_INFO_TABLE % (hsid, title, zone, name, extra, url)
        try:
            self.__conn.execute(sql)
            self.__conn.commit()
            return self.DB_OK
        except BaseException as e:
            v2log.warn("sql: %s, except:%s"%(sql, e))

        return self.DB_ERROR

    def add_house_details(self, hsid, marketing, area):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_INSERT_HOUSE_DETAILS_TABLE % (hsid, marketing, area)
        try:
            self.__conn.execute(sql)
            self.__conn.commit()
            return self.DB_OK
        except BaseException as e:
            v2log.warn("sql: %s, except:%s"%(sql, e))

        return self.DB_ERROR

    """  DELETE  """
    """  MODIFY  """
    """  QUERY  """
    def query_house_info(self, hsid):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_QUERY_HOUSE_INFO_TABLE % hsid
        v2log.debug("sql: %s "%(sql))
        try:
            res = self.__conn.execute(sql)
            for row in res:
                if str(row[1]) == hsid:
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
        except BaseException as e:
            v2log.warn("sql: %s, except:%s" % (sql, e))

        return None

    def query_house_details(self, hsid):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_QUERY_HOUSE_DETAILS_TABLE % hsid
        try:
            res = self.__conn.execute(sql)
            for row in res:
                if str(row[1]) == hsid:
                    ret = dict()
                    ret['id'] = row[0]
                    ret['hsid'] = row[1]
                    ret['marketing'] = row[2]
                    return ret
        except BaseException as e:
            v2log.warn("sql: %s, except:%s"%(sql, e))

        return None

    def query_all_house_info(self):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_QUERY_ALL_HOUSE_INFO
        try:
            sql_res = self.__conn.execute(sql)
            result = []
            for row in sql_res:
                cell = dict()
                cell['id'] = row[0]
                cell['hsid'] = row[1]
                cell['name'] = row[4]
                cell['zone'] = row[3]
                cell['area'] = row[10]
                cell['marketing'] = row[11]
                cell['extra'] = row[5]
                cell['title'] = row[2]
                cell['url'] = row[6]
                cell['in_time'] = row[7]
                result.append(cell)
            return result
        except BaseException as e:
            v2log.warn("sql: %s, except:%s"%(sql, e))

        return None

    def query_all_house_info_hole(self):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_QUERY_ALL_HOUSE_INFO_HOLE
        try:
            sql_res = self.__conn.execute(sql)
            result = []
            for row in sql_res:
                cell = dict()
                cell['hsid'] = row[0]
                cell['name'] = row[1]
                cell['url'] = row[2]
                result.append(cell)
            return result
        except BaseException as e:
            v2log.warn("sql: %s, except:%s"%(sql, e))

        return None


if __name__ == "__main__":
    db = HouseInfoDB()
    ret = db.query_all_house_info()
    for cell in ret:
        print(cell)