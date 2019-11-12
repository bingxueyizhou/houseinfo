#!/usr/bin/python3
import os

import code.app.ip_scout.app_project as app_project
v2log = None

class IPDB:
    # outer define
    DB_OK = 0
    DB_ERROR = -1

    # inner value
    __conn = None

    # inner sql values
    DB_HOME = os.path.dirname( os.path.realpath(__file__) )
    DB_PATH = DB_HOME+"/data/ip_history.db"

    SQL_QUERY_TABLE_EXIST = "SELECT NAME FROM SQLITE_MASTER " \
                            "WHERE TYPE='table' AND NAME='%s'"

    SQL_IP_HISTORY_TABLE_NAME = "IP_HISTORY"
    SQL_CREATE_IP_HISTORY_TABLE = "CREATE TABLE IF NOT EXISTS `IP_HISTORY` (" \
                                  "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                                  "IP TEXT NOT NULL," \
                                  "TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP );"
    SQL_INSERT_IP_HISTORY_TABLE = "INSERT INTO `IP_HISTORY` (IP) VALUES('%s');"
    SQL_QUERY_IP_HISTORY_TABLE = "SELECT * FROM `IP_HISTORY`;"
    SQL_QUERY_LAST_IP_RECORD = "SELECT * FROM `IP_HISTORY` ORDER BY `ID` DESC LIMIT 0,1;"

    # inner functions
    def __init__(self, path=None):
        global v2log

        # step 1: init frame work. and create dir and file.
        v2log = app_project.get_logger()
        if path is not None:
            self.DB_HOME = path
        self.DB_PATH = self.DB_HOME + "/db/ip_history.db"
        self.__check_dirs()

        # step 2: try to connect database
        app_project.init_v2db(self.DB_PATH)
        self.__conn = app_project.get_v2db()

        # step 3: database first init.
        if self.__conn is None:
            v2log.warn("opened ip history database failed.")
        else:
            self.__create_db_table()
            v2log.info("opened ip history database successfully.")

    @staticmethod
    def __touch(path):
        with open(path, 'a'):
            os.utime(path, None)

    def __check_dirs(self):
        basedir = os.path.dirname(self.DB_PATH)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        if not os.path.exists(self.DB_PATH):
            self.__touch(self.DB_PATH)

    def __create_db_table(self):
        self.__conn.execute(self.SQL_CREATE_IP_HISTORY_TABLE)

    # outer function
    def close(self):
        return

    """  ADD  """
    def add_ip_record(self, ip):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_INSERT_IP_HISTORY_TABLE % (ip)
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
    def query_all_record(self):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_QUERY_IP_HISTORY_TABLE
        v2log.debug("sql: %s "%(sql))
        try:
            res = self.__conn.execute(sql)
            result = []
            for row in res:
                cell = dict()
                cell['id'] = row[0]
                cell['ip'] = row[1]
                cell['time'] = row[7]
                result.append(cell)
            return result
        except BaseException as e:
            v2log.warn("sql: %s, except:%s" % (sql, e))

        return None

    def query_last_record(self):
        if self.__conn is None:
            v2log.error("database is unavailable.")
            return self.DB_ERROR

        sql = self.SQL_QUERY_LAST_IP_RECORD
        try:
            res = self.__conn.execute(sql)
            for row in res:
                ret = dict()
                ret['id'] = row[0]
                ret['ip'] = row[1]
                ret['time'] = row[2]
                return ret
        except BaseException as e:
            v2log.warn("sql: %s, except:%s"%(sql, e))

        return None

if __name__ == "__main__":
    db = IPDB()
    ret = db.query_all_record()
    for cell in ret:
        print(cell)