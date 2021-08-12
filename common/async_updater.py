import asyncio
from data.TUData import TUData

class AsyncUpdater():
    def __init__(self, dates):
        self.dates = dates

    async def updater(self, q):
        td = TUData()
        while q.empty() == False:
            date = await q.get()
            # print("update {0}".format(date))
            td.update_daily(trade_date = str(date))
            await asyncio.sleep(1)
            q.task_done()

    async def start_update(self):
        q = asyncio.Queue()
        for date in self.dates:
            await q.put(date)

        num_updaters = 4
        updaters = [asyncio.create_task(self.updater(q)) for _ in range(num_updaters)]
        await q.join()
        for u in updaters:
            u.cancel()

    def run(self):
        asyncio.run(self.start_update())
