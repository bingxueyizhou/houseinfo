import time

import code.app.ip_scout.app_project as app_scout
from code.app.ip_scout.scout import Scout

SLEEP_INTERVEL = 3600


def result_print(list):
    print("result:")
    print(list)


def main():
    scout = Scout()
    #while True:
    scout.handle(result_print, rand=True)
    #time.sleep(SLEEP_INTERVEL)


if __name__ == '__main__' :
    app_scout.app_init()
    main()