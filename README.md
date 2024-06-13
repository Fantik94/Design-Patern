# Projet : Jeu de RPG textuel

## Introduction

Dans ce jeu de rôle textuel, les joueurs choisissent un personnage (guerrier, mage, archer) et affrontent des ennemis. Chaque personnage a une stratégie d'attaque différente et unique. Le jeu est structuré pour utiliser les patterns Singleton, Factory, et Strategy.

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

- Prendre en compte la rareté de l’attaque pour l'ennemi.
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


### Liste des tâches à accomplir

- [x] Implémenter le pattern Singleton pour gérer l'état global du jeu (fichier : `game_manager.py`).
- [x] Utiliser le pattern Factory pour créer des personnages de différents types (fichier : `character_factory.py`).
- [x] Appliquer le pattern Strategy pour les attaques des personnages (fichier : `attack_strategy.py`).
- [x] Utiliser le pattern Builder pour la création des personnages (fichier : `character_builder.py`).
- [x] Implémenter la gestion des ennemis et leurs attaques (fichier : `enemy.py`).
- [x] Ajouter des mécaniques de jeu comme le vol de vie, les attaques critiques, et les attaques puissantes.
- [x] Implémenter un système de soin et d'amélioration des personnages après chaque niveau.
- [x] Ajouter un historique des combats pour suivre les actions pendant le jeu.
- [x] Implémenter la logique principale du jeu avec une boucle de jeu (fichier : `main.py`).
- [x] Améliorer l'affichage des points de vie et des barres de santé pour plus de lisibilité.


## Comment jouer

1. Clonez le repository.
2. Assurez-vous d'avoir Python installé.
3. `cd Projet Jeu RPG`
4. Exécutez le fichier `main.py`. 
    ```
    python main.py
    ```
5. Suivez les instructions affichées pour choisir un personnage et combattre les ennemis.

## Auteur

- `RINGLER Baptiste`, module de Design Patern (H3 Hitema)
