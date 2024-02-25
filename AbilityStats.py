class AbilityStat:
    _bonus: int
    _value: int

    @property
    def value(self):
        return self._value

    @property
    def bonus(self):
        return self._bonus

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._bonus = (new_value - 10) // 2


class AbilityStats:
    _strength: AbilityStat = AbilityStat()
    _dexterity: AbilityStat = AbilityStat()
    _constitution: AbilityStat = AbilityStat()
    _intelligence: AbilityStat = AbilityStat()
    _wisdom: AbilityStat = AbilityStat()
    _charisma: AbilityStat = AbilityStat()
    all_ability = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, new_value):
        self._strength.value = new_value

    @property
    def dexterity(self):
        return self._dexterity

    @dexterity.setter
    def dexterity(self, new_value):
        self._dexterity.value = new_value

    @property
    def constitution(self):
        return self._constitution

    @constitution.setter
    def constitution(self, new_value):
        self._constitution.value = new_value

    @property
    def intelligence(self):
        return self._intelligence

    @intelligence.setter
    def intelligence(self, new_value):
        self._intelligence.value = new_value

    @property
    def wisdom(self):
        return self._wisdom

    @wisdom.setter
    def wisdom(self, new_value):
        self._wisdom.value = new_value

    @property
    def charisma(self):
        return self._charisma

    @charisma.setter
    def charisma(self, new_value):
        self._charisma.value = new_value
