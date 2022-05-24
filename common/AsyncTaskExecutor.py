import concurrent.futures

class Task():
    def __init__(self, f, *args):
        self.f = f
        self.args = args

    def run(self):
        self.f(*self.args)

class AsyncTaskExecutor():
    def __init__(self, num_workers = 16):
        self.num_workers = num_workers
        self.tasks = []

    def push(self, task):
        self.tasks.append(task)

    def run_task(self, task):
        task.run()

    def execute(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers = self.num_workers) as executor:
            executor.map(self.run_task, self.tasks)