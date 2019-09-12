import time
import threading


class ScheduleTask(object):
    MODE_TIMES = 1
    MODE_SINGLE = 2
    MODE_LOOP = 3

    def __init__(self, private=None, callback=None):
        self.private = private
        self.callback = callback


class Schedule(object):
    __trigger_cxt = threading.Semaphore(0)
    __queue_lock = threading.Semaphore(1)
    __initialized = False
    __task_list = []

    def __init__(self):
        self.start()

    def __loop(self):
        print("schedule start.")
        while True:
            self.__trigger_cxt.acquire()
            
            self.__queue_lock.acquire()
            for task in self.__task_list:
                task.callback(task.private)
            self.__task_list = []
            self.__queue_lock.release()

    def start(self):
        if not self.__initialized:
            t = threading.Thread(target=self.__loop)
            t.start()
            self.__initialized = True
        return


    def trigger(self):
        self.__trigger_cxt.release()
    
    
    def register(self, pridata=None, callback=None):
        self.__queue_lock.acquire()
        self.__task_list.append(ScheduleTask(pridata, callback))
        self.__queue_lock.release()
    
    def do(self, pri_data=None, cb=None, name="",
           interval=1, mode=ScheduleTask.MODE_LOOP, times=0):
        if mode == ScheduleTask.MODE_SINGLE:
            self.register(pri_data, cb)
            timer = threading.Timer(interval, (lambda: self.trigger()))
            timer.start()
        elif mode == ScheduleTask.MODE_LOOP:
            self.register(pri_data, cb)
            self.trigger()
            timer = threading.Timer(interval, lambda: self.do(pri_data=pri_data, cb=cb, name=name, interval=interval, mode=ScheduleTask.MODE_LOOP))
            timer.start()
        elif mode == ScheduleTask.MODE_TIMES:
            if times <= 0:
                return
            self.register(pri_data, cb)
            self.trigger()
            timer = threading.Timer(interval, lambda: self.do(pri_data=pri_data, cb=cb, name=name, interval=interval, mode=ScheduleTask.MODE_TIMES, times=(times-1)))
            timer.start()
            
# debug
if __name__ == '__main__':
    # name = "",        当前任务的名字
    # mode = MODE_LOOP, MODE_SINGLE/单次,MODE_LOOP/死循环/默认，MODE_TIMES/制定循环次数
    # times = 0,       MODE_TIMES时生效，循环多少次
    # interval = 1,    触发间隔，默认1s一次
    # pri_data = None,  私有数据每次都会自带
    # cb = None, 回调函数
    schedule = Schedule()
    schedule.do(pri_data="Crawler", cb=(lambda x: print("debug %s"%(time.time())) ),
                name="Crawler", interval=1, mode=ScheduleTask.MODE_TIMES, times=4)