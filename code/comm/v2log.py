import logging
import os
import gzip
import time
from logging import handlers

"""
format参数中可能用到的格式化串:
    1>.%(name)s
         Logger的名字
    2>.%(levelno)s
        数字形式的日志级别
    3>.%(levelname)s
        文本形式的日志级别
    4>.%(pathname)s
        调用日志输出函数的模块的完整路径名，可能没有
    5>.%(filename)s
        调用日志输出函数的模块的文件名
    6>.%(module)s
        调用日志输出函数的模块名
    7>.%(funcName)s
        调用日志输出函数的函数名
    8>.%(lineno)d
        调用日志输出函数的语句所在的代码行
    9>.%(created)f
        当前时间，用UNIX标准的表示时间的浮 点数表示
    10>.%(relativeCreated)d
        输出日志信息时的，自Logger创建以 来的毫秒数
    11>.%(asctime)s
        字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
    12>.%(thread)d
        线程ID。可能没有
    13>.%(threadName)s
        线程名。可能没有
    14>.%(process)d
        进程ID。可能没有
    15>.%(message)s
        用户输出的消息
"""


class GzTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    def __init__(self, filename, when, interval):
        super(GzTimedRotatingFileHandler, self).__init__(filename, when, interval, encoding="utf-8")

    def doGzip(self, old_log):
        with open(old_log) as old:
            with gzip.open(old_log + '.gz', 'wb') as comp_log:
                comp_log.writelines(old)
        os.remove(old_log)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        # Issue 18940: A file may not have been created if delay is True.
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
            self.doGzip(dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt



global applog
logging.root.setLevel(logging.NOTSET)  # cancel Logger's level, standard to handler
applog = logging.getLogger(__name__)

# 文件夹与创建
log_file = "./log/app.log"
log_path_dir = os.path.dirname(log_file)
if not os.path.exists(log_path_dir):
    os.makedirs(log_path_dir)


formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(filename)s %(funcName)s: %(lineno)s] %(message)s")  #定义输出格式

fh = GzTimedRotatingFileHandler(filename=log_file, when="S", interval=1)
fh.setFormatter(formatter)
fh.setLevel("INFO")
applog.addHandler(fh)

# applog.handlers.pop()
