from dataclasses import dataclass


@dataclass
class AbilityStat:
    value: int
    bonus: int


@dataclass
class AbilityStats:
    strength: AbilityStat
    dexterity: AbilityStat
    constitution: AbilityStat
    intelligence: AbilityStat
    wisdom: AbilityStat
    charisma: AbilityStat
