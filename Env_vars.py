import os


class EnvVars:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(EnvVars, cls).__new__(cls)
            for key in os.environ:
                getter = cls.create_getter(key)
                setter = cls.create_setter(key)
                prop = property(getter, setter)
                setattr(cls, key, prop)
                setattr(cls.__instance, '_' + key, os.environ.get(key))
        return cls.__instance

    @staticmethod
    def create_getter(key):
        def getter(self):
            return getattr(self, '_' + key)
        return getter

    @staticmethod
    def create_setter(key):
        def setter(self, value):
            raise AttributeError(f"Cannot modify {key}")
        return setter


env_vars = EnvVars()
