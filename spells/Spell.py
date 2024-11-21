from dataclasses import dataclass


@dataclass
class Spell:
    name: str
    level: str
    cast_time: str
    duration: str
    school: str
    range_area: int
    attack_save: str
    components: str
    description: str
