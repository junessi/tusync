import asyncio
from data.TUData import TUData

class AsyncUpdater():
    def __init__(self):
        self.num_updaters = 2

    async def updater(self, q):
        td = TUData()
        while q.empty() == False:
            date = await q.get()
            # print("update {0}".format(date))
            self.num_of_stocks_updated += td.update_daily(trade_date = str(date))
            await asyncio.sleep(1)
            q.task_done()

    async def start_update(self, dates):
        q = asyncio.Queue()
        for date in dates:
            await q.put(date)

        updaters = [asyncio.create_task(self.updater(q)) for _ in range(self.num_updaters)]
        await q.join()
        for u in updaters:
            u.cancel()

    def update_all_stocks_on_dates(self, dates):
        self.num_of_stocks_updated = 0
        asyncio.run(self.start_update(dates))

        return self.num_of_stocks_updated

