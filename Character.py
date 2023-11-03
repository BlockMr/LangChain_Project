from dataclasses import dataclass
from typing import Literal


@dataclass
class Character:
    name: str
    char_class: str
    level: int
    race: str
    background: str
    pl_name: str
    worldview: str
    exp_points: int
    inspiration: int
    prof_bonus: int
    armor_class: int
    initiative: int
    speed: int
    initiative: int
    armor_class: int
    hair: str
    skin: str
    eyes: str
    height: int
    weight: int
    age: int
    cur_hit_points: int
    temp_hit_points: int
    hit_dice: int
    death_saves: Literal[0, 1, 2, 3]
    person_traits: str
    ideals: str
    bonds: str
    flaws: str
    features_traits: str
    passive_wisdom: int
    other_prof_lang: str
    opisanie_pers: str

