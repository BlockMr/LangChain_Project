import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from Character import Character


class CharacterSheetBuilder:
    def __init__(self, user_request):
        self.user_request = user_request
        self.llm = ChatOpenAI(openai_api_key=os.environ['API_KEY_OPENAI'])
        self.character_sheet = Character(
            description=self.get_description()

        )

    def get_description(self):
        art_description = f'Напиши краткое художественное описание для несуществующего персонажа' \
                          f' используя данный запрос {self.user_request}'
        description = self.llm.invoke(art_description)
        return description

    # def get_ability_stats(self):
    #     pass


load_dotenv()

user_request = input()


char_build = CharacterSheetBuilder(user_request)
print(char_build.character_sheet)
