import sys
import os
import platform

global APP_PRO_HOME
global v2log
global v2conf

APP_PRO_HOME  = os.path.dirname(os.path.realpath(__file__))
APP_DATA_HOME = APP_PRO_HOME + "/user_data"

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

def get_system_type():
    return platform.system()

def get_linux_path():
    return "/var/v2info/"

def get_windows_path():
    path = os.path.dirname(os.environ["USERPROFILE"]+"/")
    return path + "/v2info"

def get_default_path():
    sys_type = get_system_type()
    if sys_type is "Windows":
        return get_windows_path()
    if sys_type is "Linux":
        return get_linux_path()
    return None

def get_project_default_path():
    return APP_PRO_HOME

def app_init(path=None):
    global APP_PRO_HOME
    global APP_DATA_HOME

    sys_path = get_default_path()
    if sys_path is not None:
        APP_PRO_HOME = sys_path

    if path is not None:
        APP_PRO_HOME = path
    print(APP_PRO_HOME)
    APP_DATA_HOME = APP_PRO_HOME + "/user_data"
    init_logger()
    set_logger(APP_DATA_HOME + "/log/v2info.log")

    init_config()
    set_config(APP_DATA_HOME + "/conf/v2info.conf")