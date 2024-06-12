class ForceManager:
    _instance = None  
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.force_level = 0 
            self.initialized = True

    def access_force(self):
        return "La Force est avec vous. Niveau actuel : {}".format(self.force_level)

    def increase_force(self, amount):
        self.force_level += amount
        return "Niveau de la Force augmenté. Nouveau niveau : {}".format(self.force_level)

    def decrease_force(self, amount):
        self.force_level -= amount
        return "Niveau de la Force diminué. Nouveau niveau : {}".format(self.force_level)

if __name__ == "__main__":
    manager1 = ForceManager()
    print(manager1.access_force())
    print(manager1.increase_force(10))

    manager2 = ForceManager()
    print(manager2.access_force())
    print(manager2.decrease_force(5))

    print("manager1 est manager2 : ", manager1 is manager2)
