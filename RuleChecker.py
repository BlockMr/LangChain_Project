from Character import char_race_abil, char_class_skill
from db.db_methods import get_all_weapons_name


class RuleChecker:
    @classmethod
    def deletion_of_excess(cls, check_list: list, all_name_list: list):
        fix_list = []
        for name in check_list:
            if name in all_name_list:
                fix_list.append(name)

        return fix_list

    @classmethod
    def check_char_and_race(cls, race_and_class: list):
        if race_and_class[0] not in char_race_abil or race_and_class[1] not in char_class_skill:
            return False

        return True

    @classmethod
    def check_ability_stats_bonus(cls, bonus: list, char_race: str):
        all_bonus = char_race_abil[char_race]
        count_bonus = 0
        for key in range(len(list(all_bonus.keys()))):
            for name_bonus in bonus:
                if name_bonus in list(all_bonus.keys())[key]:
                    count_bonus += 1

        if count_bonus == len(bonus):
            return True
        else:
            return False

    @classmethod
    def check_eval(cls, check_res):
        try:
            check_res = eval(check_res)
        except SyntaxError:
            return False
        return True

    @classmethod
    def check_num_and_correct_list(cls, check_list: list, num: int, all_list: list):
        correct = True
        if len(check_list) == num:
            for name in check_list:
                if name not in all_list:
                    correct = False

        return correct
