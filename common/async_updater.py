import threading
import queue
import time
from data.TUData import TUData

class AsyncUpdater():
    def __init__(self):
        self.num_updaters = 128
        self.td = TUData()
        self.queue_lock = threading.Lock()
        self.num_of_stocks_updated_lock = threading.Lock()

    def updater(self, updater_id):
        while True:
            try:
                self.queue_lock.acquire()
                date = self.queue.get_nowait() # will throw queue.Empty when self.queue is empty
                self.queue.task_done()
                self.queue_lock.release()

                # print("updater {0} got {1}".format(updater_id, date))
                num_updated = self.td.update_daily(trade_date = str(date))
                time.sleep(1)
                self.num_of_stocks_updated_lock.acquire()
                self.num_of_stocks_updated += num_updated
                self.num_of_stocks_updated_lock.release()
                # time.sleep(5)
                # print("updater {0} finished updating {1}".format(updater_id, date))
            except queue.Empty:
                # queue is empty, exit thread.
                # print("Exception: queue empty")
                self.queue_lock.release()
                break
            except Exception as e:
                print("AsyncUpdater.update(): {}".format(e))
                self.queue_lock.release()

    def start_update(self, dates):
        self.queue = queue.Queue()

        for date in dates:
            self.queue.put(date)

        nparallel = self.num_updaters if self.num_updaters < self.queue.qsize() else self.queue.qsize()
        updaters = list()
        for i in range(nparallel):
            u = threading.Thread(target = self.updater, args = (i,))
            updaters.append(u)
            u.start()

        self.queue.join()
        for u in updaters:
            u.join()

    def update_all_stocks_on_dates(self, dates):
        self.num_of_stocks_updated = 0
        self.start_update(dates)

        return self.num_of_stocks_updated

