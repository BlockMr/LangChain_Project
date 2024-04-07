from dataclasses import dataclass


class Skills:
    acrobatics: int
    animal_handling: int
    arcana: int
    athletics: int
    deception: int
    history: int
    insight: int
    intimidation: int
    investigation: int
    medicine: int
    nature: int
    perception: int
    perfomance: int
    persuasion: int
    religion: int
    sleight_of_hand: int
    stealth: int
    survival: int

    def __str__(self):
        all_skills = {'acrobatics': 'dexterity', 'animal_handling': 'wisdom', 'arcana': 'intelligence',
                      'athletics': 'strength', 'deception': 'charisma', 'history': 'intelligence', 'insight': 'wisdom',
                      'intimidation': 'charisma', 'investigation': 'intelligence', 'medicine': 'wisdom',
                      'nature': 'intelligence', 'perception': 'wisdom', 'performance': 'charisma',
                      'persuasion': 'charisma',
                      'religion': 'intelligence', 'sleight_of_hand': 'dexterity', 'stealth': 'dexterity',
                      'survival': 'wisdom'}
        skills_str = []
        for skill in all_skills:
            skills_str.append(f'{skill}: {getattr(self, skill)}')
        return f"{' ,'.join(skills_str)}"

