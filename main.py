from typing import Literal


class Character:
    def __init__(self, name, calss, level, bg, pl_name, race, alignment, exp_points,
                 inspiration, prof_bonus, armor_class, initiative, speed, age, height, weight, eyes, skin, hair,
                 cur_hit, temp_hit, hit_dice, person_traits, ideals, bonds, flaws, features_traits, passive_wisdom,
                 other_prof_lang, appearance, backstory, allies_organiz, add_features_trains, treasure, cantrips,
                 spell_cast_ability, spell_save_dc, spell_attack_bonus, spell_cast_class, enquipment, acrob, animal,
                 arc, athlet, deception, hostory, insight, intimidation, invest, med, nature, perception, performance,
                 persuasion, religion, sleight_of_hand, stealth, survival, death_saves: Literal[0]):

        self.name = name
        self.calss = calss
        self.level = level
        self.spell_cast_class = spell_cast_class
        # происхождение
        self.bg = bg
        # имя игрока
        self.pl_name = pl_name
        self.race = race
        # мировоззрение
        self.alignment = alignment
        self.exp_points = exp_points
        self.inspiration = inspiration
        self.speed = speed
        self.initiative = initiative
        self.armor_class = armor_class
        self.prof_bonus = prof_bonus
        self.hair = hair
        self.skin = skin
        self.eyes = eyes
        self.height = height
        self.weight = weight
        self.age = age
        self.cur_hit = cur_hit
        self.temp_hit = temp_hit
        self.hit_dice = hit_dice
        self.death_saves = death_saves
        self.person_traits = person_traits
        self.ideals = ideals
        self.bonds = bonds
        self.flaws = flaws
        self.features_traits = features_traits
        self.passive_wisdom = passive_wisdom
        self.other_prof_lang = other_prof_lang
        self.appearance = appearance
        self.backstory = backstory
        self.allies_organiz = allies_organiz
        self.add_features_trains = add_features_trains
        self.treasure = treasure
        self.cantrips = cantrips
        self.spell_cast_ability = spell_cast_ability
        self.spell_save_dc = spell_save_dc
        self.spell_attack_bonus = spell_attack_bonus
        self.enquipment = enquipment
        self.survival = survival
        self.stealth = stealth
        self.sleight_of_hand = sleight_of_hand
        self.religion = religion
        self.persuasion = persuasion
        self.performance = performance
        self.perception = perception
        self.nature = nature
        self.med = med
        self.invest = invest
        self.intimidation = intimidation
        self.insight = insight
        self.hostory = hostory
        self.deception = deception
        self.athlet = athlet
        self.arc = arc
        self.animal = animal
        self.acrob = acrob


class AbilityStat:
    def __init__(self, strength, dexterity, const, intell, wisdom, charisma):
        self.strength = strength
        self.dexterity = dexterity
        self.const = const
        self.intell = intell
        self.wisdom = wisdom
        self.charisma = charisma
