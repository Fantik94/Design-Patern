from attack_strategy import SwordAttack, MagicAttack, BowAttack, PowerfulSwordAttack, PowerfulBowAttack, PowerfulMagicAttack, UltimateSwordAttack, UltimateBowAttack, UltimateMagicAttack
from colorama import Fore, Style
import random

# Base Character class
class Character:
    def __init__(self, name, health_points, damage_multiplier):
        self.name = name
        self.health_points = health_points
        self.max_health_points = health_points
        self.damage_multiplier = damage_multiplier
        self.powerful_attacks_remaining = 2
        self.ultimate_attacks_remaining = 1
        self.initial_rarity = None
        self.initial_name = None
        self.initial_attack_strategy = None

    def attack(self, powerful=False, ultimate=False):
        if powerful and self.powerful_attacks_remaining > 0:
            self.powerful_attacks_remaining -= 1
            return self.attack_strategy.get_damage(powerful=True, multiplier=self.damage_multiplier)
        elif ultimate and self.ultimate_attacks_remaining > 0:
            self.ultimate_attacks_remaining -= 1
            return self.attack_strategy.get_damage(ultimate=True, multiplier=self.damage_multiplier)
        return self.attack_strategy.get_damage(multiplier=self.damage_multiplier)

    def change_attack_strategy(self, new_strategy):
        self.attack_strategy = new_strategy

    def change_to_powerful_attack(self):
        pass  # Subclasses will override this method

    def change_to_ultimate_attack(self):
        pass  # Subclasses will override this method

    def get_initial_attack_strategy(self):
        return self.initial_attack_strategy

    def heal(self, percentage=None):
        if percentage is None:
            heal_percentage = random.uniform(0.05, 0.10)
        else:
            heal_percentage = percentage
        heal_amount = int(self.max_health_points * heal_percentage)
        self.health_points += heal_amount
        if self.health_points > self.max_health_points:
            self.health_points = self.max_health_points
        return heal_amount

    def lifesteal(self, damage, lifesteal_percentage):
        if damage == float('inf'):
            return 0  # No lifesteal if the damage is infinite (coup fatal)
        lifesteal_amount = int(damage * lifesteal_percentage)
        self.health_points += lifesteal_amount
        if self.health_points > self.max_health_points:
            self.health_points = self.max_health_points
        return lifesteal_amount

    def level_up(self):
        self.max_health_points = int(self.max_health_points * 1.1)
        self.health_points = self.max_health_points
        self.attack_strategy.base_damage_min = int(self.attack_strategy.base_damage_min * 1.1)
        self.attack_strategy.base_damage_max = int(self.attack_strategy.base_damage_max * 1.1)
        self.powerful_attacks_remaining = 2
        self.ultimate_attacks_remaining = 1

    def display_health(self):
        health_bar = '█' * (self.health_points // 10) + '-' * (10 - self.health_points // 10)
        return f"{Fore.RED}♥ {self.health_points:.1f} [{health_bar}]{Style.RESET_ALL}"

# Concrete Characters
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health_points=150, damage_multiplier=1.0)
        self.attack_strategy = SwordAttack()
        self.initial_rarity = self.attack_strategy.rarity
        self.initial_name = self.attack_strategy.name
        self.initial_attack_strategy = SwordAttack(rarity=self.initial_rarity, base_name=self.initial_name)

    def change_to_powerful_attack(self):
        self.attack_strategy = PowerfulSwordAttack(rarity=self.initial_rarity, base_name=self.initial_name)

    def change_to_ultimate_attack(self):
        self.attack_strategy = UltimateSwordAttack(rarity=self.initial_rarity, base_name=self.initial_name)

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health_points=70, damage_multiplier=1.2)
        self.attack_strategy = MagicAttack()
        self.initial_rarity = self.attack_strategy.rarity
        self.initial_name = self.attack_strategy.name
        self.initial_attack_strategy = MagicAttack(rarity=self.initial_rarity, base_name=self.initial_name)

    def change_to_powerful_attack(self):
        self.attack_strategy = PowerfulMagicAttack(rarity=self.initial_rarity, base_name=self.initial_name)

    def change_to_ultimate_attack(self):
        self.attack_strategy = UltimateMagicAttack(rarity=self.initial_rarity, base_name=self.initial_name)

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health_points=100, damage_multiplier=1.1)
        self.attack_strategy = BowAttack()
        self.initial_rarity = self.attack_strategy.rarity
        self.initial_name = self.attack_strategy.name
        self.initial_attack_strategy = BowAttack(rarity=self.initial_rarity, base_name=self.initial_name)

    def change_to_powerful_attack(self):
        self.attack_strategy = PowerfulBowAttack(rarity=self.initial_rarity, base_name=self.initial_name)

    def change_to_ultimate_attack(self):
        self.attack_strategy = UltimateBowAttack(rarity=self.initial_rarity, base_name=self.initial_name)
