import unittest
import time
from common.AsyncTaskExecutor import AsyncTaskExecutor, Task

class testAsyncTaskExecutor(unittest.TestCase):
    def sleep_seconds(self, s, n):
        time.sleep(s)
        self.result.append(n)

    def test_execute_tasks(self):
        self.result = []
        a = AsyncTaskExecutor(4)
        a.push(Task(self.sleep_seconds, 0.2, 1))
        a.push(Task(self.sleep_seconds, 0.4, 3))
        a.push(Task(self.sleep_seconds, 0.5, 4))
        a.push(Task(self.sleep_seconds, 0.6, 5))
        a.push(Task(self.sleep_seconds, 0.1, 2)) # must be inserted between 1 and 3

        start_time = time.time()
        a.execute()
        end_time = time.time()
        self.assertLess(end_time - start_time, 0.7)
        self.assertEqual([1, 2, 3, 4, 5], self.result)
