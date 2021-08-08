from command.State import State
from command.Update import Update

class Command:
    def __init__(self, params):
        self.state = State.NULL

        cmd = params.next()
        if cmd == 'update':
            self.state = Update(params).get_state()
        else:
            raise BaseException("Unknown command: '{0}'".format(cmd))

    def state(self):
        return self.state
