from dataclasses import dataclass
from typing import Literal


@dataclass
class Spells:
    level: int
    name: str
    cast_time: int
    duration: int
    school: str
    range_area: int
    attack_save: str
    components: Literal['V', 'S', 'M', '*']

