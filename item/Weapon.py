from item.Item import Item


class Weapon(Item):
    def __init__(self, name, price, weight, damage_type, damage, properties, description=None):
        super().__init__(name, price, weight, description)
        self.damage_type = damage_type
        self.damage = damage
        self.properties = properties
