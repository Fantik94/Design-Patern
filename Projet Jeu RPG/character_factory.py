from character import Warrior, Mage, Archer

# Factory class
class CharacterFactory:
    @staticmethod
    def create_character(character_type, name):
        if character_type == "Guerrier":
            return Warrior(name)
        elif character_type == "Mage":
            return Mage(name)
        elif character_type == "Archer":
            return Archer(name)
        else:
            raise ValueError(f"Unknown character type: {character_type}")
