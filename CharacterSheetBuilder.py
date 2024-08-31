from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from Character import char_class_skill, char_race_abil
from AbilityStats import AbilityStats, AbilityStat
from Env_vars import env_vars
from item import Weapon as wp
from item import Armor as ar
from item import Item as it
from Skills import Skills
from spells.Spell import Spell
from db.db_methods import get_all_weapons_name, get_all_armors_name, get_all_gears_name
from db.db_methods import get_gear, get_armor, get_weapon, get_spell
from RuleChecker import RuleChecker


class CharacterSheetBuilder:
    abilities: AbilityStats = None
    description: str = None
    all_item: list = []
    char_class: str = None
    char_race: str = None
    skills: Skills = None
    spells: list = []

    def __init__(self, user_request, user_setting):
        self.user_request = user_request
        self.user_setting = user_setting
        self.llm = ChatOpenAI(openai_api_key=env_vars.API_KEY_OPENAI)
        self.get_description()
        self.get_weapon()
        self.get_armor()
        self.get_gear()
        self.get_char_class_race()
        self.get_ability_stats()
        self.get_skills()
        self.get_spells()

    def get_description(self):
        art_prompt = f'Напиши краткое художественное описание внешности и одежды для персонажа' \
                     f'существующего в рамках сеттинга описываемого как {self.user_setting} ' \
                     f'используя данное краткое описание: {self.user_request}, пожалуйста, обрати внимание на ' \
                     f'на все детали которые мог указать пользователь в запросе.'
        description = self.llm.invoke(art_prompt).content
        self.description = description

    def weapon_prompt(self):
        selection_prompt = f"Напиши предметы которые подходят к персонажу опираясь на его богатство или бедность," \
                           f"и краткое описание - {self.description}, " \
                           f"а выбери предметы пожалуйста только из этого списка - {get_all_weapons_name()}. Не из этого списка" \
                           f"предметы не предлагай" \
                           f"Их количество тоже нужно сопоставить персонажу" \
                           f"В ответ дай только названия этих предметов списоком по типу ['name', 'name', 'name']"

        weapon_for_char = self.llm.invoke(selection_prompt).content

        return weapon_for_char

    def weapon_selection(self, iter=int(env_vars.ITER)):
        for num_iter in range(iter):
            weapon_for_char = self.weapon_prompt()
            if RuleChecker.check_eval(weapon_for_char):
                fix_weapons = RuleChecker.deletion_of_excess(eval(self.weapon_prompt()), get_all_weapons_name())
                if len(fix_weapons) != 0:
                    return fix_weapons

        print('Подобрать weapon не удалось, повторите попытку создания')
        return quit()

    def get_weapon(self):
        for weapon_name in self.weapon_selection():
            weapon_inf = get_weapon(weapon_name)
            self.all_item.append(wp.Weapon(weapon_inf[0], weapon_inf[1], weapon_inf[2],
                                           weapon_inf[3], weapon_inf[4], weapon_inf[5], weapon_inf[6]))

    def armor_prompt(self):
        selection_prompt = f"Из списка {get_all_armors_name()} выбери армор для персонажа имеющего описание: " \
                           f"{self.description}" \
                           f"постарайся выбрать предметы подходящие персонажу по уровню достатка и тем задачам," \
                           f" которые он может решать в ходе своих приключений. учти, что надеть два комплекта" \
                           f" брони на себя он не сможет." \
                           f"Ответ дай в виде списка - ['name', 'name', 'name']"

        armor_for_char = self.llm.invoke(selection_prompt).content

        return armor_for_char

    def armor_selection(self, iter=int(env_vars.ITER)):
        for num_iter in range(iter):
            armor_for_char = self.armor_prompt()
            if RuleChecker.check_eval(armor_for_char):
                fix_armor = RuleChecker.deletion_of_excess(eval(armor_for_char), get_all_armors_name())
                if len(fix_armor) != 0:
                    return fix_armor

        print('Подобрать armor не удалось, повторите попытку создания')
        return quit()

    def get_armor(self):
        for armor_name in self.armor_selection():
            armor_inf = get_armor(armor_name)
            self.all_item.append(ar.Armor(armor_inf[0], armor_inf[1], armor_inf[3], armor_inf[3],
                                          armor_inf[4], armor_inf[5], armor_inf[6], armor_inf[7]))

    def gear_prompt(self):
        selection_prompt = f'Для персонажа имеющего краткое описание {self.description}, выбери только из списка ' \
                           f'{get_all_gears_name()} предметы, опираясь на его богатство или бедность, ' \
                           f'количетсво предметов тоже сопоставь персонажу. Вот так дай ответ - ["name", "name"], ' \
                           f'name возми в точности из списка {get_all_gears_name()}.' \
                           f'Еще раз убедись пожалуйста в том, что предметы или предмет, который ты выбрал, 100% ' \
                           f'находится в списке {get_all_gears_name()}, если нет, то выберай только из него, ' \
                           f'пожалуйста'

        gear_for_char = self.llm.invoke(selection_prompt).content

        return gear_for_char

    def gear_selection(self, iter=int(env_vars.ITER)):
        for num_iter in range(iter):
            gear_for_char = self.gear_prompt()
            if RuleChecker.check_eval(gear_for_char):
                fix_gear = RuleChecker.deletion_of_excess(eval(gear_for_char), get_all_gears_name())
                if len(fix_gear) != 0:
                    return fix_gear

        print('Подобрать gear не удалось, повторите попытку создания')
        return quit()

    def get_gear(self):
        for gear_name in self.gear_selection():
            gear_inf = get_gear(gear_name)
            self.all_item.append(it.Item(gear_inf[0], gear_inf[1], gear_inf[2], gear_inf[3]))

    def char_class_race_prompt(self):
        all_prompt = f'Выбери для персонажа, с кратким описание - {self.user_request} и находящегося в рамках' \
                     f'сеттинга - {self.user_setting}, расу из списка {char_race_abil.keys()}' \
                     f' и класс из списка {char_class_skill.keys()}, ы ответ дай толькоо список - ["race", "class"]'

        char_race_class = self.llm.invoke(all_prompt).content

        return char_race_class

    def get_char_class_race(self, iter=int(env_vars.ITER)):
        for num_iter in range(iter):
            char_race_class = self.char_class_race_prompt()
            if RuleChecker.check_eval(char_race_class):
                char_race_class = eval(char_race_class)
                if RuleChecker.check_char_and_race(char_race_class):
                    self.char_race = char_race_class[0]
                    self.char_class = char_race_class[1]
                    return

        print('Подобрать char_class_race не удалось, повторите попытку создания')
        return quit()

    def ability_stats_prompt(self):
        self.abilities = AbilityStats()
        stats_prompt = f'для персонажа имеющего описание {self.description} напиши значение харатеристик:' \
                       f'{", ".join(self.abilities.all_ability)}.' \
                       f'Характеристики могут принимать значение от 0 до 20. В ответ пожалуйста дай только список' \
                       f'в таком формате:' \
                       '{"strength": значение, "dexterity": значение, "constitution": значение,' \
                       ' "intelligence": значение, "wisdom": значение, "charisma": значение}'

        raw_stats = self.llm.invoke(stats_prompt).content

        return raw_stats

    def ability_stats_selection(self, iter=int(env_vars.ITER)):
        for num_iter in range(iter):
            raw_stats = self.ability_stats_prompt()
            if RuleChecker.check_eval(raw_stats):
                raw_stats = eval(raw_stats)
                if len(raw_stats) == 6:
                    return raw_stats

        print('Подобрать ability_stats не удалось, повторите попытку создания')
        return quit()

    def ability_stats_bonus_prompt_for_other_race(self):
        all_bonus = char_race_abil[self.char_race]
        bonus_for_other_race_prompt = f'для персонажа имеющего описание {self.description} выбери 2 характеристики' \
                                      f'которые более всего подходят для этого персонажа из списка ' \
                                      f'{list(all_bonus.keys())[1]} в ответ напиши только список этих характеристик - ' \
                                      f'["name", "name"]'
        bonus = self.llm.invoke(bonus_for_other_race_prompt).content

        return bonus

    def ability_stats_bonus_for_other_race_selection(self, iter=int(env_vars.ITER)):
        all_bonus = char_race_abil[self.char_race]
        for num_iter in range(iter):
            bonus = self.ability_stats_bonus_prompt_for_other_race()
            if RuleChecker.check_eval(bonus):
                bonus = eval(bonus)
                if RuleChecker.check_num_and_correct_list(bonus, 2, list(all_bonus.keys())[1]):
                    return bonus

        print('Подобрать ability_stats_for_other_race не удалось, повторите попытку создания')
        return quit()

    def get_ability_stats_bonus(self):
        # вместо Half-Elf создать список со всеми рассами
        if self.char_race == 'Half-Elf':
            return self.ability_stats_bonus_for_other_race_selection()
        else:
            return char_race_abil[self.char_race]

    def get_ability_stats(self):
        self.abilities = AbilityStats()
        raw_stats = self.ability_stats_selection()
        bonus = self.get_ability_stats_bonus()

        for ability_name in self.abilities.all_ability:
            for bonus_name in bonus:
                stat = AbilityStat()
                if ability_name == bonus_name:
                    stat.value = raw_stats[ability_name] + bonus[ability_name]
                    setattr(self.abilities, '_' + ability_name, stat)
                else:
                    stat.value = raw_stats[ability_name]
                    setattr(self.abilities, '_' + ability_name, stat)

    def bonus_skills_prompt(self):
        choice_skills_prompt = f'Для персонажа, имеющего описание {self.description} выбери ' \
                               f'{char_class_skill[self.char_class].values()} харатеристики из ' \
                               f'{list(char_class_skill[self.char_class].keys())}, которые с ' \
                               f'наибольшей вероятностью понадобятся этому персонажу во время игры. Ответ выдай ' \
                               f'в формате - ["характеристика", "характеристика"]'

        # ['acrobatics', 'stealth', 'sleight_of_hand', 'perception']
        bonus_skills = self.llm.invoke(choice_skills_prompt).content

        return bonus_skills

    def bonus_skills_selection(self, iter=int(env_vars.ITER)):
        for num_iter in range(iter):
            bonus_skills = self.bonus_skills_prompt()
            if RuleChecker.check_eval(bonus_skills):
                bonus_skills = eval(bonus_skills)
                if RuleChecker.check_num_and_correct_list(bonus_skills,
                                                          char_class_skill[self.char_class].values(),
                                                          list(char_class_skill[self.char_class].keys())):
                    return bonus_skills

        print('Подобрать bonus не удалось, повторите попытку создания')
        return quit()

    def get_skills(self):
        self.skills = Skills()
        all_skills = {
            'acrobatics': 'dexterity', 'animal_handling': 'wisdom', 'arcana': 'intelligence',
            'athletics': 'strength', 'deception': 'charisma', 'history': 'intelligence', 'insight': 'wisdom',
            'intimidation': 'charisma', 'investigation': 'intelligence', 'medicine': 'wisdom',
            'nature': 'intelligence', 'perception': 'wisdom', 'performance': 'charisma',
            'persuasion': 'charisma',
            'religion': 'intelligence', 'sleight_of_hand': 'dexterity', 'stealth': 'dexterity',
            'survival': 'wisdom'
        }

        bonus_skills = self.bonus_skills_selection()
        for skills_name in all_skills.keys():
            for bonus_skills_name in bonus_skills:
                value = getattr(self.abilities, '_' + all_skills[skills_name])
                if bonus_skills_name == skills_name:
                    setattr(self.skills, skills_name, value.value + 2)
                else:
                    setattr(self.skills, skills_name, value.value)

    def spell_prompt(self):
        spells_and_cantrips_for_class = {
            'Bard': (
                ['Dancing Lights', 'Light', 'Mage Hand', 'Mending', 'Message', 'Minor Illusion', 'Prestidigitation',
                 'True Strike', 'Vicious Mockery'],
                ['Animal Friendship', 'Bane', 'Charm Person', 'Comprehend Languages',
                 'Cure Wounds', 'Detect Magic', 'Disguise Self', 'Faerie Fire', 'Feather Fall', 'Healing Word',
                 'Heroism',
                 'Identify', 'Illusory Script', 'Longstrider', 'Silent Image', 'Sleep', 'Speak with Animals',
                 'Thunderwave', 'Unseen Servant']),
            'Cleric': (
                ["Guidance", "Light", "Mending", "Resistance", "Sacred Flame", "Spare the Dying", "Thaumaturgy"],
                ["Bane", "Bless", "Command", "Create or Destroy Water", "Cure Wounds", "Detect Evil and Good",
                 "Detect Magic", "Detect Poison and Disease", "Guiding Bolt", "Healing Word", "Inflict Wounds",
                 "Protection from Evil and Good", "Purify Food and Drink", "Sanctuary", "Shield of Faith"]),
            'Druid': (
                ["Druidcraft", "Guidance", "Mending", "Poison Spray", "Produce Flame", "Resistance", "Shillelagh"],
                ["Animal Friendship", "Charm Person", "Create or Destroy Water", "Cure Wounds", "Detect Magic",
                 "Detect Poison and Disease", "Entangle", "Faerie Fire", "Fog Cloud", "Goodberry", "Healing Word",
                 "Jump", "Longstrider", "Purify Food and Drink", "Speak with Animals", "Thunderwave"]),
            'Sorcerer': (
                ["Acid Splash", "Chill Touch", "Dancing Lights", "Fire Bolt", "Light", "Mage Hand",
                 "Mending", "Message", "Minor Illusion", "Poison Spray", "Prestidigitation", "Ray of Frost",
                 "Shocking Grasp",
                 "True Strike"],
                ["Burning Hands", "Charm Person", "Color Spray", "Comprehend Languages",
                 "Detect Magic", "Disguise Self", "Expeditious Retreat", "False Life", "Feather Fall",
                 "Fog Cloud",
                 "Jump", "Mage Armor", "Magic Missile", "Ray of Sickness", "Shield", "Silent Image", "Sleep"]),
            'Warlock': (
                ["Chill Touch", "Eldritch Blast", "Mage Hand", "Minor Illusion", "Poison Spray", "Prestidigitation",
                 "True Strike"],
                ["Charm Person", "Comprehend Languages", "Expeditious Retreat", "Hellish Rebuke", "Illusory Script",
                 "Protection from Evil and Good", "Unseen Servant"]),
            'Wizard': (
                ["Acid Splash", "Chill Touch", "Dancing Lights", "Fire Bolt", "Light", "Mage Hand", "Mending",
                 "Message",
                 "Minor Illusion", "Poison Spray", "Prestidigitation", "Ray of Frost", "Shocking Grasp", "True Strike"],
                ["Alarm", "Burning Hands", "Charm Person", "Color Spray", "Comprehend Languages", "Detect Magic",
                 "Disguise Self", "Expeditious Retreat", "False Life", "Feather Fall", "Fog Cloud", "Find Familiar",
                 "Grease", "Identify", "Illusory Script", "Jump", "Longstrider", "Mage Armor", "Magic Missile",
                 "Protection from Evil and Good", "Shield", "Silent Image", "Sleep", "Thunderwave", "Unseen Servant"])
        }
        num_cantrips_and_spells_for_class = {
            'Bard': [2, 4],
            'Cleric': [3, 2],
            'Druid': [2, 2],
            'Sorcerer': [4, 2],
            'Warlock': [2, 2],
            'Wizard': [3, 2]
        }
        if self.char_class in list(spells_and_cantrips_for_class.keys()):
            choice_spells_prompt = f"Для персонажа, с кратким описанием - {self.description}, выбери " \
                                   f"{num_cantrips_and_spells_for_class[self.char_class][0]} разных заговора из списка: " \
                                   f"{spells_and_cantrips_for_class[self.char_class][0]}, и " \
                                   f"{num_cantrips_and_spells_for_class[self.char_class][1]} разных заклинания из списка: " \
                                   f"{spells_and_cantrips_for_class[self.char_class][1]}. " \
                                   f"В ответ напиши только два списка через ';' вот так - " \
                                   f"['name', 'name']; ['name', 'name']"

            all_spells = self.llm.invoke(choice_spells_prompt).content

            return all_spells

    def spells_selection(self, iter=int(env_vars.ITER)):
        spells_and_cantrips_for_class = {
            'Bard': (
                ['Dancing Lights', 'Light', 'Mage Hand', 'Mending', 'Message', 'Minor Illusion', 'Prestidigitation',
                 'True Strike', 'Vicious Mockery'],
                ['Animal Friendship', 'Bane', 'Charm Person', 'Comprehend Languages',
                 'Cure Wounds', 'Detect Magic', 'Disguise Self', 'Faerie Fire', 'Feather Fall', 'Healing Word',
                 'Heroism',
                 'Identify', 'Illusory Script', 'Longstrider', 'Silent Image', 'Sleep', 'Speak with Animals',
                 'Thunderwave', 'Unseen Servant']),
            'Cleric': (
                ["Guidance", "Light", "Mending", "Resistance", "Sacred Flame", "Spare the Dying", "Thaumaturgy"],
                ["Bane", "Bless", "Command", "Create or Destroy Water", "Cure Wounds", "Detect Evil and Good",
                 "Detect Magic", "Detect Poison and Disease", "Guiding Bolt", "Healing Word", "Inflict Wounds",
                 "Protection from Evil and Good", "Purify Food and Drink", "Sanctuary", "Shield of Faith"]),
            'Druid': (
                ["Druidcraft", "Guidance", "Mending", "Poison Spray", "Produce Flame", "Resistance", "Shillelagh"],
                ["Animal Friendship", "Charm Person", "Create or Destroy Water", "Cure Wounds", "Detect Magic",
                 "Detect Poison and Disease", "Entangle", "Faerie Fire", "Fog Cloud", "Goodberry", "Healing Word",
                 "Jump", "Longstrider", "Purify Food and Drink", "Speak with Animals", "Thunderwave"]),
            'Sorcerer': (
                ["Acid Splash", "Chill Touch", "Dancing Lights", "Fire Bolt", "Light", "Mage Hand",
                 "Mending", "Message", "Minor Illusion", "Poison Spray", "Prestidigitation", "Ray of Frost",
                 "Shocking Grasp",
                 "True Strike"],
                ["Burning Hands", "Charm Person", "Color Spray", "Comprehend Languages",
                 "Detect Magic", "Disguise Self", "Expeditious Retreat", "False Life", "Feather Fall",
                 "Fog Cloud",
                 "Jump", "Mage Armor", "Magic Missile", "Ray of Sickness", "Shield", "Silent Image", "Sleep"]),
            'Warlock': (
                ["Chill Touch", "Eldritch Blast", "Mage Hand", "Minor Illusion", "Poison Spray", "Prestidigitation",
                 "True Strike"],
                ["Charm Person", "Comprehend Languages", "Expeditious Retreat", "Hellish Rebuke", "Illusory Script",
                 "Protection from Evil and Good", "Unseen Servant"]),
            'Wizard': (
                ["Acid Splash", "Chill Touch", "Dancing Lights", "Fire Bolt", "Light", "Mage Hand", "Mending",
                 "Message",
                 "Minor Illusion", "Poison Spray", "Prestidigitation", "Ray of Frost", "Shocking Grasp", "True Strike"],
                ["Alarm", "Burning Hands", "Charm Person", "Color Spray", "Comprehend Languages", "Detect Magic",
                 "Disguise Self", "Expeditious Retreat", "False Life", "Feather Fall", "Fog Cloud", "Find Familiar",
                 "Grease", "Identify", "Illusory Script", "Jump", "Longstrider", "Mage Armor", "Magic Missile",
                 "Protection from Evil and Good", "Shield", "Silent Image", "Sleep", "Thunderwave", "Unseen Servant"])
        }
        num_cantrips_and_spells_for_class = {
            'Bard': [2, 4],
            'Cleric': [3, 2],
            'Druid': [2, 2],
            'Sorcerer': [4, 2],
            'Warlock': [2, 2],
            'Wizard': [3, 2]
        }
        for num_iter in range(iter):
            cantrips_and_spells = self.spell_prompt().split('; ')
            cantrips = cantrips_and_spells[0]
            spells = cantrips_and_spells[1]
            if RuleChecker.check_eval(cantrips) and RuleChecker.check_eval(spells):
                cantrips = eval(cantrips)
                spells = eval(spells)
                if RuleChecker.check_num_and_correct_list(cantrips,
                                                          num_cantrips_and_spells_for_class[self.char_class][0],
                                                          spells_and_cantrips_for_class[self.char_class][0]) and \
                        RuleChecker.check_num_and_correct_list(spells,
                                                               num_cantrips_and_spells_for_class[self.char_class][1],
                                                               spells_and_cantrips_for_class[self.char_class][1]):
                    return cantrips + spells

        print('Подобрать spells не удалось, повторите попытку создания')
        return quit()

    def get_spells(self):
        for name in self.spells_selection():
            spell_inf = get_spell(name)
            self.spells.append(Spell(spell_inf[0], spell_inf[1], spell_inf[2], spell_inf[3], spell_inf[4],
                                     spell_inf[5], spell_inf[6], spell_inf[7], spell_inf[8]))


load_dotenv()

user_request = input('Введите краткое описание персонажа: ')
user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(
    user_request='маг',
    user_setting='киберпанк'
)

if char_build.description and char_build.char_class and char_build.char_race \
        and char_build.abilities and char_build.skills and char_build.spells and char_build.all_item is not None:
    print(f"Краткое описание персонажа: \n{char_build.description}\n"
          f"Класс персонажа: {char_build.char_class}\n"
          f"Расса персонажа: {char_build.char_race}\n"
          f"Абилки персонажа: {char_build.abilities}\n"
          f"Скилы персонажа: {char_build.skills}\n"
          f"Предметы персонажа: ")
    for object_item in char_build.all_item:
        print(object_item)
    print('Все спелы:')
    for all_inf in char_build.spells:
        print(all_inf)
