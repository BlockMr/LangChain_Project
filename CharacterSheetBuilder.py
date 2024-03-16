import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from Character import Character as char
from AbilityStats import AbilityStats, AbilityStat
from Env_vars import env_vars
from item import Weapon as wp
from item import Armor as ar
from item import Item as it


class CharacterSheetBuilder:
    abilities: AbilityStats = None
    description: str = None
    all_item: list = []
    char_class: str = None
    race: str = None

    def __init__(self, user_request, user_setting):
        self.user_request = user_request
        self.user_setting = user_setting
        self.llm = ChatOpenAI(openai_api_key=env_vars.API_KEY_OPENAI)
        self.get_description()
        # self.get_weapon()
        # self.get_armor()
        # self.get_gear()
        self.get_char_class_race()
        self.get_ability_stats()

    def get_description(self):
        art_prompt = f'Напиши краткое художественное описание внешности и одежды для персонажа' \
                     f'существующего в рамках сеттинга описываемого как {self.user_setting}' \
                     f' используя данное краткое описание: {self.user_request}'
        description = self.llm.invoke(art_prompt).content
        self.description = description

    def weapon_selection(self):
        selection_prompt = f'Напиши предметы которые подходят к персонажу опираясь на его богатство или бедность,' \
                           f'сеттинг - {self.user_setting}, краткое описание - {self.user_request}, ' \
                           f'а выбери предметы из этого списка - {wp.all_weapon}.' \
                           f'Их количество тоже нужно сопоставить персонажу.' \
                           f'В ответ дай только названия этих предметов списоком по типу [name, name, name]'

        weapon_for_char = self.llm.invoke(selection_prompt).content
        return eval(weapon_for_char)

    def get_weapon(self, k=env_vars.ITER):
        if k != 0:
            try:
                for weapon_name in self.weapon_selection():
                    all_select = wp.all_weapon[weapon_name]
                    self.all_item.append(wp.Weapon(weapon_name, all_select[0], all_select[1],
                                                   all_select[3], all_select[2], all_select[4], all_select[5]))
            except IndexError or SyntaxError:
                return self.get_weapon(k-1)
        else:
            return 'Произошла ошибка, повторите пожалуйста запрос'

    def armor_selection(self):
        selection_prompt = f'Для персонажа существующего в рамках сеттинг - {self.user_setting}, ' \
                           f'краткое описание - {self.user_request}, выбери предметы из списка {ar.all_armor}.' \
                           f'постарайся выбрать предметы подходящие персонажу по уровню достатка и тем задачам,' \
                           f' которые он может решать в ходе своих приключений. учти, что надеть два комплекта брони' \
                           f' на себя он не сможет. Щит давай персонажу, только если он ему правда необходим и ' \
                           f'подходит по краткому описанию, а так же сеттингу. ' \
                           f'у персонажа может быть как один предмет, так и несколько.' \
                           f' в твет напиши только названия предметов в ковычках и в []'

        armor_for_char = self.llm.invoke(selection_prompt).content
        return eval(armor_for_char)

    def get_armor(self, k=env_vars.ITER):
        if k != 0:
            try:
                for armor_name in self.armor_selection():
                    all_select = ar.all_armor[armor_name]
                    self.all_item.append(ar.Armor(armor_name, all_select[0], all_select[1],
                                                  all_select[2], all_select[4], all_select[5],
                                                  all_select[3], all_select[6]))
            except IndexError or SyntaxError:
                return self.get_armor(k-1)
        else:
            return 'Произошла ошибка, повторите пожалуйста запрос'

    def gear_selection(self):
        selection_prompt = f'Для персонажа существующего в рамках сеттинг - {self.user_setting}, ' \
                           f'краткого описания {self.user_request}, выбери предметы из списка {it.all_gear}' \
                           f'Выбирая опирайся на его богатство или бедность, и количество предметов' \
                           f'тоже сопоставь персонажу. В ответ выдай в таком формате: [name, name].'

        gear_for_char = self.llm.invoke(selection_prompt).content
        return eval(gear_for_char)

    def get_gear(self, k=env_vars.ITER):
        if k != 0:
            try:
                for gear_name in self.gear_selection():
                    all_select = it.all_gear[gear_name]
                    self.all_item.append(it.Item(gear_name, all_select[0], all_select[1], all_select[2]))
            except IndexError or SyntaxError:
                return self.get_gear(k - 1)
        else:
            return 'Произошла ошибка, повторите пожалуйста запрос'

    def get_char_class_race(self, k=env_vars.ITER):
        all_prompt = f'Выбери для персонажа, с кратким описание - {self.user_request} и находящегося в рамках' \
                     f'сеттинга - {self.user_setting}, расу из списка {char.char_race_abil.keys()}' \
                     f' и класс из списка {char.char_class_skill.keys()}, ответ дай в таком формате: ["race", "class"]'

        char_race_class = eval(self.llm.invoke(all_prompt).content)
        self.race = char_race_class[0]
        self.char_class = char_race_class[1]

    def get_ability_stats(self, k=env_vars.ITER):
        self.abilities = AbilityStats()
        stats_prompt = f'для персонажа имеющего описание {self.description} напиши значение харатеристик:' \
                       f'{", ".join(self.abilities.all_ability)}.' \
                       f'Характеристики могут принимать значение от 0 до 20, ответ выведи в формате:' \
                       '{"strength": значение, "dexterity": значение, "constitution": значение,' \
                       ' "intelligence": значение, "wisdom": значение, "charisma": значение}'

        raw_stats = eval(self.llm.invoke(stats_prompt).content)
        bonus = char.char_race_abil[self.race]
        print(raw_stats)
        print(bonus)

        if k != 0:
            for ability_name in self.abilities.all_ability:
                for bonus_name in bonus:
                    if ability_name == bonus_name:
                        try:
                            stat = AbilityStat()
                            stat.value = raw_stats[ability_name] + bonus[ability_name]
                            setattr(self.abilities, '_' + ability_name, stat)
                        except KeyError or SyntaxError:
                            return self.get_ability_stats(k - 1)
                stat = AbilityStat()
                stat.value = raw_stats[ability_name]
                setattr(self.abilities, '_' + ability_name, stat)
        else:
            return 'Произошла ошибка, повторите пожалуйста запрос'


load_dotenv()

# user_request = input('Введите краткое описание персонажа: ')
# user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(
    user_request='мальчик томас - малолетний воришка из нижней части города. не самый искусный вор, зато мелкий'
                 ' и юркий, что помогает ему выходить сухим из воды',
    user_setting='киберпанк'
)
# print(char_build.description + '\n')
# print(char_build.armor_selection())
# for object_item in char_build.all_item:
#     print(object_item)
print(char_build.abilities)
