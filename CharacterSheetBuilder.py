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
                return self.get_weapon(k - 1)
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
                return self.get_armor(k - 1)
        else:
            return 'Произошла ошибка, повторите пожалуйста запрос'

    def gear_selection(self):
        # selection_prompt = f'Для персонажа существующего в рамках сеттинг - {self.user_setting}, ' \
        #                    f'краткого описания {self.user_request}, выбери предметы из списка {list(it.all_gear.keys())}' \
        #                    f'Выбирая опирайся на его богатство или бедность, и количество предметов' \
        #                    f'тоже сопоставь персонажу. В ответ напиши только список в таком формате:' \
        #                    f'["name", "name"], name должно быть напсиано в точности так же как и в ' \
        #                    f'{list(it.all_gear.keys())}'

        selection_prompt = f'Для персонажа имеющего краткое описание {self.description}, выбери только из списка ' \
                           f'{list(it.all_gear.keys())} предметы, опираясь на его богатство или бедность, ' \
                           f'количетсво предметов тоже сопоставь персонажу. Вот так дай ответ - ["name", "name"], ' \
                           f'name возми в точности из списка {list(it.all_gear.keys())}.' \
                           f'Еще раз убедись пожалуйста в том, что предметы или предмет, который ты выбрал, 100% ' \
                           f'находится в списке {list(it.all_gear.keys())}, если нет, то выберай только из него, ' \
                           f'пожалуйста'

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
        self.char_race = char_race_class[0]
        self.char_class = char_race_class[1]

    def get_ability_stats(self, k=env_vars.ITER):
        self.abilities = AbilityStats()
        stats_prompt = f'для персонажа имеющего описание {self.description} напиши значение харатеристик:' \
                       f'{", ".join(self.abilities.all_ability)}.' \
                       f'Характеристики могут принимать значение от 0 до 20, ответ выведи в формате:' \
                       '{"strength": значение, "dexterity": значение, "constitution": значение,' \
                       ' "intelligence": значение, "wisdom": значение, "charisma": значение}'
        raw_stats = eval(self.llm.invoke(stats_prompt).content)
        bonus = char.char_race_abil[self.char_race]

        # прописать отдельно для эльфа
        if k != 0 and self.char_race != 'Half-Elf':
            for ability_name in self.abilities.all_ability:
                for bonus_name in bonus:
                    try:
                        stat = AbilityStat()
                        if ability_name == bonus_name:
                            stat.value = raw_stats[ability_name] + bonus[ability_name]
                            setattr(self.abilities, '_' + ability_name, stat)
                        else:
                            stat.value = raw_stats[ability_name]
                            setattr(self.abilities, '_' + ability_name, stat)
                    except KeyError or SyntaxError:
                        return self.get_ability_stats(k - 1)
        else:
            return 'Произошла ошибка, повторите пожалуйста запрос'

    def get_skills(self, k=env_vars.ITER):
        self.skills = Skills()
        choice_skills_prompt = f'Для персонажа, имеющего описание {self.description}, класс которого - ' \
                               f'{self.char_class}, а расса - {self.char_race}, выбери ' \
                               f'{char.char_class_skill[self.char_class].values()} харатеристики из ' \
                               f'{list(char.char_class_skill[self.char_class].keys())}, которые с ' \
                               f'наибольшей вероятностью понадобятся этому персонажу во время игры. Ответ выдай ' \
                               f'в формате - ["характеристика", "характеристика"]'
        bonus_skills = eval(self.llm.invoke(choice_skills_prompt).content)
        print(self.abilities)
        # ['acrobatics', 'stealth', 'sleight_of_hand', 'perception']
        if k != 0:
            try:
                for skills_name in self.skills.all_skills.keys():
                    for bonus_skills_name in bonus_skills:
                        value = getattr(self.abilities, '_' + self.skills.all_skills[skills_name])
                        if bonus_skills_name == skills_name:
                            setattr(self.skills, skills_name, value.value + 2)
                        else:
                            setattr(self.skills, skills_name, value.value)
            except Exception:
                return self.get_skills(k - 1)
        else:
            return 'Произошла ошибка, повторите запрос еще раз'


load_dotenv()

# user_request = input('Введите краткое описание персонажа: ')
# user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(
    user_request='король Артур - хозяин камелота',
    user_setting='придумай сам'
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
