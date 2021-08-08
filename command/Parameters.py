class Parameters:
    def __init__(self, parameters):
        self.index = 0 if len(parameters) > 0 else -1
        self.parameters = parameters

    def current(self):
        if self.index >= 0 and self.index < len(self.parameters):
            return self.parameters[self.index]

        return ''

    def next(self):
        """
            Return current parameter and go to next parameter.
        """
        if self.index >= 0 and self.index < len(self.parameters):
            next_token = self.parameters[self.index]
            self.index += 1
            return next_token

        return ''
