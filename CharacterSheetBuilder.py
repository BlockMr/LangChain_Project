import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from Character import Character
from AbilityStats import AbilityStat, AbilityStats


class CharacterSheetBuilder:
    def __init__(self, user_request, user_setting):
        self.user_request = user_request
        self.user_setting = user_setting
        self.llm = ChatOpenAI(openai_api_key=os.environ['API_KEY_OPENAI'])
        self.description = self.get_description()
        self.abilities = self.get_ability_stats()

    def get_description(self):
        art_prompt = f'Напиши краткое художественное описание внешности и одежды для персонажа' \
                    f'существующего в рамках сеттинга описываемого как {self.user_setting}' \
                    f' используя данное краткое описание: {self.user_request}'
        description = self.llm.invoke(art_prompt).content

        return description

    def get_ability_stats(self):
        ability_stats = {}
        stats_prompt = f'для персонажа имеющего описание {self .get_description()} напиши силу харатеристик:' \
                       f'strength, dexterity, const, intell, wisdom, charisma.'\
                       f'Характеристики могут принимать значение от 0 до 20, ответ выведи в формате:' \
                       f'strength = значение' \
                       f'dexterity = значение' \
                       f'и так далее.'

        stats = self.llm.invoke(stats_prompt).content.split('\n')

        if len(stats) == 6:
            for i in range(6):
                str_prompt = stats[i].split('=')
                value = int(str_prompt[1][1:])
                bonus = (value - 10) // 2
                ability_stats[str_prompt[0][:-1]] = [value, bonus]
        else:
            self.get_ability_stats()

        abilities = AbilityStats(
            strength=AbilityStat(ability_stats['strength'][0], ability_stats['strength'][1]),
            dexterity=AbilityStat(ability_stats['dexterity'][0], ability_stats['dexterity'][1]),
            constitution=AbilityStat(ability_stats['constitution'][0], ability_stats['constitution'][1]),
            intelligence=AbilityStat(ability_stats['intelligence'][0], ability_stats['intelligence'][1]),
            wisdom=AbilityStat(ability_stats['wisdom'][0], ability_stats['wisdom'][1]),
            charisma=AbilityStat(ability_stats['charisma'][0], ability_stats['charisma'][1]))
        return abilities


load_dotenv()

user_request = input('Введите краткое описание персонажа: ')
user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(user_request, user_setting)
print(char_build.get_description())
print(char_build.get_ability_stats())

