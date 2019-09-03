import sys
import os

global APP_PRO_HOME
global v2log
global v2conf

APP_PRO_HOME  = os.path.dirname(os.path.realpath(__file__))
APP_DATA_HOME = APP_PRO_HOME + "/user_data"
sys.path.append(os.path.abspath(APP_PRO_HOME + "/code"))
sys.path.append(os.path.abspath(APP_PRO_HOME + "/code/comm"))
sys.path.append(os.path.abspath(APP_PRO_HOME + "/code/app/houseinfo"))

from code.comm.v2log import init_v2log
from code.comm.v2conf import init_v2conf

## logger
def init_logger():
    global v2log
    v2log = None


def set_logger(path):
    global v2log
    v2log = init_v2log(path)


def get_logger():
    global v2log
    return v2log


## config
def init_config():
    global v2conf
    v2conf = None


def set_config(path):
    global v2conf
    v2conf = init_v2conf(path)


def get_config():
    global v2conf
    return v2conf


## path
def get_app_path():
    return APP_PRO_HOME


def get_app_data_path():
    return APP_DATA_HOME


def app_init(path=None):
    global APP_PRO_HOME
    global APP_DATA_HOME

    if path is not None:
        APP_PRO_HOME = path
    APP_DATA_HOME = APP_PRO_HOME + "/user_data"
    init_logger()
    set_logger(APP_DATA_HOME + "/log/app.log")

    init_config()
    set_config(APP_DATA_HOME + "/conf/app.conf")