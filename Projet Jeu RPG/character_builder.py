from character import Warrior, Mage, Archer

class CharacterBuilder:
    def __init__(self):
        self.name = None
        self.type = None

    def set_name(self, name):
        self.name = name
        return self

    def set_type(self, type):
        self.type = type
        return self

    def build(self):
        if self.type == "Guerrier":
            return Warrior(self.name)
        elif self.type == "Mage":
            return Mage(self.name)
        elif self.type == "Archer":
            return Archer(self.name)
        else:
            raise ValueError(f"Unknown character type: {self.type}")
