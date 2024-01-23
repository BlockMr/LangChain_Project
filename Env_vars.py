from dotenv import load_dotenv, dotenv_values


class Env_vars(object):
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(Env_vars, cls).__new__(cls)
            load_dotenv()
            config = dotenv_values()
            for key, value in config.items():
                getter = cls.create_getter(key)
                setter = cls.create_setter(key)
                prop = property(getter, setter)
                setattr(cls, key, prop)
                setattr(cls.__instance, '_' + key, value)
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


env_vars = Env_vars()

