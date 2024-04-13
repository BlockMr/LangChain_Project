from dataclasses import dataclass
from typing import Literal
from AbilityStats import AbilityStats
from Skills import Skills
from spells.Spell import Spell


@dataclass
class Character:
    name: str
    char_class: str
    level: int
    char_race: str
    background: str
    pl_name: str
    alignment: Literal['LG', 'LN', 'LV',
                       'NG', 'TN', 'NV',
                       'CG', 'CN', 'CV']
    exp_points: int
    inspiration: int
    prof_bonus: int
    armor_class: int
    initiative: int
    speed: int
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
    description: str
    abilities: AbilityStats
    skills: Skills
    spells: list[Spell]

    char_class_skill = {
        'Barbarian': {('animal_handling', 'athletics', 'intimidation', 'nature', 'perception', 'survival'): 2},
        'Bard': {('acrobatics', 'animal_handling', 'arcana', 'athletics', 'deception', 'history', 'insight',
                  'intimidation', 'investigation', 'medicine', 'nature', 'perception', 'performance', 'persuasion',
                  'religion', 'sleight_of_hand', 'stealth', 'survival'): 3},
        'Cleric': {('history', 'insight', 'medicine', 'persuasion', 'religion'): 2},
        'Druid': {('arcana', 'animal_handling', 'insight', 'medicine', 'nature', 'perception', 'religion', 'survival'): 2},
        'Fighter': {('acrobatics', 'animal_handling', 'athletics', 'history', 'insight', 'intimidation', 'perception'): 2},
        'Monk': {('acrobatics', 'athletics', 'history', 'insight', 'religion', 'stealth'): 2},
        'Paladin': {('athletics', 'medicine', 'insight', 'intimidation', 'persuasion', 'religion'): 2},
        'Ranger': {('animal_handling', 'athletics', 'insight', 'investigation', 'nature', 'perception', 'stealth',
                   'survival'): 3},
        'Rogue': {('acrobatics', 'athletics', 'deception', 'insight', 'intimidation', 'investigation', 'perception',
                  'perfomance', 'persuasion', 'sleight_of_hand', 'stealth'): 4},
        'Sorcerer': {('arcana', 'deception', 'insight', 'intimidation', 'persuasion', 'religion'): 2},
        'Warlock': {('arcana', 'deception', 'history', 'intimidation', 'investigation', 'nature', 'religion'): 2},
        'Wizard': {('arcana', 'history', 'insight', 'investigation', 'medicine', 'religion'): 2}
    }

    char_race_abil = {
        'Elf': {'dexterity': 2},
        'Dwarf': {'constitution': 2},
        'Halfling': {'dexterity': 2},
        'Gnome': {'intelligence': 2},
        'Dragonborn': {'strength': 2, 'charisma': 1},
        'Half-Orc': {'strength': 2, 'constitution': 1},
        'Tiefling': {'charisma': 2, 'intelligence': 1},
        'Human': {'strength': 1, 'dexterity': 1, 'constitution': 1, 'intelligence': 1, 'wisdom': 1, 'charisma': 1},
        'Half-Elf': {'charisma': 2, ('strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'): 1}
    }
