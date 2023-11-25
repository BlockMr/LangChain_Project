import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from Character import Character
from AbilityStats import AbilityStat, AbilityStats


class CharacterSheetBuilder:
    def __init__(self, user_request, user_setting):
        self.user_request = user_request
        self.user_setting = user_setting
        self.ability_stats = {}
        self.llm = ChatOpenAI(openai_api_key=os.environ['API_KEY_OPENAI'])
        self.character_sheet = Character(
            description=self.get_description(),
            abilities=AbilityStats(
                strength=AbilityStat(self.ability_stats['strength'][0], self.ability_stats['strength'][1]),
                dexterity=AbilityStat(self.ability_stats['dexterity'][0], self.ability_stats['dexterity'][1]),
                constitution=AbilityStat(self.ability_stats['constitution'][0], self.ability_stats['constitution'][1]),
                intelligence=AbilityStat(self.ability_stats['intelligence'][0], self.ability_stats['intelligence'][1]),
                wisdom=AbilityStat(self.ability_stats['wisdom'][0], self.ability_stats['wisdom'][1]),
                charisma=AbilityStat(self.ability_stats['charisma'][0], self.ability_stats['charisma'][1])
            )
        )

    def get_description(self):
        art_prompt = f'Напиши краткое художественное описание внешности и одежды для персонажа' \
                    f'существующего в рамках сеттинга описываемого как {self.user_setting}' \
                    f' используя данное краткое описание: {self.user_request}'
        description = self.llm.invoke(art_prompt).content

        return description

    def get_ability_stats(self):
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
                self.ability_stats[str_prompt[0]] = str_prompt[1]
            return self.ability_stats

        else:
            self.get_ability_stats()


load_dotenv()

user_request = input('Введите краткое описание персонажа: ')
user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(user_request, user_setting)
print(char_build.get_description())
char_build.get_ability_stats()

