from abc import ABC, abstractmethod

class Arme(ABC):
    @abstractmethod
    def utiliser(self):
        pass

class Armure(ABC):
    @abstractmethod
    def porter(self):
        pass

class FabriqueEquipement(ABC):
    @abstractmethod
    def creer_arme(self) -> Arme:
        pass

    @abstractmethod
    def creer_armure(self) -> Armure:
        pass

class Epée(Arme):
    def utiliser(self):
        return "une épée du hero."

class BaguetteMagique(Arme):
    def utiliser(self):
        return "une baguette magique divine."

class Arc(Arme):
    def utiliser(self):
        return "un arc puissant légendaire."

class ArmureDArgent(Armure):
    def porter(self):
        return "une armure d'argent."

class RobeMagique(Armure):
    def porter(self):
        return "une tennue magique enchantée."

class ArmureEnCuir(Armure):
    def porter(self):
        return "une armure en cuir."

class FabriqueGuerrier(FabriqueEquipement):
    def creer_arme(self) -> Arme:
        return Epée()

    def creer_armure(self) -> Armure:
        return ArmureDArgent()

class FabriqueMage(FabriqueEquipement):
    def creer_arme(self) -> Arme:
        return BaguetteMagique()

    def creer_armure(self) -> Armure:
        return RobeMagique()

class FabriqueArcher(FabriqueEquipement):
    def creer_arme(self) -> Arme:
        return Arc()

    def creer_armure(self) -> Armure:
        return ArmureEnCuir()

def main():
    print("Choisissez un type de personnage :")
    types = ["Guerrier", "Mage", "Archer"]
    for i, type_pers in enumerate(types):
        print(f"{i + 1}. {type_pers}")
    choix = int(input("Entrez le numéro du type de personnage : "))

    if choix == 1:
        fabrique = FabriqueGuerrier()
    elif choix == 2:
        fabrique = FabriqueMage()
    elif choix == 3:
        fabrique = FabriqueArcher()
    else:
        print("Choix invalide")
        return

    arme = fabrique.creer_arme()
    armure = fabrique.creer_armure()

    print("\nÉquipement créé :")
    print(arme.utiliser())
    print(armure.porter())

if __name__ == "__main__":
    main()
