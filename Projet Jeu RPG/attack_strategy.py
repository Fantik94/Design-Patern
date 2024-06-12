import random
from abc import ABC, abstractmethod
from colorama import Fore

class AttackStrategy(ABC):
    RARITY_DAMAGE_BONUS = {
        "Basique": 0,
        "Rare": 5,
        "Epique": 15,
        "Légendaire": 30
    }

    RARITY_COLORS = {
        "Basique": Fore.WHITE,
        "Rare": Fore.BLUE,
        "Epique": Fore.MAGENTA,
        "Légendaire": Fore.YELLOW
    }

    ONE_SHOT_CHANCES = {
        "Basique": 1/30,
        "Rare": 1/20,
        "Epique": 1/12,
        "Légendaire": 1/9
    }

    LIFESTEAL_PERCENTAGE_RANGES = {
        "Basique": (0.08, 0.16),
        "Rare": (0.16, 0.24),
        "Epique": (0.24, 0.32),
        "Légendaire": (0.30, 0.50)
    }

    NAMES = {
        "Sword": {
            "Basique": ["Épée rouillée"],
            "Rare": ["Épée d'argent"],
            "Epique": ["Épée enchantée"],
            "Légendaire": ["Excalibur"]
        },
        "Bow": {
            "Basique": ["Arc en bois"],
            "Rare": ["Arc en composite"],
            "Epique": ["Arc du faucon"],
            "Légendaire": ["Arc d'Artemis"]
        },
        "Staff": {
            "Basique": ["Bâton de novice"],
            "Rare": ["Bâton de mage"],
            "Epique": ["Bâton de sagesse"],
            "Légendaire": ["Bâton d'Azkaban"]
        }
    }

    def __init__(self, rarity=None, base_name=None):
        self.rarity = rarity if rarity else self.random_rarity()
        self.name = base_name if base_name else self.random_name()
        self.base_damage_min = 0
        self.base_damage_max = 0

    def random_rarity(self):
        rarities = ["Basique", "Rare", "Epique", "Légendaire"]
        return random.choices(rarities, weights=[70, 20, 7, 3])[0]

    def random_name(self):
        raise NotImplementedError("Subclasses should implement this method")

    def colorize_text(self, text):
        return f"{self.RARITY_COLORS[self.rarity]}{text}{Fore.RESET}"

    def check_one_shot(self):
        return random.random() < self.ONE_SHOT_CHANCES[self.rarity]

    def get_lifesteal(self):
        min_lifesteal, max_lifesteal = self.LIFESTEAL_PERCENTAGE_RANGES[self.rarity]
        return random.uniform(min_lifesteal, max_lifesteal)

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def get_damage(self, powerful=False, ultimate=False, multiplier=1):
        pass

class SwordAttack(AttackStrategy):
    def __init__(self, rarity=None, base_name=None):
        super().__init__(rarity, base_name)
        self.base_damage_min = 15
        self.base_damage_max = 20

    def random_name(self):
        return random.choice(self.NAMES["Sword"][self.rarity])

    def attack(self):
        return self.colorize_text(f"Attaque avec {self.name} ({self.rarity}) : Vous causez des dégâts tranchants.")

    def get_damage(self, powerful=False, ultimate=False, multiplier=1):
        if ultimate and self.check_one_shot():
            return float('inf'), False, self.get_lifesteal()  # Inflict infinite damage for one shot
        elif ultimate:
            return 0, False, 0  # No damage if the one shot fails
        multiplier *= 2 if powerful else 1
        base_damage = random.randint(self.base_damage_min, self.base_damage_max) * multiplier + self.RARITY_DAMAGE_BONUS[self.rarity]
        critical = False
        if random.random() < 0.2:  # 20% chance of critical hit
            base_damage *= 2
            critical = True
        return base_damage, critical, self.get_lifesteal()

class PowerfulSwordAttack(SwordAttack):
    def attack(self):
        return self.colorize_text(f"Attaque puissante avec {self.name} ({self.rarity}) : Vous causez des dégâts massifs.")

class UltimateSwordAttack(SwordAttack):
    def attack(self):
        return self.colorize_text(f"Attaque ultime avec {self.name} ({self.rarity}) : Vous tentez une attaque dévastatrice avec 1 chance sur 5 de one shot.")

class BowAttack(AttackStrategy):
    def __init__(self, rarity=None, base_name=None):
        super().__init__(rarity, base_name)
        self.base_damage_min = 16
        self.base_damage_max = 22

    def random_name(self):
        return random.choice(self.NAMES["Bow"][self.rarity])

    def attack(self):
        return self.colorize_text(f"Attaque avec {self.name} ({self.rarity}) : Vous causez des dégâts perforants.")

    def get_damage(self, powerful=False, ultimate=False, multiplier=1):
        if ultimate and self.check_one_shot():
            return float('inf'), False, self.get_lifesteal()  # Inflict infinite damage for one shot
        elif ultimate:
            return 0, False, 0  # No damage if the one shot fails
        multiplier *= 2 if powerful else 1
        base_damage = random.randint(self.base_damage_min, self.base_damage_max) * multiplier + self.RARITY_DAMAGE_BONUS[self.rarity]
        critical = False
        if random.random() < 0.2:  # 20% chance of critical hit
            base_damage *= 2
            critical = True
        return base_damage, critical, self.get_lifesteal()

class PowerfulBowAttack(BowAttack):
    def attack(self):
        return self.colorize_text(f"Attaque avec Flèche de feu ({self.name}) : Vous causez des dégâts perforants massifs.")

class UltimateBowAttack(BowAttack):
    def attack(self):
        return self.colorize_text(f"Attaque ultime avec {self.name} ({self.rarity}) : Vous tentez une attaque dévastatrice avec 1 chance sur 5 de one shot.")

class MagicAttack(AttackStrategy):
    def __init__(self, rarity=None, base_name=None):
        super().__init__(rarity, base_name)
        self.base_damage_min = 18
        self.base_damage_max = 24

    def random_name(self):
        return random.choice(self.NAMES["Staff"][self.rarity])

    def attack(self):
        return self.colorize_text(f"Attaque avec {self.name} ({self.rarity}) : Vous lancez un sort magique.")

    def get_damage(self, powerful=False, ultimate=False, multiplier=1):
        if ultimate and self.check_one_shot():
            return float('inf'), False, self.get_lifesteal()  # Inflict infinite damage for one shot
        elif ultimate:
            return 0, False, 0  # No damage if the one shot fails
        multiplier *= 2 if powerful else 1
        base_damage = random.randint(self.base_damage_min, self.base_damage_max) * multiplier + self.RARITY_DAMAGE_BONUS[self.rarity]
        critical = False
        if random.random() < 0.2:  # 20% chance of critical hit
            base_damage *= 2
            critical = True
        return base_damage, critical, self.get_lifesteal()

class PowerfulMagicAttack(MagicAttack):
    def attack(self):
        return self.colorize_text(f"Attaque avec Boule de feu ({self.rarity}) : Vous lancez un sort magique dévastateur.")

class UltimateMagicAttack(MagicAttack):
    def attack(self):
        return self.colorize_text(f"Attaque ultime avec {self.name} ({self.rarity}) : Vous tentez une attaque dévastatrice avec 1 chance sur 5 de one shot.")
