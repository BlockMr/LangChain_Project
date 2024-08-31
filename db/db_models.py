from typing import Annotated
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker
import enum

from Env_vars import env_vars

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class Alignment(enum.Enum):
    LG = 'Lawful Good'
    NG = 'Neutral Good'
    CG = 'Chaotic Good'
    LN = 'Lawful Neutral'
    TN = 'True Neutral'
    CN = 'Chaotic Neutral'
    LV = 'Lawful Evil'
    NV = 'Neutral Evil'
    CV = 'Chaotic Evil'


class DeathSaves(enum.Enum):
    one = '0'
    two = '2'
    three = '3'


class Characters(Base):
    __tablename__ = 'characters'

    char_id: Mapped[intpk]
    name: Mapped[str]
    char_class: Mapped[str]
    level: Mapped[int]
    char_race: Mapped[str]
    background: Mapped[str]
    pl_name: Mapped[str]
    alignment: Mapped[Alignment]
    exp_points: Mapped[int]
    inspiration: Mapped[int]
    prof_bonus: Mapped[int]
    armor_class: Mapped[int]
    initiative: Mapped[int]
    speed: Mapped[int]
    cur_hit_points: Mapped[int]
    temp_hit_points: Mapped[int]
    hit_dice: Mapped[int]
    death_saves: Mapped[DeathSaves]
    person_traits: Mapped[str]
    ideals: Mapped[str]
    bonds: Mapped[str]
    flaws: Mapped[str]
    features_traits: Mapped[str]
    passive_wisdom: Mapped[int]
    other_prof_lang: Mapped[str]
    description: Mapped[str]
    abilities: Mapped[str]
    skills: Mapped[str]
    spells: Mapped[str]
    item: Mapped[str]


class Skills(Base):
    __tablename__ = 'skills'

    skill_set_id: Mapped[intpk]
    character_sheet_id: Mapped[int] = mapped_column(ForeignKey('characters.char_id'))
    acrobatics: Mapped[str]
    animal_handling: Mapped[str]
    arcana: Mapped[str]
    athletics: Mapped[str]
    deception: Mapped[str]
    history: Mapped[str]
    insight: Mapped[str]
    intimidation: Mapped[str]
    investigation: Mapped[str]
    medicine: Mapped[str]
    nature: Mapped[str]
    perception: Mapped[str]
    perfomance: Mapped[str]
    persuasion: Mapped[str]
    religion: Mapped[str]
    sleight_of_hand: Mapped[str]
    stealth: Mapped[str]
    survival: Mapped[str]


class Spells(Base):
    __tablename__ = 'spells'

    spell_id: Mapped[intpk]
    name: Mapped[str]
    level: Mapped[str]
    cast_time: Mapped[str]
    duration: Mapped[str]
    school: Mapped[str]
    range_area: Mapped[str]
    attack_save: Mapped[str]
    components: Mapped[str]
    description: Mapped[str]


class Char_spells(Base):
    __tablename__ = 'char_spells'

    char_spell_id: Mapped[intpk]
    char_id: Mapped[int] = mapped_column(ForeignKey('characters.char_id'))
    spell_id: Mapped[int] = mapped_column(ForeignKey('spells.spell_id'))


class AbilityStats(Base):
    __tablename__ = 'ability_stats'

    ability_stats_id: Mapped[intpk]
    char_sheet_id: Mapped[intpk] = mapped_column(ForeignKey('characters.char_id'))
    strength: Mapped[str]
    dexterity: Mapped[str]
    constitution: Mapped[str]
    intelligence: Mapped[str]
    wisdom: Mapped[str]
    charisma: Mapped[str]


class Gears(Base):
    __tablename__ = 'gears'

    gear_id: Mapped[intpk]
    name: Mapped[str]
    price: Mapped[str]
    weight: Mapped[str]
    description: Mapped[str | None]


class Char_items(Base):
    __tablename__ = 'char_items'

    char_item_id: Mapped[intpk]
    char_id: Mapped[int] = mapped_column(ForeignKey('characters.char_id'))
    item_id: Mapped[int] = mapped_column(ForeignKey('gears.gear_id'))


class Armors(Base):
    __tablename__ = 'armors'

    armor_id: Mapped[intpk]
    name: Mapped[str]
    price: Mapped[str]
    weight: Mapped[str]
    description: Mapped[str]
    armor_class: Mapped[str]
    strength: Mapped[str]
    stealth: Mapped[str]
    armor_type: Mapped[str]
    description: Mapped[str | None]


class Char_armors(Base):
    __tablename__ = 'char_armors'

    char_armors_id: Mapped[intpk]
    char_id: Mapped[int] = mapped_column(ForeignKey('characters.char_id'))
    armor_id: Mapped[int] = mapped_column(ForeignKey('armors.armor_id'))


class Weapons(Base):
    __tablename__ = 'weapons'

    weapon_id: Mapped[intpk]
    name: Mapped[str]
    price: Mapped[str]
    weight: Mapped[str]
    damage_type: Mapped[str]
    damage: Mapped[str]
    properties: Mapped[str]
    description: Mapped[str | None]


class Char_weapons(Base):
    __tablename__ = 'char_weapons'

    char_weapons_id: Mapped[intpk]
    char_id: Mapped[int] = mapped_column(ForeignKey('characters.char_id'))
    weapon_id: Mapped[int] = mapped_column(ForeignKey('weapons.weapon_id'))


engine = create_engine(f'postgresql+psycopg2://{env_vars.USER}:{env_vars.PASS}@localhost/{env_vars.DB_NAME}')

Session = sessionmaker(bind=engine)
session = Session()
