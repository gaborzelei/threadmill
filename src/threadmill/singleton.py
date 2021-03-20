class Singleton(type):
    """ Singleton metaclass """

    _INSTANCES = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._INSTANCES:
            cls._INSTANCES[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._INSTANCES[cls]
