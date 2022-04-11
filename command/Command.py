from command.State import State
from command.Update import Update
from command.Fetch import Fetch
import common.usages as usages

def printState(state):
    if state == State.INVALID_DATE:
        print('Invalid date given. Valid form should be YYYYMMDD.')
    elif state == State.UNKNOWN_COMMAND:
        print('Unknown command.')
        usages.printCommands()

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
                self.state = State.UNKNOWN_COMMAND

            printState(self.state)

        except BaseException as e:
            print("Command: {}".format(e))
            usages.printUpdateUsage()

    def get_state(self):
        return self.state
