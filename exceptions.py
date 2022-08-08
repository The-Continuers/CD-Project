class CompilerPanic(Exception):

    def __init__(self, *args, caused_by: Exception = None):
        super(CompilerPanic, self).__init__(*args)
        self.caused_by = caused_by

    def __str__(self):
        message = super(CompilerPanic, self).__str__()
        if self.caused_by is not None:
            message = ', '.join([message, str(self.caused_by)])
        return message
