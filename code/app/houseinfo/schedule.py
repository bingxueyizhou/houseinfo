import time
import threading

class ScheduleTask(object):
    MODE_TIMES  = 1
    MODE_SINGLE = 2
    MODE_LOOP   = 3

    def __init__(self, now=0, name="", mode=MODE_LOOP, times=0, interval=1, pridata=None, callback=None):
        self.name     = name
        self.interval = interval
        self.pridata  = pridata
        self.callback = callback
        self.mode       = mode
        self.times      = times
        self.createTime = now
        self.lastCall   = now


class Schedule(object):
    # old code start
    TICK = 1000
    MAX_TICK = 520131452013145201314
    SCHEDULE_SLEEP = float(TICK)/1000

    def __init__(self, tik=TICK):
        self.tik = tik
        self.tasklist = []
        self.current_tick = 0
        self.schedule_start = self.get_msec()

    def register(self, pridata=None, callback=None, name="",
                 interval=1, mode=ScheduleTask.MODE_LOOP, times=0):
        self.tasklist.append(
                    ScheduleTask(
                        self.get_tick()-interval, name, mode, times,
                        interval, pridata, callback))

    def get_msec(self):
        return int(round(time.time() * 1000))

    def get_tick(self):
        return self.current_tick

    def reset_all_task(self):
        self.current_tick -= Schedule.MAX_TICK
        for task in self.tasklist:
            task.lastCall -= Schedule.MAX_TICK

    def loop(self):
        while True:
            now = self.get_tick()
            for task in self.tasklist:
                if (task.lastCall + task.interval) <= now:
                    task.callback(task.pridata)
                    task.lastCall = now
                    if task.mode == ScheduleTask.MODE_TIMES:
                        task.times = task.times - 1
                    if task.mode == ScheduleTask.MODE_SINGLE:
                        self.tasklist.remove(task)
                    if task.mode == ScheduleTask.MODE_TIMES and task.times <= 0:
                        self.tasklist.remove(task)
            time.sleep(Schedule.SCHEDULE_SLEEP)
            self.current_tick = self.get_tick() + 1
            if self.get_tick() > Schedule.MAX_TICK:
                self.reset_all_task()

    def start(self):
        # self.loop()
        return
    # old code end

    def do(self, pri_data=None, cb=None, name="",
           interval=1, mode=ScheduleTask.MODE_LOOP, times=0):
        if mode == ScheduleTask.MODE_SINGLE:
            timer = threading.Timer(interval, (lambda: cb(pri_data)))
            timer.start()
        elif mode == ScheduleTask.MODE_LOOP:
            cb(pri_data)
            timer = threading.Timer(interval, lambda: self.do(pri_data=pri_data, cb=cb, name=name, interval=interval, mode=ScheduleTask.MODE_LOOP))
            timer.start()
        elif mode == ScheduleTask.MODE_TIMES:
            if times <= 0:
                return
            cb(pri_data)
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
    schedule.do(pri_data="Crawler", cb=(lambda x: print("debug")),
                name="Crawler", interval=1, mode=ScheduleTask.MODE_TIMES, times=4)