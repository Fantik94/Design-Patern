from colorama import Fore, Style
import random

class Enemy:
    RARITY_COLORS = {
        "Basique": Fore.WHITE,
        "Rare": Fore.BLUE,
        "Epique": Fore.MAGENTA,
        "Légendaire": Fore.YELLOW
    }

    RARITY_HEALTH_MULTIPLIERS = {
        "Basique": 1,
        "Rare": 2,
        "Epique": 2.8,
        "Légendaire": 4
    }

    RARITY_DAMAGE_MULTIPLIERS = {
        "Basique": 1.0,
        "Rare": 1.1,
        "Epique": 1.2,
        "Légendaire": 1.3
    }

    TYPE_HEALTH_MULTIPLIERS = {
        "Gobelin": 1,
        "Vampire": 1.12,
        "Hydre": 1.22
    }

    TYPE_CHANCES = {
        "Gobelin": 1.0,
        "Vampire": 0.8,
        "Hydre": 0.52
    }

    def __init__(self, name, base_health_points, base_attack_damage, rarity_weights=None, floor_number=1):
        self.name = name
        self.type = self.random_type()
        self.rarity = self.random_rarity(rarity_weights, floor_number)
        self.health_points = int(base_health_points * self.RARITY_HEALTH_MULTIPLIERS[self.rarity] * self.TYPE_HEALTH_MULTIPLIERS[self.type] * (1.1 ** (floor_number - 1)))
        self.base_attack_damage = base_attack_damage * (1.119 ** (floor_number - 1)) * (1.1109 ** (floor_number - 1)) * self.RARITY_DAMAGE_MULTIPLIERS[self.rarity]
        self.color = self.RARITY_COLORS[self.rarity]

    def random_type(self):
        types = ["Gobelin", "Vampire", "Hydre"]
        weights = [self.TYPE_CHANCES[t] for t in types]
        return random.choices(types, weights=weights, k=1)[0]

    def random_rarity(self, weights, floor_number):
        rarities = ["Basique", "Rare", "Epique", "Légendaire"]
        if weights is None:
            weights = [60, 25, 10, 5]
        adjusted_weights = self.adjust_rarity_weights(weights, floor_number)
        return random.choices(rarities, weights=adjusted_weights)[0]

    def adjust_rarity_weights(self, weights, floor_number):
        base_weight = weights[0]
        increment = floor_number - 1
        return [
            max(base_weight - increment * 3, 0),
            weights[1] + increment * 2,
            weights[2] + increment,
            weights[3] + increment // 2
        ]

    def take_damage(self, damage):
        self.health_points -= damage
        if self.health_points < 0:
            self.health_points = 0

    def attack(self):
        base_damage = random.randint(int(self.base_attack_damage / 2), int(self.base_attack_damage))
        return base_damage

    def display_health(self):
        health_points_int = int(self.health_points)
        health_bar = '█' * (health_points_int // 10) + '-' * (10 - health_points_int // 10)
        return f"{self.color}♥ {self.health_points} [{health_bar}]{Style.RESET_ALL}"

    def display_info(self):
        return f"{self.color}{self.name} ({self.type}, {self.rarity}) - Points de vie : {self.health_points}{Style.RESET_ALL}"
