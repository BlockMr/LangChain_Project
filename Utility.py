class Utility:
    @classmethod
    def generate_indexed_list(cls, items: list):
        """
        Генерирует строку с индексами и элементами items.
        Вывод:
        0. item[0]
        1. item[1]
        """
        indexed_list = ''
        for index, race in enumerate(items):
            indexed_list += f"{index}. {race}\n"
        return indexed_list
