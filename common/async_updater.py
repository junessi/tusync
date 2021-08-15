import threading
import queue
import time
from data.TUData import TUData

class AsyncUpdater():
    def __init__(self):
        self.num_updaters = 2
        self.td = TUData()
        self.queue_lock = threading.Lock()

    def updater(self, updater_id):
        while True:
            try:
                self.queue_lock.acquire()
                date = self.queue.get_nowait()
                self.queue.task_done()
                self.queue_lock.release()

                print("updater {0} got {1}".format(updater_id, date))
                self.num_of_stocks_updated += self.td.update_daily(trade_date = str(date))
                # time.sleep(5)
                print("updater {0} finished updating {1}".format(updater_id, date))
            except queue.Empty:
                # queue is empty, exit thread.
                print("Exception: queue empty")
                self.queue_lock.release()
                break

    def start_update(self, dates):
        self.finished = False
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

