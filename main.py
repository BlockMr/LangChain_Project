class Character:
    def __init__(self, name, calss, level, bg, pl_name, race, alignment, exp_points,
                 inspiration, prof_bonus, armor_class, initiative, speed, age, height, weight, eyes, skin, hair):

        self.name = name
        self.calss = calss
        self.level = level
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


class AbilityStat:
    def __init__(self, strength, dexterity, const, intell, wisdom, charisma):
        self.strength = strength
        self.dexterity = dexterity
        self.const = const
        self.intell = intell
        self.wisdom = wisdom
        self.charisma = charisma
