import unittest
from command.Parameters import Parameters

class testParameters(unittest.TestCase):
    def test_init(self):
        params = Parameters([])
        self.assertEqual(params.size(), 0)

        params = Parameters(["update"])
        self.assertEqual(params.size(), 1)

        params = Parameters(["update", "SH", "123456"])
        self.assertEqual(params.size(), 3)

    def test_action_series(self):
        params = Parameters(["update", "SH", "123456"])
        self.assertEqual(params.size(), 3)
        self.assertEqual(params.current(), "update");
        self.assertEqual(params.next(), "update");
        self.assertEqual(params.current(), "SH");
        self.assertEqual(params.next(), "SH");
        self.assertEqual(params.current(), "123456");
        self.assertEqual(params.next(), "123456");
        self.assertEqual(params.current(), "");

        params.add("20220222")
        params.add("20220202")
        self.assertEqual(params.current(), "20220222");
        self.assertEqual(params.next(), "20220222");
        self.assertEqual(params.current(), "20220202");
        self.assertEqual(params.next(), "20220202");
        self.assertEqual(params.current(), "");
