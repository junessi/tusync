from command.State import State
from command.Update import Update
import common.usages as usages

class Command:
    def __init__(self, params):
        self.state = State.NULL

        cmd = params.next()
        if cmd == 'update':
            try:
                self.state = Update(params).get_state()
            except BaseException as e:
                print(e)
                usages.printUpdateUsage()
        else:
            print("Unknown command: '{0}'".format(cmd))
            usages.printCommands()

    def state(self):
        return self.state
