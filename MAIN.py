from os import remove


class Owner:
    name_own = None
    phone = None
    address = None
    def __init__(self, name_own, phone, address):
        self.name_own = name_own
        self.phone = phone
        self.address = address
        self.pets = []
    def add_pet(self, pet):
        self.pets.append(pet)
        print(f"{pet.name} теперь принадлежит {self.name_own}")
    def show_all_pets(self):
        print(f"\n Все питомцы {self.name_own} ")
        for pet in self.pets:
            print(pet.get_info())
            print("---------")


class Pet:
    name = None
    age = None
    breed = None
    color = None
    def __init__(self, name, age, breed, color):
        self.name = name
        self.age = age
        self.breed = breed
        self.color = color
        self.owner = None

    def get_info(self):
        return f"Name: {self.name}\n Age: {self.age}\n Breed {self.breed} \n Color: {self.color}"

    def set_owner(self, owner):
        self.owner = owner



class Dog(Pet):
    hunting = None
    homelike = None
    def __init__(self, name, age, breed, color, hunting, homelike):
        super(Dog,self).__init__(name,age,breed,color)
        self.hunting = hunting
        self.homelike = homelike
    def get_info(self):
        return f"Name: {self.name}\n Age: {self.age}\n Breed {self.breed} \n Color {self.color} \n Hunting: {self.hunting}\n Homelike: {self.homelike}"


class Cat(Pet):
    There_is_wool = None
    def __init__(self, name, age, breed, color, There_is_wool):
        super(Cat,self).__init__(name,age,breed,color)
        self.There_is_wool = There_is_wool

    def get_info(self):
        return f"Name: {self.name}\n Age: {self.age}\n Breed {self.breed} \n Color {self.color} \n There_is_wool: {self.There_is_wool}"


class Fish(Pet):
    need_oxygen = None
    def __init__(self, name, age, breed, color, need_oxygen):
        super(Fish,self).__init__(name,age,breed,color)
        self.need_oxygen = need_oxygen

    def get_info(self):
        return f"Name: {self.name}\n Age: {self.age}\n Breed {self.breed} \n Color {self.color} \n Need oxygen : {self.need_oxygen}"

class Bird(Pet):
    can_fly = None
    def __init__(self, name, age, breed, color, can_fly):
        super(Bird, self).__init__(name,age,breed,color)
        self.can_fly = can_fly
    def get_info(self):
        return f"Name: {self.name}\n Age: {self.age}\n Breed {self.breed} \n Color {self.color} \n Can fly: {self.can_fly}"

    def set_info(self, name, age, breed, color, can_fly):
        self.name = name
        self.age = age
        self.breed = breed
        self.color = color
        self.can_fly = can_fly


class Traning():
    def __init__(self, pet : Pet, traner):
        self.pet = pet
        self.traner = traner
        self.ability = []
    def skils(self, ability):
        self.ability.append(ability)
    def all_skils(self):
        print(self.ability)
    def delete_skils(self, ability):
        try:
            self.ability.remove(ability)
        except ValueError:
            print("Такого умения нет у питомца")

if __name__ == "__main__":
    a = Fish("jack", 15, "rock", "red", "Yes")
    b = Fish("lack", 15, "rock", "red", "Yes")
    owner = Owner("Max", "123345", "street")
    owner.add_pet(a)
    owner.add_pet(b)
    bird = Bird("Popug", 3, "pocker", "yellow", "Yes")
    owner.add_pet(bird)





    # tr = Traning(a, "LUKER")
    # tr.skils("сидеть")
    # tr.skils("кувырок")
    # tr.all_skils()
    # tr.delete_skils("сидеть")
    # tr.all_skils()

