class MetaConstant(type):

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        raise TypeError


class Constant(object, metaclass=MetaConstant):

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        raise TypeError
