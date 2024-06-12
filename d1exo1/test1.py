from abc import ABC, abstractmethod

# Interface pour les commandes
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        pass

# Commande pour attaquer
class AttackCommand(Command):
    def __init__(self, character):
        self.character = character

    def execute(self):
        self.character.attack()

    def undo(self):
        self.character.cancel_attack()

    def redo(self):
        self.execute()

# Commande pour défendre
class DefendCommand(Command):
    def __init__(self, character):
        self.character = character

    def execute(self):
        self.character.defend()

    def undo(self):
        self.character.cancel_defense()

    def redo(self):
        self.execute()

# Commande pour soigner
class HealCommand(Command):
    def __init__(self, character):
        self.character = character

    def execute(self):
        self.character.heal()

    def undo(self):
        self.character.cancel_heal()

    def redo(self):
        self.execute()

# Classe représentant un personnage
class Character:
    def attack(self):
        print("Le personnage attaque.")

    def cancel_attack(self):
        print("L'attaque du personnage est annulée.")

    def defend(self):
        print("Le personnage se défend.")

    def cancel_defense(self):
        print("La défense du personnage est annulée.")

    def heal(self):
        print("Le personnage se soigne.")

    def cancel_heal(self):
        print("Le soin du personnage est annulé.")

# Utilisation des commandes
character = Character()

attack_command = AttackCommand(character)
defend_command = DefendCommand(character)
heal_command = HealCommand(character)

attack_command.execute()  # Le personnage attaque
defend_command.execute()  # Le personnage se défend
heal_command.execute()    # Le personnage se soigne

attack_command.undo()     # L'attaque du personnage est annulée
defend_command.undo()     # La défense du personnage est annulée
heal_command.undo()       # Le soin du personnage est annulé

attack_command.redo()     # Le personnage attaque à nouveau
defend_command.redo()     # Le personnage se défend à nouveau
heal_command.redo()       # Le personnage se soigne à nouveau