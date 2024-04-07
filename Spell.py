from typing import Literal


class Spell:
    level: int
    name: str
    cast_time: int
    duration: int
    school: str
    range_area: int
    attack_save: str
    components: Literal['V', 'S', 'M']
    description: str


casting_classes = ['Bard', 'Druid', 'Cleric', 'Ranger', 'Sorcerer', 'Warlock', 'Wizard', 'Paladin']
