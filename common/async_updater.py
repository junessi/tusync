import threading
import queue
import time
from data.TUData import TUData

class AsyncUpdater():
    def __init__(self):
        self.num_updaters = 16
        self.td = TUData()
        self.queue_lock = threading.Lock()
        self.call_ts_lock = threading.Lock()
        self.set_call_limit(500, 60) # 500 calls/min

    def updater(self, updater_id):
        while True:
            try:
                self.queue_lock.acquire()
                date = self.queue.get_nowait() # will throw queue.Empty when self.queue is empty
                self.queue.task_done()
                self.queue_lock.release()

                self.wait_for_available_call()

                # print("updater {0} got {1}".format(updater_id, date))
                self.num_of_stocks_updated += self.td.update_daily(trade_date = str(date))
                # time.sleep(5)
                # print("updater {0} finished updating {1}".format(updater_id, date))
            except queue.Empty:
                # queue is empty, exit thread.
                # print("Exception: queue empty")
                self.queue_lock.release()
                break

    def wait_for_available_call(self):
        try:
            self.call_ts_lock.acquire()
            while self.call_timestamps.full():
                # remove all time stamps older than self.n_seconds
                sixty_seconds_ago = time.time() - self.n_seconds
                timestamps_list = list(self.call_timestamps)
                n = len(timestamps_list)
                # print("timestamps queue size: " + n)
                for i in range(n):
                    t = timestamps_list[i]
                    if t <= sixty_seconds_ago:
                        # print("remove " + t)
                        self.call_timestamps.get()
                        self.call_timestamps.task_done()
                    else:
                        break

                if self.call_timestamps.full() == False:
                    break

                time.sleep(1)

            self.call_timestamps.put(time.time())
            self.call_ts_lock.release()
        except:
            self.call_ts_lock.release()

    def set_call_limit(self, ncalls, n_seconds):
        """
            call limit ncalls/n_seconds
        """
        self.ncalls = ncalls
        self.n_seconds = n_seconds
        self.call_timestamps = queue.Queue(self.ncalls)

    def start_update(self, dates):
        self.queue = queue.Queue()

        for date in dates:
            self.queue.put(date)

        updaters = list()
        for i in range(self.num_updaters):
            u = threading.Thread(target = self.updater, args = (i,))
            updaters.append(u)
            u.start()

        self.queue.join()
        # print("queue joined")
        for u in updaters:
            u.join()
        # print("updaters joined")

    def update_all_stocks_on_dates(self, dates):
        self.num_of_stocks_updated = 0
        self.start_update(dates)

        return self.num_of_stocks_updated

