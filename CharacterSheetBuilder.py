import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from Character import Character
from AbilityStats import AbilityStats
from Env_vars import env_vars


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
        abilities = AbilityStats()
        stats_prompt = f'для персонажа имеющего описание {self.get_description()} напиши силу харатеристик:' \
                       f'{", ".join(abilities.all_ability)}.'\
                       f'Характеристики могут принимать значение от 0 до 20, ответ выведи в формате:' \
                       '{strength: значение, dexterity: значение, constitution: значение, intelligence: значение, ' \
                       'wisdom: значение, charisma: значение}'

        raw_stats = eval(self.llm.invoke(stats_prompt).content)
        pass
        # if k != 0:
        #     for ability_name in abilities.all_ability:
        #         try:
        #             setattr(abilities, ability_name, raw_stats[ability_name])
        #         except KeyError:
        #             return self.get_ability_stats(k - 1)


load_dotenv()

user_request = input('Введите краткое описание персонажа: ')
user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(user_request, user_setting)
print(char_build.description)
# print(char_build.abilities)
