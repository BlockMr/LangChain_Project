from dataclasses import dataclass


@dataclass
class AbilityStat:
    value: int
    bonus: int


@dataclass
class AbilityStats:
    strength: AbilityStat
    dexterity: AbilityStat
    const: AbilityStat
    intell: AbilityStat
    wisdom: AbilityStat
    charisma: AbilityStat
