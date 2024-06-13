# Projet : Jeu de RPG textuel

## Introduction

Dans ce jeu de rôle textuel, les joueurs choisissent un personnage (guerrier, mage, archer, etc.) et affrontent des ennemis. Chaque personnage a une stratégie d'attaque différente et unique. Le jeu est structuré pour utiliser les patterns Singleton, Factory, et Strategy.

## Objectifs pédagogiques

- Comprendre et implémenter le pattern Singleton pour gérer l'état global du jeu.
- Utiliser le pattern Factory pour créer différents types de personnages.
- Appliquer le pattern Strategy pour définir des comportements d'attaque variables pour les personnages.

## Exigences du projet

### 1. Singleton Pattern

- **Description**: Le Singleton est un pattern qui restreint l'instanciation d'une classe à un seul objet. Il est utilisé pour contrôler l'accès aux ressources partagées.
- **Implémentation**:
  - Créer une classe `GameManager` qui utilise le pattern Singleton pour gérer l'état global du jeu (comme les scores, les tours, ou tout autre état global).
  - Assurer qu'il ne peut y avoir qu'une seule instance de `GameManager` pendant le jeu.
  - **Code**:
    ```python
    class GameManager:
        _instance = None

        @staticmethod
        def get_instance():
            if GameManager._instance is None:
                GameManager()
            return GameManager._instance

        @staticmethod
        def reset_instance():
            GameManager._instance = None

        def __init__(self):
            if GameManager._instance is not None:
                raise Exception("singleton")
            else:
                GameManager._instance = self
                self.characters = []
                self.battle_history = []
                self.current_round = 0

        def add_character(self, character):
            self.characters.append(character)

        def add_battle_history(self, record):
            self.battle_history.append(record)
    ```

### 2. Factory Pattern

- **Description**: Le Factory Pattern est un pattern de création qui utilise une méthode pour créer des objets sans avoir à spécifier la classe concrète de l'objet à créer. Il permet de créer des objets de différentes classes tout en maintenant une interface commune.
- **Implémentation**:
  - Créer une classe `CharacterFactory` qui sera responsable de la création des différents personnages (Guerrier, Mage, Archer).
  - Chaque type de personnage doit avoir des propriétés spécifiques (par exemple, points de vie, attaque, défense) et doit être créé par la `CharacterFactory`.
  - **Code**:
    ```python
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
    ```

### 3. Strategy Pattern

- **Description**: Le Strategy Pattern est un pattern comportemental qui permet de définir une famille d'algorithmes, de les encapsuler chacun et de les rendre interchangeables. Ce pattern permet de rendre les algorithmes indépendants du client qui les utilise.
- **Implémentation**:
  - Définir une interface `AttackStrategy` avec une méthode `attack`.
  - Implémenter différentes stratégies d'attaque pour chaque type de personnage (par exemple, `SwordAttack` pour le guerrier, `MagicAttack` pour le mage, `BowAttack` pour l'archer).
  - Chaque personnage doit pouvoir changer sa stratégie d'attaque à la volée (par exemple, un mage pourrait utiliser une attaque magique ou une attaque physique faible).
  - **Code**:
    ```python
    from abc import ABC, abstractmethod

    class AttackStrategy(ABC):
        @abstractmethod
        def attack(self):
            pass

    class SwordAttack(AttackStrategy):
        def attack(self):
            return "Attaque avec épée"

    class MagicAttack(AttackStrategy):
        def attack(self):
            return "Attaque magique"

    class BowAttack(AttackStrategy):
        def attack(self):
            return "Attaque avec arc"
    ```

## Étapes du projet

### 1. Initialisation du jeu

- Créer une instance unique de `GameManager`.
- Utiliser `CharacterFactory` pour créer des personnages et les ajouter à l'état global du jeu via `GameManager`.

### 2. Choix du personnage

- Demander au joueur de choisir un personnage (guerrier, mage, archer).
- Créer le personnage choisi en utilisant `CharacterFactory` et assigner une stratégie d'attaque initiale.

### 3. Simulation de combats

- Simuler des tours de combat où le personnage utilise sa stratégie d'attaque actuelle.
- Permettre au joueur de changer de stratégie d'attaque entre les tours.

### 4. Gestion de l'état du jeu

- Utiliser `GameManager` pour suivre les statistiques du jeu, comme les points de vie restants, les ennemis vaincus, etc.

## Prérequis avancé

- Prendre en compte la rareté de l’attaque pour l'ennemie.
- Faire 10 combats.
- Avoir un ennemi différent à chaque étage.
- Mettre un système de Heal en place.
- Historique des combats avec `GameManager`.

## Implémentation du jeu

Le jeu est implémenté avec plusieurs classes et fichiers pour organiser le code de manière claire et modulaire.

### Structure des fichiers

- `main.py`: Point d'entrée principal du jeu.
- `game_manager.py`: Implémentation du Singleton pour gérer l'état global du jeu.
- `character_factory.py`: Implémentation de la Factory pour créer des personnages.
- `character_builder.py`: Implémentation du Builder pour construire les personnages.
- `enemy.py`: Classe pour les ennemis avec leur logique.
- `attack_strategy.py`: Implémentation des différentes stratégies d'attaque.
- `character.py`: Définitions des classes de personnages.

## Code principal (`main.py`), naration du jeu.

```python
from game_manager import GameManager
from character_builder import CharacterBuilder
from enemy import Enemy
from colorama import init, Fore, Style
from character import Archer, Mage
import time

init(autoreset=True)

def get_valid_input(prompt, valid_choices, default_choice=None):
    while True:
        user_input = input(prompt).strip()
        if user_input == "" and default_choice is not None:
            return default_choice
        try:
            choice = int(user_input)
            if choice in valid_choices:
                return choice
            else:
                print(Fore.RED + "Choix invalide. Veuillez entrer un numéro valide." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Entrée invalide. Veuillez entrer un numéro." + Style.RESET_ALL)

def print_separator():
    print(Fore.YELLOW + "\n" + "=" * 50 + "\n" + Style.RESET_ALL)

def ask_yes_no_question(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ["oui", "non"]:
            return user_input == "oui"
        print(Fore.RED + "Réponse invalide. Veuillez répondre par 'oui' ou 'non'." + Style.RESET_ALL)

def display_health_status(entity, entity_type):
    health_bar = entity.display_health()
    return f"{Fore.CYAN if entity_type == 'joueur' else Fore.RED}{entity.name} - Barre de vie : {health_bar}{Style.RESET_ALL}"

def main():
    while True:
        game_manager = GameManager.get_instance()

        print(Fore.CYAN + "Choisissez un type de personnage :")
        types = ["Guerrier", "Mage", "Archer"]
        for i, type_pers in enumerate(types):
            print(f"{Fore.GREEN}{i + 1}. {type_pers}{Style.RESET_ALL}")

        choix = get_valid_input("Entrez le numéro du type de personnage : ", [1, 2, 3])
        
        nom = input("Entrez le nom de votre personnage : ")
        builder = CharacterBuilder().set_name(nom).set_type(types[choix - 1])
        personnage = builder.build()
        game_manager.add_character(personnage)

        print(f"\n{Fore.GREEN}{personnage.name} rejoint la bataille!")
        print(f"Stratégie d'attaque initiale : {personnage.attack_strategy.attack()}")

        rarity_weights = [70, 20, 7, 3]  # Initial rarity weights

        for floor_number in range(1, 11):
            print_separator()
            print(f"{Fore.YELLOW}Étage {floor_number}")
            print_separator()
            
            # Initialisation de l'ennemi
            base_health_points = 100
            base_attack_damage = 10
            ennemi = Enemy("Ennemi", base_health_points, base_attack_damage, rarity_weights, floor_number)
            print(f"{Fore.YELLOW}{ennemi.display_info()} apparaît!")

            while ennemi.health_points > 0 and personnage.health_points > 0:
                print_separator()
                print(f"{Fore.YELLOW}Choisissez le type d'attaque :")
                print(Fore.WHITE + "1. Attaque simple" + Style.RESET_ALL)
                if personnage.powerful_attacks_remaining > 0:
                    powerful_attack_name = "Attaque puissante"
                    if isinstance(personnage, Archer):
                        powerful_attack_name = "Flèche de feu"
                    elif isinstance(personnage, Mage):
                        powerful_attack_name = "Boule de feu"
                    print(f"{Fore.RED}2. {powerful_attack_name} ({personnage.powerful_attacks_remaining} restantes)" + Style.RESET_ALL)
                if personnage.ultimate_attacks_remaining > 0:
                    print(f"{Fore.MAGENTA}3. Attaque ultime ({personnage.ultimate_attacks_remaining} restante)" + Style.RESET_ALL)

                valid_attack_choices = [1]
                if personnage.powerful_attacks_remaining > 0:
                    valid_attack_choices.append(2)
                if personnage.ultimate_attacks_remaining > 0:
                    valid_attack_choices.append(3)
                attack_choice = get_valid_input("Entrez le numéro de l'attaque : ", valid_attack_choices, default_choice=1)
                
                powerful = (attack_choice == 2)
                ultimate = (attack_choice == 3)

                if powerful:
                    personnage.change_to_powerful_attack()
                elif ultimate:
                    personnage.change_to_ultimate_attack()
                else:
                    personnage.change_attack_strategy(personnage.get_initial_attack_strategy())

                print(f"\n{Fore.YELLOW}{personnage.name} attaque!")

                damage, critical, lifesteal = personnage.attack(powerful=powerful, ultimate=ultimate)
                
                if damage == float('inf'):
                    print(Fore.RED + "Coup fatal ! L'ennemi est éliminé d'un seul coup.")
                    ennemi.take_damage(ennemi.health_points)  # Inflict damage equal to the enemy's health to ensure death
                elif damage == 0 and ultimate:
                    print(Fore.RED + "L'attaque ultime a échoué ! Vous perdez la moitié de vos points de vie.")
                    personnage.health_points = int(personnage.health_points / 2)
                else:
                    print(Fore.MAGENTA + personnage.attack_strategy.attack())
                    print(f"{Fore.YELLOW}Dégâts infligés : {damage}{Fore.RESET}")
                    if critical:
                        print(f"{Fore.RED}Coup critique !")
                    ennemi.take_damage(damage)

                    lifesteal_amount = personnage.lifesteal(damage, lifesteal)
                    print(f"{Fore.GREEN}Vous récupérez {lifesteal_amount} points de vie grâce au vol de vie !")

                    game_manager.add_battle_history(
                        f"{Fore.CYAN}Étage {floor_number}: {personnage.attack_strategy.attack()} - Dégâts : {damage} {'(Coup critique!)' if critical else ''} (Vol de vie : {lifesteal_amount})\n"
                        f"{display_health_status(personnage, 'joueur')}\n"
                        f"{display_health_status(ennemi, 'ennemi')}"
                    )

                # Affichage des barres de vie
                print(display_health_status(personnage, 'joueur'))
                print(display_health_status(ennemi, 'ennemi'))

                if ennemi.health_points > 0:
                    # L'ennemi attaque le joueur
                    damage = ennemi.attack()
                    personnage.health_points -= damage
                    print(f"\n{Fore.RED}{ennemi.name} attaque et inflige {damage} dégâts!")
                    print(display_health_status(personnage, 'joueur'))
                    game_manager.add_battle_history(
                        f"{Fore.RED}Étage {floor_number}: {ennemi.name} attaque - Dégâts : {damage}\n"
                        f"{display_health_status(personnage, 'joueur')}\n"
                        f"{display_health_status(ennemi, 'ennemi')}"
                    )

                    if personnage.health_points <= 0:
                        print(f"\n{Fore.RED}{personnage.name} est mort!")
                        GameManager._instance = None  # Reset singleton instance
                        break

                time.sleep(0.5)  # Pause for better readability

            if personnage.health_points <= 0:
                break

            print_separator()
            print(f"\n{Fore.GREEN}{ennemi.name} a été vaincu à l'étage {floor_number}!")
            
            # Heal 50% after each level if the player is still alive
            if personnage.health_points > 0:
                heal_amount = personnage.heal(0.5)  
                print(f"\n{Fore.GREEN}{personnage.name} se soigne de {heal_amount} points de vie à la fin de l'étage!")
                print(display_health_status(personnage, 'joueur'))

            # Augmenter les points de vie et les dégâts du personnage
            personnage.level_up()
            
            # Augmenter les chances d'ennemis de haute rareté
            rarity_weights = [max(weight - 5, 0) for weight in rarity_weights]

            # Add separator for each floor in battle history
            game_manager.add_battle_history(
                "=" * 50 + f"\n{Fore.YELLOW}Fin de l'étage {floor_number}\n" + "=" * 50 + Style.RESET_ALL
            )

        if personnage.health_points > 0:
            print(f"\n{Fore.GREEN}{personnage.name} a survécu aux 10 étages!")
        else:
            print(f"\n{Fore.RED}{'='*10} FIN DU JEU {'='*10}\nVoici l'histoire des combats :\n{'='*10} FIN DU JEU {'='*10}{Style.RESET_ALL}")

        if ask_yes_no_question("Voulez-vous voir l'historique des combats ? (oui/non) "):
            print_separator()
            for record in game_manager.battle_history:
                print(record)

        if not ask_yes_no_question("Voulez-vous relancer le jeu ? (oui/non) "):
            print(Fore.YELLOW + "Merci d'avoir joué ! À la prochaine !" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()
