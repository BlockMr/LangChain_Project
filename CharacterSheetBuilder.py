from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from AbilityStats import AbilityStats, AbilityStat
from Character import char_class_skill, char_race_abil
from Env_vars import env_vars
from RuleChecker import RuleChecker
from Skills import Skills
from Utility import Utility
from db.db_methods import get_all_weapons_name, get_all_armors_name, get_all_gears_name
from db.db_methods import get_gear, get_armor, get_weapon, get_spell
from item import Armor as Ar
from item import Item as It
from item import Weapon as Wp
from spells.Spell import Spell


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
        self.creative_llm = ChatOpenAI(openai_api_key=env_vars.API_KEY_OPENAI, temperature=0.7)
        self.json_llm = ChatOpenAI(openai_api_key=env_vars.API_KEY_OPENAI, temperature=0)
        self.get_description()
        self.get_weapon()
        self.get_armor()
        self.get_gear()
        self.get_char_class_and_race()
        self.get_ability_stats()
        self.get_skills()
        self.get_spells()

    def get_description(self):
        prompt = (
            f"Создай краткое художественное описание (на английском языке) внешности и одежды персонажа, "
            f"который существует в рамках сеттинга: {self.user_setting}. "
            f"Используй следующее краткое описание персонажа: {self.user_request}. "
            f"Обрати внимание на все детали, указанные пользователем, и постарайся учесть их в описании. "
            f"Описание должно быть точным, атмосферным и соответствовать заданному сеттингу."
        )
        # prompt = (
        #     f"Для персонажа с этим описанием: {self.user_request}, создай художественное описание его внешности и одежды. "
        #     f"Персонаж существует в рамках сеттинга: {self.user_setting}. "
        #     f"Твоя задача — выделить ключевые детали из описания, такие как возраст, телосложение, выражение лица, "
        #     f"тип одежды и аксессуары, чтобы они подходили сеттингу и передавали атмосферу персонажа. "
        #     f"Убедись, что описание внешности является компактным, но детализированным, чтобы оно идеально подходило к его роли. "
        #     f"Не добавляй лишние выдуманные детали, но постарайся максимально раскрыть образ персонажа."
        # )
        description = self.creative_llm.invoke(prompt).content
        self.description = description

    def weapon_prompt(self):
        # prompt = (
        #     f"Для персонажа с описанием: {self.description}, выбери предметы строго из следующего списка.\n"
        #     f"\nСписок предметов с индексами:\n{Utility.generate_indexed_list(get_all_weapons_name())}"
        #     f"\nВыбор должен быть только из указанных предметов. Нельзя выбирать ничего, что не указано в списке. "
        #     f"Количество предметов должно соответствовать социальному статусу персонажа (богатство или бедность). "
        #     f"В ответ дай только список индексов выбранных предметов в формате: [index1, index2, index3]. "
        #     f"Больше в ответ ничего писать не нужно."
        # )

        prompt = (
            f"Подбери предметы для персонажа на основе его социального статуса (богатство или бедность) и краткого описания: {self.description}. "
            f"Выбирай предметы только из списка: {get_all_weapons_name()}. Не предлагай предметы, которых нет в этом списке. "
            f"Количество предметов должно соответствовать статусу персонажа."
            f"Ответь только названиями предметов в формате: [\"name\", \"name\", \"name\"]"
        )

        weapon_for_char = self.json_llm.invoke(prompt).content

        return weapon_for_char

    def weapon_selection(self, iter=int(env_vars.ITER)):
        all_weapons_name = get_all_weapons_name()
        for _ in range(iter):
            weapons_for_char = self.weapon_prompt()
            if RuleChecker.check_eval(weapons_for_char):
                fix_weapons = RuleChecker.deletion_of_excess(eval(weapons_for_char), all_weapons_name)
                if len(fix_weapons) != 0:
                    return fix_weapons

        print('Подобрать weapon не удалось, повторите попытку создания')
        return quit()

    def get_weapon(self):
        all_weapon_for_char = self.weapon_selection()
        for weapon_name in all_weapon_for_char:
            weapon_inf = get_weapon(weapon_name)
            self.all_item.append(Wp.Weapon(name=weapon_inf.name, price=weapon_inf.price, weight=weapon_inf.weight,
                                           damage_type=weapon_inf.damage_type, damage=weapon_inf.damage,
                                           properties=weapon_inf.properties, description=weapon_inf.description))

    def armor_prompt(self):
        prompt = (
            f"Подбери броню для персонажа на основе его описания: {self.description}. "
            f"Выбирай подходящие предметы только из списка: {get_all_armors_name()}. "
            f"Учитывай уровень достатка персонажа и задачи, которые он решает в своих приключениях. "
            f"Помни, что персонаж не сможет надеть более одного комплекта брони. "
            f"Ответь только названиями предметов в формате: [\"name\", \"name\", \"name\"]"
        )

        armor_for_char = self.json_llm.invoke(prompt).content

        return armor_for_char

    def armor_selection(self, iter=int(env_vars.ITER)):
        all_armors_name = get_all_armors_name()
        for _ in range(iter):
            armor_for_char = self.armor_prompt()
            if RuleChecker.check_eval(armor_for_char):
                fix_armor = RuleChecker.deletion_of_excess(eval(armor_for_char), all_armors_name)
                if len(fix_armor) != 0:
                    return fix_armor

        print('Подобрать armor не удалось, повторите попытку создания')
        return quit()

    def get_armor(self):
        all_armor_for_char = self.armor_selection()
        for armor_name in all_armor_for_char:
            armor_inf = get_armor(armor_name)
            self.all_item.append(Ar.Armor(name=armor_inf.name, price=armor_inf.price, weight=armor_inf.weight,
                                          armor_class=armor_inf.armor_class, strength=armor_inf.strength,
                                          stealth=armor_inf.stealth, armor_type=armor_inf.armor_type,
                                          description=armor_inf.description))

    def gear_prompt(self):
        prompt = (
            f"Подбери предметы для персонажа на основе его описания: {self.description}. "
            f"Выбирай только из списка: {get_all_gears_name()}, и подбирай предметы, подходящие по уровню достатка персонажа "
            f"и его задачам. Количество предметов также должно соответствовать его статусу. "
            f"Убедись, что все выбранные предметы 100% присутствуют в списке. "
            f"Ответь только названиями предметов в формате: [\"name\", \"name\", \"name\"]"
        )

        gear_for_char = self.json_llm.invoke(prompt).content

        return gear_for_char

    def gear_selection(self, iter=int(env_vars.ITER)):
        for _ in range(iter):
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
            self.all_item.append(It.Item(name=gear_inf.name, price=gear_inf.price,
                                         weight=gear_inf.weight, description=gear_inf.description))

    def char_class_and_race_prompt(self):
        prompt = (
            f"Для персонажа с описанием: {self.user_request} и сеттингом: {self.user_setting}, "
            f"выбери расу и класс строго из следующих списков.\n"
            f"\nСписок рас с индексами: \n{Utility.generate_indexed_list(char_race_abil.keys())}"
            f"\nСписок классов с индексами: \n{Utility.generate_indexed_list(char_class_skill.keys())}"
            f"\nВыборы должны быть только из этих списков. Нельзя выбирать ничего, что не указано здесь. "
            f"В ответ дай только список из индекса расы и индекса класса в таком формате: [index_race, index_class]. "
            f"Больше в ответ ничего писать не нужно."
        )

        char_race_class = self.json_llm.invoke(prompt).content

        return char_race_class

    def get_char_class_and_race(self, iter=int(env_vars.ITER)):
        for _ in range(iter):
            char_race_and_class = self.char_class_and_race_prompt()
            if RuleChecker.check_eval(char_race_and_class):
                char_race = list(char_race_abil.keys())[eval(char_race_and_class)[0]]
                char_class = list(char_class_skill.keys())[eval(char_race_and_class)[1]]
                if RuleChecker.check_char_and_race(char_race, char_class):
                    self.char_race = char_race
                    self.char_class = char_class
                    return

        print('Подобрать char_class_and_race не удалось, повторите попытку создания')
        return quit()

    def ability_stats_prompt(self):
        self.abilities = AbilityStats()

        stats_prompt = (
            f"Для персонажа с описанием: {self.description}, выбери значения следующих характеристик: "
            f"{', '.join(self.abilities.all_ability)}. "
            f"Характеристики могут принимать значения от 0 до 20. Пожалуйста, определяй значения характеристик, "
            f"основываясь на описании персонажа и его чертах. Если персонаж выглядит физически сильным, "
            f"увеличь значение силы, если он описан как ловкий — увеличь ловкость, если умный — интеллект, "
            f"и так далее. Учитывай любые упомянутые особенности или навыки из описания. "
            f"Ответ дай строго в формате: "
            f'{{"strength": значение, "dexterity": значение, "constitution": значение, '
            f'"intelligence": значение, "wisdom": значение, "charisma": значение}}.'
        )

        raw_stats = self.creative_llm.invoke(stats_prompt).content

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

    # TODO исправить генерацию для персонажей по типу Half-Elf, у них присутствует выбор в характеристиках

    def ability_stats_bonus_prompt_for_other_race(self):
        all_bonus = char_race_abil[self.char_race]
        # bonus_for_other_race_prompt = f'для персонажа имеющего описание {self.description} выбери 2 характеристики' \
        #                               f'которые более всего подходят для этого персонажа из списка ' \
        #                               f'{list(all_bonus.keys())[1]} в ответ напиши только список этих характеристик - ' \
        #                               f'["name", "name"]'

        bonus_for_other_race_prompt = (
            f"Для персонажа с описанием: {self.description}, выбери 2 характеристики, которые наиболее подходят "
            f"этому персонажу, основываясь на его чертах, навыках или поведении, указанном в описании. "
            f"Характеристики выбирай только из следующего списка: {list(all_bonus.keys())[1]}. "
            f"Постарайся учитывать все детали, указанные в описании, и выбери те характеристики, которые лучше всего "
            f"отражают суть персонажа. "
            f"Ответ дай строго в формате списка: [\"name\", \"name\"]. Ничего больше добавлять не нужно."
        )

        bonus = self.json_llm.invoke(bonus_for_other_race_prompt).content

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
        choice_skills_prompt = (
            f"Для персонажа с описанием: {self.description}, выбери {char_class_skill[self.char_class].values()} "
            f"характеристики из следующего списка: {list(char_class_skill[self.char_class].keys())}. "
            f"Выбирай те характеристики, которые с наибольшей вероятностью понадобятся этому персонажу в ходе игры, "
            f"учитывая его описание и предполагаемые действия. "
            f"Ответ дай строго в формате: [\"name\", \"name\", \"name\"]. Ничего больше добавлять не нужно."
        )

        # ['acrobatics', 'stealth', 'sleight_of_hand', 'perception']
        bonus_skills = self.json_llm.invoke(choice_skills_prompt).content

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

    # TODO посоветоваться с Андреем на счет (372) if self.char_class in list(spells_and_cantrips_for_class.keys()):, есть ли смысл запускать функцию, если чел не маг

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
        # choice_spells_prompt = f"Для персонажа, с кратким описанием - {self.description}, выбери " \
        #                        f"{num_cantrips_and_spells_for_class[self.char_class][0]} разных заговора из списка: " \
        #                        f"{spells_and_cantrips_for_class[self.char_class][0]}, и " \
        #                        f"{num_cantrips_and_spells_for_class[self.char_class][1]} разных заклинания из списка: " \
        #                        f"{spells_and_cantrips_for_class[self.char_class][1]}. " \
        #                        f"В ответ напиши только два списка через ';' вот так - " \
        #                        f"['name', 'name']; ['name', 'name']"

        choice_spells_prompt = (
            f"Для персонажа с кратким описанием: {self.description}, выбери "
            f"{num_cantrips_and_spells_for_class[self.char_class][0]} различных заговора из следующего списка: "
            f"{spells_and_cantrips_for_class[self.char_class][0]} и "
            f"{num_cantrips_and_spells_for_class[self.char_class][1]} различных заклинания из следующего списка: "
            f"{spells_and_cantrips_for_class[self.char_class][1]}. "
            f"Выбирай заклинания, которые лучше всего подходят для персонажа, учитывая его описание и возможный стиль игры. "
            f"Ответ дай строго в формате двух списков через точку с запятой: ['name', 'name']; ['name', 'name'] "
            f"Не добавляй ничего лишнего."
        )

        all_spells = self.json_llm.invoke(choice_spells_prompt).content

        return all_spells

    def spells_selection(self, iter=int(env_vars.ITER) - 1):
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
        kostyl = ['Bard', 'Cleric', 'Druid', 'Sorcerer', 'Warlock', 'Wizard']
        if self.char_class in kostyl:
            for name in self.spells_selection():
                spell_inf = get_spell(name)
                self.spells.append(Spell(name=spell_inf.name, level=spell_inf.level, cast_time=spell_inf.cast_time,
                                         duration=spell_inf.duration, school=spell_inf.school,
                                         range_area=spell_inf.range_area, attack_save=spell_inf.attack_save,
                                         components=spell_inf.components, description=spell_inf.description))


load_dotenv()

# user_request = input('Введите краткое описание персонажа: ')
# user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(
    user_request='Саша футболист',
    user_setting='классическое фентези'
)

if char_build.description and char_build.char_class and char_build.char_race \
        and char_build.abilities and char_build.skills is not None:
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
