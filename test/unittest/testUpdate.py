from sre_parse import State
import unittest

from click import command
from command.Update import Update
from command.Command import Command
from command.State import State
from command.Parameters import Parameters
from unittest.mock import patch

class testUpdate(unittest.TestCase):
    def update_last_n_days_mock(self, days):
        print(days)
        return State.NULL

    def test_update_last_n_days(self):
        with patch.object(Update, 'update_last_n_days', new = self.update_last_n_days_mock):
            cmd = Command(Parameters(['update']))
            print(cmd.get_state())
            assert cmd.get_state() == State.DONE
