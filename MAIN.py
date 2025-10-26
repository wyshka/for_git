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
    def delete_pet(self, pet):
        try:
            pet_name = pet.get_name()
            self.pets.remove(pet)
            print(f"Питомец {pet_name} был удален из списка питомцев :(")
        except ValueError:
            print("Неправильная кличка питомца")



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

    def set_owner(self, owner ):
        self.owner = owner
    def get_name(self):
        return self.name

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
        return print(f"Name: {self.name}\n Age: {self.age}\n Breed {self.breed} \n Color {self.color} \n Can fly: {self.can_fly}")




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

class Eat():
    def __init__(self, pet : Pet , omnivorous):
        self.omnivorous = omnivorous
        self.pet = pet
        self.food = []
        self.portions = []
    def what_eat(self, meal, dose):
        self.food.append(meal)
        self.portions.append(dose)
    def get_info(self):
        return f"Питомец {self.pet.name} ест {self.food} порции {self.portions}"
    def remove_food_or_portions(self, meal, dose):
        try:
            self.food.remove(meal)
            self.portions.remove(dose)
        except ValueError:
            print("Неправильное название")

class Veterinarian():
    def __init__(self, pet : Pet, name, date):
        self.pet = pet
        self.name = name
        self.date = date
    def visite(self):
        return print(f"{self.date} было посещения ветеринара {self.name} с питомцом {self.pet.name}")

class Vaccination():
    def __init__(self, pet : Pet):
        self.pet = pet
        self.vaccine = []
        self.visits = []
    def visite(self, vis, vaci):
        self.visits.append(vis)
        self.vaccine.append(vaci)
    def get_info(self):
        return print(f"{self.visits} была сделана {self.vaccine} питомцу {self.pet.name}")
    def remove_vaccine_and_visit(self, vis, vaci):
        try:
            self.vaccine.remove(vis)
            self.visits.remove(vaci)
        except ValueError:
            print("Неправильное названия или дата")

if __name__ == "__main__":
    a = Fish("jack", 15, "rock", "red", "Yes")
    b = Fish("lack", 15, "rock", "red", "Yes")
    owner = Owner("Max", "123345", "street")
    a.set_owner(owner)
    owner.add_pet(a)
    owner.add_pet(b)
    bird = Bird("Popug", 3, "pocker", "yellow", "Yes")
    owner.add_pet(bird)
    bird.get_info()
    bird.can_fly = "False"
    bird.get_info()
    food = Eat(bird, "Yes")
    food.what_eat("макароны", "150 грамм")
    food.what_eat("мясо", "500 грамм")
    print(food.get_info())
    food.remove_food_or_portions("мясо", "150 грамм")
    print(food.get_info())
    vet = Veterinarian(a,"Max", "21.21.2009")
    vet.visite()

    vac = Vaccination(a)
    vac.visite("21.19.2034", " от бешенаства")
    vac.visite("26.19.2034", "прививка")
    vac.get_info()


    tr = Traning(a, "LUKER")
    tr.skils("сидеть")
    tr.skils("кувырок")
    tr.all_skils()
    tr.delete_skils("сидеть")
    tr.all_skils()

    print("--------")
    owner.show_all_pets()
    owner.delete_pet(a)
    owner.show_all_pets()
