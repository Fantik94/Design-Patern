class Personnage:
    def __init__(self, nom, classe, points_de_vie=None, force=None, agilite=None, intelligence=None, arme=None, armure=None):
        self.nom = nom
        self.classe = classe
        self.points_de_vie = points_de_vie
        self.force = force
        self.agilite = agilite
        self.intelligence = intelligence
        self.arme = arme
        self.armure = armure

    def __str__(self):
        return (f"Nom : {self.nom}\nClasse : {self.classe}\nPoints de vie : {self.points_de_vie}\n"
                f"Force : {self.force}\nAgilité : {self.agilite}\nIntelligence : {self.intelligence}\n"
                f"Arme : {self.arme}\nArmure : {self.armure}")

class Builder:
    def __init__(self):
        self.nom = None
        self.classe = None
        self.points_de_vie = None
        self.force = None
        self.agilite = None
        self.intelligence = None
        self.arme = None
        self.armure = None

    def set_nom(self, nom):
        self.nom = nom
        return self

    def set_classe(self, classe):
        self.classe = classe
        return self

    def set_points_de_vie(self, points_de_vie):
        self.points_de_vie = points_de_vie
        return self

    def set_force(self, force):
        self.force = force
        return self

    def set_agilite(self, agilite):
        self.agilite = agilite
        return self

    def set_intelligence(self, intelligence):
        self.intelligence = intelligence
        return self

    def set_arme(self, arme):
        self.arme = arme
        return self

    def set_armure(self, armure):
        self.armure = armure
        return self

    def build(self):
        return Personnage(self.nom, self.classe, self.points_de_vie, self.force, self.agilite, self.intelligence, self.arme, self.armure)


def creer_personnage():
    constructeur = Builder()

    nom = input("Entrez le nom du personnage : ")
    constructeur.set_nom(nom)

    print("Choisissez une classe :")
    classes = ["Guerrier", "Mage", "Archer"]
    for i, classe in enumerate(classes):
        print(f"{i + 1}. {classe}")
    choix_classe = int(input("Entrez le numéro de la classe : "))
    constructeur.set_classe(classes[choix_classe - 1])

    points_de_vie = input("Entrez les points de vie (laisser vide si aucune valeur) : ")
    if points_de_vie:
        constructeur.set_points_de_vie(int(points_de_vie))

    force = input("Entrez la force (laisser vide si aucune valeur) : ")
    if force:
        constructeur.set_force(int(force))

    agilite = input("Entrez l'agilité (laisser vide si aucune valeur) : ")
    if agilite:
        constructeur.set_agilite(int(agilite))

    intelligence = input("Entrez l'intelligence (laisser vide si aucune valeur) : ")
    if intelligence:
        constructeur.set_intelligence(int(intelligence))

    arme = input("Entrez l'arme (laisser vide si aucune valeur) : ")
    if arme:
        constructeur.set_arme(arme)

    armure = input("Entrez l'armure (laisser vide si aucune valeur) : ")
    if armure:
        constructeur.set_armure(armure)

    personnage = constructeur.build()
    print("\nPersonnage créé avec succès !")
    print(personnage)

if __name__ == "__main__":
    creer_personnage()

