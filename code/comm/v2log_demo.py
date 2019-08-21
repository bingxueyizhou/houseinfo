# -*- coding:utf-8 -*-

# start 引入日志模块
import sys
import os
APP_PRO_HOME = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(APP_PRO_HOME + ".."))
from code.comm.v2log import v2info
# end  引入日志模块

def applog_test():
    v2info.debug("debug message")              #告警级别最低，只有在诊断问题时才有兴趣的详细信息。

    v2info.info("info message")                #告警级别比debug要高，确认事情按预期进行。

    v2info.warning("warning message")          #告警级别比info要高，该模式是默认的告警级别！预示着一些意想不到的事情发生，或在不久的将来出现一些问题（例如“磁盘空间低”）。该软件仍在正常工作。

    v2info.error("error message")              #告警级别要比warning药膏，由于一个更严重的问题，该软件还不能执行某些功能。

    v2info.critical("critical message")        #告警级别要比error还要高，严重错误，表明程序本身可能无法继续运行。

if __name__ == "__main__":
    applog_test()