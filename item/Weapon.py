from Item import Item
from langchain_openai import ChatOpenAI
from Env_vars import env_vars
llm = ChatOpenAI(openai_api_key=env_vars.API_KEY_OPENAI)


class Weapon(Item):
    def __init__(self, name, price, weight, damage_type, damage, properties, range=None):
        super().__init__(name, price, weight)
        self.damage_type = damage_type
        self.damage = damage
        self.properties = properties
        self.range = range
        self.llm = ChatOpenAI(openai_api_key=env_vars.API_KEY_OPENAI)
        # name: [Cost, Damage, Weight, Properties]
        self.all_weapon = {'Sickle': ['1 gp', '1d4 slashing', '2 lb.', 'light'],
                      'Club': ['1 sp', '1d4 bludgeoning', '2 lb.', 'light'],
                      'Dagger': ['2 gp', '1d4 piercing', '1 lb.', 'finesse, light, thrown (range 20/60)'],
                      'Greatclub': ['2 sp', '1d8 bludgeoning', '10 lb.', 'two-handed'],
                      'Handaxe': ['5 gp', '1d6 slashing', '2 lb.', 'light, thrown (range 20/60)'],
                      'Javelin': ['5 sp', '1d6 piercing', '2 lb.', 'thrown (range 30/120)'],
                      'Light Hammer': ['2 gp', '1d4 bludgeoning', '2 lb.', 'light, thrown (range 20/60)'],
                      'Mace': ['5 gp', '1d6 bludgeoning', '4 lb.', '-'],
                      'Quarterstaff': ['2 sp', '1d6 bludgeoning', '4 lb.', 'versatile (1d8)'],
                      'Spear': ['1 gp', '1d6 piercing', '3 lb.', 'thrown (range 20/60), versatile (1d8)'],
                      'Crossbow, light': ['25 gp', '1d8 piercing', '5 lb.',
                                          'ammunition (range 80/320), loading, two-handed'],
                      'Shortbow': ['25 gp', '1d6 piercing', '2 lb.', 'ammunition (range 80/320), two-handed'],
                      'Sling': ['1 sp', '1d4 bludgeoning', '-', 'ammunition (range 30/120)'],
                      'Battleaxe': ['10 gp', '1d8 slashing', '4 lb.', 'versatile (1d10)'],
                      'Flail': ['10 gp', '1d8 bludgeoning', '2 lb.', '-'],
                      'Glaive': ['20 gp', '1d10 slashing', '6 lb.', 'heavy, reach, two-handed'],
                      'Greataxe': ['30 gp', '1d12 slashing', '7 lb.', 'heavy, two-handed'],
                      'Greatsword': ['50 gp', '2d6 slashing', '6 lb.', 'heavy, two-handed'],
                      'Halberd': ['20 gp', '1d10 slashing', '6 lb.', 'heavy, reach, two-handed'],
                      'Lance': ['10 gp', '1d12 piercing', '6 lb.', 'reach, special'],
                      'Longsword': ['15 gp', '1d8 slashing', '3 lb.', 'versatile (1d10)'],
                      'Maul': ['10 gp', '2d6 bludgeoning', '10 lb.', 'heavy, two-handed'],
                      'Morningstar': ['15 gp', '1d8 piercing', '4 lb.', '-'],
                      'Pike': ['5 gp', '1d10 piercing', '18 lb.', 'heavy, reach, two-handed'],
                      'Rapier': ['25 gp', '1d8 piercing', '2 lb.', 'finesse'],
                      'Scimitar': ['25 gp', '1d6 slashing', '3 lb.', 'finesse, light'],
                      'Shortsword': ['10 gp', '1d6 piercing', '2 lb.', 'finesse, light'],
                      'Trident': ['5 gp', '1d6 piercing', '4 lb.', 'thrown (range 20/60), versatile (1d8)'],
                      'War Pick': ['5 gp', '1d8 piercing', '2 lb.', '-'],
                      'Warhammer': ['15 gp', '1d8 bludgeoning', '2 lb.', 'versatile (1d10)'],
                      'Whip': ['2 gp', '1d4 slashing', '3 lb.', 'finesse, reach'],
                      'Blowgun': ['10 gp', '1 piercing', '1 lb.', 'ammunition (range 25/100), loading'],
                      'Crossbow, hand': ['75 gp', '1d6 piercing', '3 lb.',
                                         'ammunition (range 30/120), light, loading'],
                      'Crossbow, heavy': ['50 gp', '1d10 piercing', '18 lb.',
                                          'ammunition (range 100/400), heavy, loading, two-handed'],
                      'Longbow': ['50 gp', '1d8 piercing', '2 lb.',
                                  'ammunition (range 150/600), heavy, two-handed'],
                      'Net': ['1 gp', '-', '3 lb.', 'special, thrown (range 5/15)']}
