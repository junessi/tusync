from command.State import State
from command.Update import Update
from command.Fetch import Fetch
import common.usages as usages

class Command:
    def __init__(self, params):
        self.state = State.NULL

        cmd = params.next()
        try:
            if cmd == 'update':
                self.state = Update(params).get_state()
            elif cmd == 'fetch':
                self.state = Fetch(params).get_state()
            else:
                print("Command: Unknown command: '{0}'".format(cmd))
                usages.printCommands()
        except BaseException as e:
            print("Command: {}".format(e))
            usages.printUpdateUsage()

    def state(self):
        return self.state
