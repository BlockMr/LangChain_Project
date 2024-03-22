from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from Character import Character as char
from AbilityStats import AbilityStats, AbilityStat
from Env_vars import env_vars
from item import Weapon as wp
from item import Armor as ar
from item import Item as it
from Skills import Skills


class CharacterSheetBuilder:
    abilities: AbilityStats = None
    description: str = None
    all_item: list = []
    char_class: str = None
    char_race: str = None
    skills: Skills = None

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

    def get_description(self):
        art_prompt = f'Напиши краткое художественное описание внешности и одежды для персонажа' \
                     f'существующего в рамках сеттинга описываемого как {self.user_setting}' \
                     f' используя данное краткое описание: {self.user_request}'
        description = self.llm.invoke(art_prompt).content
        self.description = description

    def weapon_prompt(self):
        selection_prompt = f'Напиши предметы которые подходят к персонажу опираясь на его богатство или бедность,' \
                           f'и краткое описание - {self.description}, ' \
                           f'а выбери предметы пожалуйста только из этого списка - {wp.all_weapon}. Не из этого списка' \
                           f'предметы не предлагай' \
                           f'Их количество тоже нужно сопоставить персонажу.' \
                           f'В ответ дай только названия этих предметов списоком по типу [name, name, name]'

        weapon_for_char = eval(self.llm.invoke(selection_prompt).content)

        return weapon_for_char

    def weapon_selection(self, iter=int(env_vars.ITER)):
        all_weapon = self.weapon_prompt()

        for name in all_weapon:
            if name not in wp.all_weapon:
                all_weapon.remove(name)

        for num_iter in range(iter):
            if len(all_weapon) == 0:
                all_weapon = self.weapon_prompt()
                for name in all_weapon:
                    if name not in wp.all_weapon:
                        all_weapon.remove(name)
                if len(all_weapon) != 0:
                    return all_weapon
                else:
                    continue

        if len(all_weapon) == 0:
            return 'Подобрать Weapon не удалось', quit()
        else:
            return all_weapon

    def get_weapon(self):
        for weapon_name in self.weapon_selection():
            all_select = wp.all_weapon[weapon_name]
            self.all_item.append(wp.Weapon(weapon_name, all_select[0], all_select[1],
                                           all_select[3], all_select[2], all_select[4], all_select[5]))

    def armor_prompt(self):
        selection_prompt = f'Для персонажа с кратким описанием - {self.description},' \
                           f' выбери предметы из списка {ar.all_armor}.' \
                           f'постарайся выбрать предметы подходящие персонажу по уровню достатка и тем задачам,' \
                           f' которые он может решать в ходе своих приключений. учти, что надеть два комплекта брони' \
                           f' на себя он не сможет. Щит давай персонажу, только если он ему правда необходим и ' \
                           f'подходит по краткому описанию, а так же сеттингу. ' \
                           f'у персонажа может быть как один предмет, так и несколько.' \
                           f' в твет напиши только названия предметов в ковычках и в []'

        armor_for_char = eval(self.llm.invoke(selection_prompt).content)

        return armor_for_char

    def armor_selection(self, iter=int(env_vars.ITER)):
        all_armor = self.armor_prompt()

        for name in all_armor:
            if name not in ar.all_armor:
                all_armor.remove(name)

        for num_iter in range(iter):
            if len(all_armor) == 0:
                all_armor = self.armor_prompt()
                for name in all_armor:
                    if name not in ar.all_armor:
                        all_armor.remove(name)
                if len(all_armor) != 0:
                    return all_armor
                else:
                    continue

        if len(all_armor) == 0:
            return 'Подобрать Armor не удалось', quit()
        else:
            return all_armor

    def get_armor(self):
        for armor_name in self.armor_selection():
            all_select = ar.all_armor[armor_name]
            self.all_item.append(ar.Armor(armor_name, all_select[0], all_select[1],
                                          all_select[2], all_select[4], all_select[5],
                                          all_select[3], all_select[6]))

    def gear_prompt(self):
        selection_prompt = f'Для персонажа имеющего краткое описание {self.description}, выбери только из списка ' \
                           f'{list(it.all_gear.keys())} предметы, опираясь на его богатство или бедность, ' \
                           f'количетсво предметов тоже сопоставь персонажу. Вот так дай ответ - ["name", "name"], ' \
                           f'name возми в точности из списка {list(it.all_gear.keys())}.' \
                           f'Еще раз убедись пожалуйста в том, что предметы или предмет, который ты выбрал, 100% ' \
                           f'находится в списке {list(it.all_gear.keys())}, если нет, то выберай только из него, ' \
                           f'пожалуйста'

        gear_for_char = eval(self.llm.invoke(selection_prompt).content)

        return gear_for_char

    def gear_selection(self, iter=int(env_vars.ITER)):
        all_gear = self.gear_prompt()

        for name in all_gear:
            if name not in it.all_gear:
                all_gear.remove(name)

        for num_iter in range(iter):
            if len(all_gear) == 0:
                all_gear = self.gear_prompt()
                for name in all_gear:
                    if name not in it.all_gear:
                        all_gear.remove(name)
                if len(all_gear) != 0:
                    return all_gear
                else:
                    continue

        if len(all_gear) == 0:
            return 'Подобрать Gear не удалось', quit()
        else:
            return all_gear

    def get_gear(self):
        for gear_name in self.gear_selection():
            all_select = it.all_gear[gear_name]
            self.all_item.append(it.Item(gear_name, all_select[0], all_select[1], all_select[2]))

    def char_class_race_prompt(self):
        all_prompt = f'Выбери для персонажа, с кратким описание - {self.user_request} и находящегося в рамках' \
                     f'сеттинга - {self.user_setting}, расу из списка {char.char_race_abil.keys()}' \
                     f' и класс из списка {char.char_class_skill.keys()}, ответ дай в таком формате: ["race", "class"]'

        char_race_class = eval(self.llm.invoke(all_prompt).content)

        return char_race_class

    def get_char_class_race(self, iter=int(env_vars.ITER)):
        race_and_class = self.char_class_race_prompt()

        if race_and_class[0] not in char.char_race_abil or race_and_class[1] not in char.char_class_skill:
            for num_iter in range(iter):
                race_and_class = self.char_class_race_prompt()
                if race_and_class[0] in char.char_race_abil or race_and_class[1] in char.char_class_skill:
                    self.char_race = race_and_class[0]
                    self.char_class = race_and_class[1]
                else:
                    continue
        else:
            self.char_race = race_and_class[0]
            self.char_class = race_and_class[1]

    def ability_stats_prompt(self):
        self.abilities = AbilityStats()
        stats_prompt = f'для персонажа имеющего описание {self.description} напиши значение харатеристик:' \
                       f'{", ".join(self.abilities.all_ability)}.' \
                       f'Характеристики могут принимать значение от 0 до 20. В ответ пожалуйста дай только список' \
                       f'в таком формате:' \
                       '{"strength": значение, "dexterity": значение, "constitution": значение,' \
                       ' "intelligence": значение, "wisdom": значение, "charisma": значение}'

        raw_stats = eval(self.llm.invoke(stats_prompt).content)

        if self.char_race == 'Half-Elf':
            all_bonus = char.char_race_abil[self.char_race]
            bonus_for_Half_Elf_prompt = f'для персонажа имеющего описание {self.description} выбери 2 характеристики' \
                                        f'которые более всего подходят для этого персонажа из списка ' \
                                        f'{list(all_bonus.keys())[1]} в ответ напиши только список этих характеристик - ' \
                                        f'["name", "name"]'
            bonus = eval(self.llm.invoke(bonus_for_Half_Elf_prompt).content)
        else:
            bonus = char.char_race_abil[self.char_race]

        return raw_stats, bonus

    def ability_stats_selection(self, iter=int(env_vars.ITER)):
        stats = self.ability_stats_prompt()
        raw_stats = stats[0]
        bonus = stats[1]
        all_bonus = char.char_race_abil[self.char_race]
        count_bonus = 0

        # проверка статов
        if len(raw_stats) != 6:
            for num_iter in range(iter):
                stats = self.ability_stats_prompt()
                print(stats)
                raw_stats = stats[0]
                if len(raw_stats) != 6:
                    continue
                else:
                    break

        # проверка бонусов
        for key in range(len(list(all_bonus.keys()))):
            for name_bonus in bonus:
                if name_bonus in list(all_bonus.keys())[key]:
                    count_bonus += 1
        if count_bonus < len(bonus):
            for num_iter in range(iter):
                stats = self.ability_stats_prompt()
                bonus = stats[1]
                count_bonus = 0
                for bonus_name in bonus:
                    if bonus_name in all_bonus:
                        count_bonus += 1
                if count_bonus == len(bonus):
                    break
                else:
                    continue

        if count_bonus != len(bonus) or len(raw_stats) != 6:
            return 'Ошибка при создании AbilityStats', quit()
        else:
            return stats

    def get_ability_stats(self):
        self.abilities = AbilityStats()
        stats = self.ability_stats_selection()
        raw_stats = stats[0]
        bonus = stats[1]

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
        self.skills = Skills()
        choice_skills_prompt = f'Для персонажа, имеющего описание {self.description} выбери ' \
                               f'{char.char_class_skill[self.char_class].values()} харатеристики из ' \
                               f'{list(char.char_class_skill[self.char_class].keys())}, которые с ' \
                               f'наибольшей вероятностью понадобятся этому персонажу во время игры. Ответ выдай ' \
                               f'в формате - ["характеристика", "характеристика"]'

        # ['acrobatics', 'stealth', 'sleight_of_hand', 'perception']
        bonus_skills = eval(self.llm.invoke(choice_skills_prompt).content)

        for name_bonus_skills in bonus_skills:
            if name_bonus_skills not in list(char.char_class_skill[self.char_class].keys()):
                bonus_skills.remove(name_bonus_skills)

        return bonus_skills

    def bonus_skills_selection(self, iter=int(env_vars.ITER)):
        bonus_skills = self.bonus_skills_prompt()

        if len(bonus_skills) == 0:
            for num_iter in range(iter):
                bonus_skills = self.bonus_skills_prompt()
                if len(bonus_skills) != 0:
                    return bonus_skills
                else:
                    continue

        if len(bonus_skills) == 0:
            return 'Подобрать Gear не удалось', quit()
        else:
            return bonus_skills

    def get_skills(self):
        self.skills = Skills()
        bonus_skills = self.bonus_skills_selection()
        for skills_name in self.skills.all_skills.keys():
            for bonus_skills_name in bonus_skills:
                value = getattr(self.abilities, '_' + self.skills.all_skills[skills_name])
                if bonus_skills_name == skills_name:
                    setattr(self.skills, skills_name, value.value + 2)
                else:
                    setattr(self.skills, skills_name, value.value)


load_dotenv()

# user_request = input('Введите краткое описание персонажа: ')
# user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(
    user_request='Аватар маг',
    user_setting='История игрушек'
)
if char_build.description and char_build.char_class and char_build.char_race \
        and char_build.abilities and char_build.skills and char_build.all_item is not None:
    print(f"Краткое описание персонажа: \n{char_build.description}\n"
          f"Класс персонажа: {char_build.char_class}\n"
          f"Расса персонажа: {char_build.char_race}\n"
          f"Абилки персонажа: {char_build.abilities}\n"
          f"Скилы персонажа: {char_build.skills}\n"
          f"Предметы персонажа: ")
    for object_item in char_build.all_item:
        print(object_item)

