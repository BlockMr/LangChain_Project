from item.Item import Item


class Weapon(Item):
    def __init__(self, name, price, weight, damage_type, damage, properties, description=None):
        super().__init__(name, price, weight, description)
        self.damage_type = damage_type
        self.damage = damage
        self.properties = properties


# {'name': ['price', 'weight', 'damage', 'damage_type', ['properties']], 'description'}
all_weapon = {
    'Coast': ['5 gp', '2 lb', '1d6', 'piercing', ['finesse', 'light'],
              'A light weapon with a hilt and a thin, straight blade'],
    'Dagger': ['2 gp', '1 lb', '1d4', 'piercing', ['finesse', 'light', 'thrown (range 20/60)'],
               'A small, easily concealed weapon with a blade that can be used for slashing or stabbing'],
    'Dart': ['5 cp', '1/4 lb', '1d4', 'piercing', ['finesse', 'thrown (range 20/60)'],
             'A small, lightweight weapon with a sharp point, designed for throwing'],
    'Flail': ['10 gp', '2 lb', '1d8', 'bludgeoning', [''],
              'A weapon with a long handle and a spiked ball on a chain, used for striking opponents'],
    'Glaive': ['20 gp', '6 lb', '1d10', 'slashing', ['heavy', 'reach', 'two-handed'],
               'A long polearm with a curved blade on one end, used for slashing and striking from a distance'],
    'Greataxe': ['30 gp', '7 lb', '1d12', 'slashing', ['heavy', 'two-handed'],
                 'A large, heavy axe with a broad blade, used for chopping and cleaving'],
    'Greatclub': ['2 sp', '10 lb', '1d8', 'bludgeoning', ['two-handed'],
                  'A large, heavy wooden club, used for crushing and bashing'],
    'Greatsword': ['50 gp', '6 lb', '2d6', 'slashing', ['heavy', 'two-handed'],
                   'A massive sword with a double-edged blade, used for powerful strikes'],
    'Halberd': ['20 gp', '6 lb', '1d10', 'slashing', ['heavy', 'reach', 'two-handed'],
                'A polearm with an axe blade and a spike on the end, used for slashing and thrusting'],
    'Handaxe': ['5 gp', '2 lb', '1d6', 'slashing', ['light', 'thrown (range 20/60)'],
                'A small, versatile axe that can be used for chopping or throwing'],
    'Javelin': ['5 sp', '2 lb', '1d6', 'piercing', ['thrown (range 30/120)'],
                'A light spear designed for throwing at targets from a distance'],
    'Lance': ['10 gp', '6 lb', '1d12', 'piercing', ['reach', 'special'],
              'A long, heavy spear used by mounted warriors for charging attacks'],
    'Light Hammer': ['2 gp', '2 lb', '1d4', 'bludgeoning', ['light', 'thrown (range 20/60)'],
                     'A small hammer with a light head, used for precise strikes or throwing'],
    'Longbow': ['50 gp', '2 lb', '1d8', 'piercing', ['ammunition (range 150/600)', 'heavy', 'two-handed'],
                'A powerful bow designed for long-range shooting'],
    'Longsword': ['15 gp', '3 lb', '1d8', 'slashing', ['versatile (1d10)'],
                  'A versatile sword with a straight blade, suitable for one or two-handed use'],
    'Mace': ['5 gp', '4 lb', '1d6', 'bludgeoning', [''],
             'A heavy club with a metal head, used for crushing and bashing'],
    'Maul': ['10 gp', '10 lb', '2d6', 'bludgeoning', ['heavy', 'two-handed'],
             'A massive hammer with a heavy head, used for powerful strikes'],
    'Morningstar': ['15 gp', '4 lb', '1d8', 'piercing', [''],
                    'A spiked club with a metal head, used for piercing and bashing'],
    'Net': ['1 gp', '3 lb', '', '', ['special'],
            'A mesh of rope or chain designed to entangle and restrain opponents'],
    'Pike': ['5 gp', '18 lb', '1d10', 'piercing', ['heavy', 'reach', 'two-handed'],
             'A long spear with a sharp point, used for thrusting and keeping enemies at a distance'],
    'Quarterstaff': ['2 sp', '4 lb', '1d6', 'bludgeoning', ['versatile (1d8)'],
                     'A simple wooden staff that can be used for striking or blocking attacks'],
    'Rapier': ['25 gp', '2 lb', '1d8', 'piercing', ['finesse'],
               'A slender, pointed sword used for precise thrusts and quick strikes'],
    'Scimitar': ['25 gp', '3 lb', '1d6', 'slashing', ['finesse', 'light'],
                 'A curved blade sword used for slashing and cutting attacks'],
    'Shortbow': ['25 gp', '2 lb', '1d6', 'piercing', ['ammunition (range 80/320)', 'two-handed'],
                 'A small, lightweight bow designed for short-range shooting'],
    'Shortsword': ['10 gp', '2 lb', '1d6', 'piercing', ['finesse', 'light'],
                   'A small, versatile sword with a sharp point, used for stabbing and slashing'],
    'Sickle': ['1 gp', '2 lb', '1d4', 'slashing', ['light'],
               'A small, curved blade attached to a short handle, used for cutting and slashing'],
    'Sling': ['1 sp', '', '1d4', 'bludgeoning', ['ammunition (range 30/120)'],
              'A simple leather strap used to hurl small stones or bullets at targets'],
    'Spear': ['1 gp', '3 lb', '1d6', 'piercing', ['thrown (range 20/60)', 'versatile (1d8)'],
              'A simple weapon with a pointed tip and a wooden shaft, used for thrusting or throwing'],
    'Trident': ['5 gp', '4 lb', '1d6', 'piercing', ['thrown (range 20/60)', 'versatile (1d8)'],
                'A three-pronged spear used for thrusting or throwing at targets'],
    'War Pick': ['5 gp', '2 lb', '1d8', 'piercing', [''],
                 'A small, heavy pick with a sharp point, used for piercing armor and breaking through barriers'],
    'Warhammer': ['15 gp', '2 lb', '1d8', 'bludgeoning', ['versatile (1d10)'],
                  'A heavy hammer with a metal head, used for crushing armor and bones'],
    'Whip': ['2 gp', '3 lb', '1d4', 'slashing', ['finesse', 'reach'],
             'A long, flexible weapon made of leather or chain, used for striking and disarming opponents']
}
