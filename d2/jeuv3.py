from abc import ABC, abstractmethod

class StrategieAttaque(ABC):
    @abstractmethod
    def attaquer(self):
        pass

class AttaqueEpee(StrategieAttaque):
    def attaquer(self):
        return "Vous attaquez avec une épée et causez des dégâts tranchants."

class AttaqueArc(StrategieAttaque):
    def attaquer(self):
        return "Vous attaquez avec un arc et causez des dégâts perforants."

class AttaqueMagique(StrategieAttaque):
    def attaquer(self):
        return "Vous lancez un sort magique et causez des dégâts magiques."

class Personnage:
    def __init__(self, nom):
        self.nom = nom
        self.strategie_attaque = None

    def set_strategie_attaque(self, strategie: StrategieAttaque):
        self.strategie_attaque = strategie

    def attaquer(self):
        if self.strategie_attaque:
            print(f"{self.nom} : {self.strategie_attaque.attaquer()}")
        else:
            print(f"{self.nom} ne sait pas comment attaquer.")

def main():
    guerrier = Personnage("Guerrier")
    mage = Personnage("Mage")
    archer = Personnage("Archer")


    attaque_epee = AttaqueEpee()
    attaque_arc = AttaqueArc()
    attaque_magique = AttaqueMagique()

    guerrier.set_strategie_attaque(attaque_epee)
    guerrier.attaquer()

    archer.set_strategie_attaque(attaque_arc)
    archer.attaquer()

    mage.set_strategie_attaque(attaque_magique)
    mage.attaquer()

if __name__ == "__main__":
    main()
