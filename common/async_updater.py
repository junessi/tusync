import asyncio
from data.TUData import TUData

class AsyncUpdater():
    def __init__(self):
        self.num_updaters = 2
        self.td = TUData()

    async def updater(self, updater_id, q):
        while q.empty() == False:
            date = await q.get()
            q.task_done()

            await asyncio.sleep(1)
            self.num_of_stocks_updated += self.td.update_daily(trade_date = str(date))

    async def start_update(self, dates):
        q = asyncio.Queue()
        for date in dates:
            await q.put(date)

        updaters = [asyncio.create_task(self.updater(i, q)) for i in range(self.num_updaters)]
        await asyncio.gather(*updaters)
        await q.join()
        for u in updaters:
            u.cancel()

    def update_all_stocks_on_dates(self, dates):
        self.num_of_stocks_updated = 0
        asyncio.run(self.start_update(dates))

        return self.num_of_stocks_updated

