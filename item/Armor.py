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


all_armor = {
    'Padded': ['5 gp', '8 lb.', '11 + Dex modifier', ArmorType.LIGHT, '-', 'Disadvantage',
               'Padded armor consists of quilted layers of cloth and batting.'],
    'Leather': ['10 gp', '10 lb.', '11 + Dex modifier', ArmorType.LIGHT, '-', '-',
                'The leather armor is made from tough but flexible material, which is usually made from animal hides.'],
    'Studded Leather': ['45 gp', '13 lb.', '12 + Dex modifier (max 2)', ArmorType.LIGHT, '-', '-',
                        'Made from tough but flexible leather, studded leather is reinforced'
                        ' with close-set rivets or spikes.'],
    'Hide': ['10 gp', '12 lb.', '12 + Dex modifier (max 2)', ArmorType.MEDIUM, '-', '-',
             'This crude armor consists of thick furs and pelts.'],
    'Chain Shirt': ['50 gp', '20 lb.', '13 + Dex modifier (max 2)', ArmorType.MEDIUM, '-', '-',
                    'Made of interlocking metal rings, a chain shirt is worn between layers of clothing or leather.'],
    'Scale Mail': ['50 gp', '45 lb.', '14 + Dex modifier (max 2)', ArmorType.MEDIUM, '-', 'Disadvantage',
                   'This armor consists of a coat and leggings made of leather covered with overlapping pieces'
                   ' of metal, much like the scales of a fish.'],
    'Breastplate': ['400 gp', '20 lb.', '14 + Dex modifier (max 2)', ArmorType.MEDIUM, '-', '-',
                    'This armor consists of a fitted metal chest piece worn with supple leather.'],
    'Half Plate': ['750 gp', '40 lb.', '15 + Dex modifier (max 2)', ArmorType.MEDIUM, '-', 'Disadvantage',
                   'Half plate consists of shaped metal plates that cover most of the wearer’s body.'],
    'Ring Mail': ['30 gp', '40 lb.', '14', ArmorType.HEAVY, '-', 'Disadvantage',
                  'This armor is leather armor with heavy rings sewn into it.'],
    'Chain Mail': ['75 gp', '55 lb.', '16', ArmorType.HEAVY, 'Str 13', 'Disadvantage',
                   'Made of interlocking metal rings, chain mail includes a layer of quilted fabric worn underneath'
                   ' the mail to prevent chafing and to cushion the impact of blows.'],
    'Splint': ['200 gp', '60 lb.', '17', ArmorType.HEAVY, 'Str 15', 'Disadvantage',
               'This armor is made of narrow vertical strips of metal riveted to a backing of leather that is worn over'
               ' cloth padding.'],
    'Plate': ['1,500 gp', '65 lb.', '18', ArmorType.HEAVY, 'Str 15', 'Disadvantage',
              'Plate consists of shaped, interlocking metal plates to cover the entire body.'
              ' A suit of plate includes gauntlets, heavy leather boots, a visored helmet, and thick layers'
              ' of padding underneath the armor.'],
    "Shield": ["10 gp", "6 lb.", "+2", ArmorType.SHIELD, '-', '-',
               'A shield is made from wood or metal and is carried in one hand. Wielding a shield increases your Armor'
               ' Class by 2. You can benefit from only one shield at a time.']
}

