from item.Item import Item
from enum import Enum, auto


class ArmorType(Enum):
    LIGHT = auto()
    MEDIUM = auto()
    HEAVY = auto()
    SHIELD = auto()


class Armor(Item):
    def __init__(self, name, price, weight, armor_class, strength, stealth, armor_type, description=None):
        super().__init__(name, price, weight, description)
        self.armor_class = armor_class
        self.strength = strength
        self.stealth = stealth
        self.armor_type = armor_type
