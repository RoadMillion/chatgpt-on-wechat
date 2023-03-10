
class ICmd:
    def __int__(self):
        pass

    # try to use cmd answer
    def try_intercept(self, text, context=None):
        raise NotImplementedError
