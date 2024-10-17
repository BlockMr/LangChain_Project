class Item:
    def __init__(self, name, price, weight, description=None):
        self.name = name
        self.price = price
        self.weight = weight
        self.description = description

    def __str__(self):
        attributes = [f"{name}={value}" for name, value in vars(self).items() if not name.startswith('__')]
        return f"{self.__class__.__name__}({', '.join(attributes)})"
