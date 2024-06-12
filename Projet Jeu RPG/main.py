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
                    ennemi.take_damage(ennemi.health_points)  # Inflige des dégâts égaux aux points de vie de l'ennemi pour assurer la mort
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
                        GameManager.reset_instance()  # Réinitialise l'instance singleton
                        break

                time.sleep(0.3)  # Pause pour une meilleure lisibilité

            if personnage.health_points <= 0:
                break

            print_separator()
            print(f"\n{Fore.GREEN}{ennemi.name} a été vaincu à l'étage {floor_number}!")
            
            # Heal 50% après chaque niveau si le joueur est encore en vie
            if personnage.health_points > 0:
                heal_amount = personnage.heal(0.5)  
                print(f"\n{Fore.GREEN}{personnage.name} se soigne de {heal_amount} points de vie à la fin de l'étage!")
                print(display_health_status(personnage, 'joueur'))

            # Augmenter les points de vie et les dégâts du personnage
            personnage.level_up()
            
            # Augmenter les chances d'ennemis de haute rareté
            rarity_weights = [max(weight - 5, 0) for weight in rarity_weights]

            # Ajouter un séparateur pour chaque étage dans l'historique des combats
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
