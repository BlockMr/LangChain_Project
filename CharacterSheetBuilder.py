import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from Character import Character


class CharacterSheetBuilder:
    def __init__(self, user_request, user_setting):
        self.user_request = user_request
        self.user_setting = user_setting
        self.llm = ChatOpenAI(openai_api_key=os.environ['API_KEY_OPENAI'])
        # self.character_sheet = Character(
        #     description=self.get_description()
        #
        # )

    def get_description(self):
        art_promt = f'Напиши краткое художественное описание внешности и одежды для персонажа' \
                    f'существующего в рамках сеттинга описываемого как {self.user_setting}' \
                    f' используя данное краткое описание: {self.user_request}'
        description = self.llm.invoke(art_promt).content

        return description

    # def get_ability_stats(self):
    #     stats_promt = f''


load_dotenv()

user_request = input('Введите краткое описание персонажа: ')
user_setting = input('Введите краткое описание сеттинга: ')

char_build = CharacterSheetBuilder(user_request, user_setting)
print(char_build.get_description())
