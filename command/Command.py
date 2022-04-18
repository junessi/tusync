from command.State import State
from command.Update import Update
from command.Fetch import Fetch
import common.usages as usages

def printState(state):
    if state == State.INVALID_DATE:
        print('Invalid date given. Valid form should be YYYYMMDD.')
    elif state == State.NEED_HELP:
        usages.printHelp()
    elif state == State.NEED_HELP_FOR_COMMAND:
        print('Unknown command.')
        usages.printCommands()
    elif state == State.NEED_HELP_FOR_UPDATE:
        usages.printUpdateUsage()
    elif state == State.NEED_HELP_FOR_FETCH:
        usages.printFetchUsage()

class Command:
    def __init__(self, params):
        self.state = State.NULL

        cmd = params.next()
        try:
            if cmd == 'update':
                if params.current() == 'help':
                    self.state = State.NEED_HELP_FOR_UPDATE
                else:
                    self.state = Update(params).get_state()
            elif cmd == 'fetch':
                if params.current() == 'help':
                    self.state = State.NEED_HELP_FOR_FETCH
                else:
                    self.state = Fetch(params).get_state()
            elif cmd == 'help':
                self.state = State.NEED_HELP
            else:
                self.state = State.NEED_HELP_FOR_COMMAND

        except BaseException as e:
            print("Command failed: {}".format(e))
            self.state = State.NEED_HELP
        finally:
            printState(self.state)

    def get_state(self):
        return self.state
