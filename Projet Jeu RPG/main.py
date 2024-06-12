from game_manager import GameManager
from character_factory import CharacterFactory, Mage, Archer
from enemy import Enemy
from colorama import init, Fore, Style
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
                print("Choix invalide. Veuillez entrer un numéro valide.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un numéro.")

def print_separator():
    print(Fore.YELLOW + "\n" + "=" * 50 + "\n" + Style.RESET_ALL)

def ask_yes_no_question(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ["oui", "non"]:
            return user_input == "oui"
        print("Réponse invalide. Veuillez répondre par 'oui' ou 'non'.")

def main():
    while True:
        game_manager = GameManager.get_instance()
        
        print(Fore.BLUE + "Bienvenue dans le jeu RPG!\n")
        print(Fore.CYAN + "Choisissez classe :")
        types = ["Guerrier", "Mage", "Archer"]
        for i, type_pers in enumerate(types):
            print(f"{i + 1}. {type_pers}")

        choix = get_valid_input("Entrez le numéro : ", [1, 2, 3])
        
        nom = input("Entrez le nom de votre personnage : ")
        personnage = CharacterFactory.create_character(types[choix - 1], nom)
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
                        f"{Fore.BLUE}Joueur ({personnage.name}) - Points de vie : {personnage.health_points}{Style.RESET_ALL}\n"
                        f"{Fore.RED}Ennemi ({ennemi.name}) - Points de vie : {ennemi.health_points}{Style.RESET_ALL}"
                    )

                # Affichage des barres de vie
                print(f"{personnage.name} - Barre de vie : {personnage.display_health()}")
                print(f"{ennemi.display_info()} - Barre de vie : {ennemi.display_health()}")

                if ennemi.health_points > 0:
                    # L'ennemi attaque le joueur
                    damage = ennemi.attack()
                    personnage.health_points -= damage
                    print(f"\n{Fore.RED}{ennemi.name} attaque et inflige {damage} dégâts!")
                    print(f"{personnage.name} - Barre de vie : {personnage.display_health()}")
                    game_manager.add_battle_history(
                        f"{Fore.RED}Étage {floor_number}: {ennemi.name} attaque - Dégâts : {damage}\n"
                        f"{Fore.BLUE}Joueur ({personnage.name}) - Points de vie : {personnage.health_points}{Style.RESET_ALL}\n"
                        f"{Fore.RED}Ennemi ({ennemi.name}) - Points de vie : {ennemi.health_points}{Style.RESET_ALL}"
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
                print(f"{personnage.name} - Barre de vie : {personnage.display_health()}")

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
            print(f"\n{Fore.RED}{'='*10} FIN DU JEU {'='*10}\n{Style.RESET_ALL}")

        if ask_yes_no_question("Voulez-vous voir l'historique des combats ? (oui/non) : "):
            print_separator()
            for record in game_manager.battle_history:
                print(record)

        if not ask_yes_no_question("Voulez-vous relancer le jeu ? (oui/non) : "):
            print("Merci d'avoir joué !")
            break

if __name__ == "__main__":
    main()
#test