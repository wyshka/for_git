from os import remove
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom


class Owner:
    def __init__(self, name_own, phone, address):
        self.name_own = name_own
        self.phone = phone
        self.address = address
        self.pets = []
        self.veterinarians = []


    def add_pet(self, pet):
        self.pets.append(pet)
        print(f"{pet.name} теперь принадлежит {self.name_own}")

    def show_all_pets(self):
        print(f"\nВсе питомцы {self.name_own}")
        for pet in self.pets:
            print(pet.get_info())
            print("---------")

    def delete_pet(self, pet):
        self.pets.remove(pet)
        print(f"Питомец {pet.name} был удален")

    def to_dict(self):
        return {
            "name_own": self.name_own,
            "phone": self.phone,
            "address": self.address,
            "pets": [pet.to_dict() for pet in self.pets]
        }

    @classmethod
    def from_dict(cls, data):
        owner = cls(data["name_own"], data["phone"], data["address"])
        for pet_data in data["pets"]:
            pet = Pet.from_dict(pet_data)
            owner.add_pet(pet)
        return owner
    def clear_all_pets(self):
        pet_count = len(self.pets)
        self.pets.clear()
        print(f"{pet_count} питомцев удалены")

    def remove_pet_by_name(self, pet_name):
        for pet in self.pets:
            if pet.name == pet_name:
                self.pets.remove(pet)
                print(f"Питомец {pet_name} удален")
                return True
        print(f"Питомец {pet_name} не найден")
        return False



class Pet:
    def __init__(self, name, age, breed, color):
        self.name = name
        self.age = age
        self.breed = breed
        self.color = color
        self.owner = None
        self.training = None
        self.eat = None
        self.vaccination = None

    def get_info(self):
        return f"Name: {self.name}\nAge: {self.age}\nBreed: {self.breed}\nColor: {self.color}"

    def set_owner(self, owner):
        self.owner = owner

    def get_name(self):
        return self.name

    def set_training(self, training_obj):
        self.training = training_obj

    def set_eat(self, eat_obj):
        self.eat = eat_obj

    def set_vaccination(self, vaccination_obj):
        self.vaccination = vaccination_obj

    def to_dict(self):
        data = {
            "type": self.__class__.__name__,
            "name": self.name,
            "age": self.age,
            "breed": self.breed,
            "color": self.color
        }
        if self.training:
            data["training"] = {
                "traner": self.training.traner,
                "ability": self.training.ability
            }
        if self.eat:
            data["eat"] = {
                "omnivorous": self.eat.omnivorous,
                "food": self.eat.food,
                "portions": self.eat.portions
            }
        if self.vaccination:
            data["vaccination"] = {
                "vaccine": self.vaccination.vaccine,
                "visits": self.vaccination.visits
            }
        return data

    @classmethod
    def from_dict(cls, data):
        pet_type = data.get("type", "Pet")
        if pet_type == "Dog":
            pet = Dog(
                data["name"], data["age"], data["breed"], data["color"],
                data.get("hunting", ""), data.get("homelike", "")
            )
        elif pet_type == "Cat":
            pet = Cat(
                data["name"], data["age"], data["breed"], data["color"],
                data.get("There_is_wool", "")
            )
        elif pet_type == "Fish":
            pet = Fish(
                data["name"], data["age"], data["breed"], data["color"],
                data.get("need_oxygen", "")
            )
        elif pet_type == "Bird":
            pet = Bird(
                data["name"], data["age"], data["breed"], data["color"],
                data.get("can_fly", "")
            )
        else:
            pet = cls(data["name"], data["age"], data["breed"], data["color"])

        if "training" in data:
            training_data = data["training"]
            training = Traning(pet, training_data["traner"])
            training.ability = training_data["ability"]
            pet.set_training(training)

        if "eat" in data:
            eat_data = data["eat"]
            eat = Eat(pet, eat_data["omnivorous"])
            eat.food = eat_data["food"]
            eat.portions = eat_data["portions"]
            pet.set_eat(eat)

        if "vaccination" in data:
            vacc_data = data["vaccination"]
            vaccination = Vaccination(pet)
            vaccination.vaccine = vacc_data["vaccine"]
            vaccination.visits = vacc_data["visits"]
            pet.set_vaccination(vaccination)

        return pet
    def remove_training(self):
        self.training = None
        print(f"Тренировки для {self.name} удалены")

    def remove_eat(self):
        self.eat = None
        print(f"Данные о питании {self.name} удалены")

    def remove_vaccination(self):
        self.vaccination = None
        print(f"Данные о вакцинации {self.name} удаены")


class Dog(Pet):
    def __init__(self, name, age, breed, color, hunting, homelike):
        super().__init__(name, age, breed, color)
        self.hunting = hunting
        self.homelike = homelike

    def get_info(self):
        return f"Name: {self.name}\nAge: {self.age}\nBreed: {self.breed}\nColor: {self.color}\nHunting: {self.hunting}\nHomelike: {self.homelike}"

    def to_dict(self):
        data = super().to_dict()
        data["hunting"] = self.hunting
        data["homelike"] = self.homelike
        return data


class Cat(Pet):
    def __init__(self, name, age, breed, color, There_is_wool):
        super().__init__(name, age, breed, color)
        self.There_is_wool = There_is_wool

    def get_info(self):
        return f"Name: {self.name}\nAge: {self.age}\nBreed: {self.breed}\nColor: {self.color}\nThere_is_wool: {self.There_is_wool}"

    def to_dict(self):
        data = super().to_dict()
        data["There_is_wool"] = self.There_is_wool
        return data


class Fish(Pet):
    def __init__(self, name, age, breed, color, need_oxygen):
        super().__init__(name, age, breed, color)
        self.need_oxygen = need_oxygen

    def get_info(self):
        return f"Name: {self.name}\nAge: {self.age}\nBreed: {self.breed}\nColor: {self.color}\nNeed oxygen: {self.need_oxygen}"

    def to_dict(self):
        data = super().to_dict()
        data["need_oxygen"] = self.need_oxygen
        return data


class Bird(Pet):
    def __init__(self, name, age, breed, color, can_fly):
        super().__init__(name, age, breed, color)
        self.can_fly = can_fly

    def get_info(self):
        return f"Name: {self.name}\nAge: {self.age}\nBreed: {self.breed}\nColor: {self.color}\nCan fly: {self.can_fly}"

    def to_dict(self):
        data = super().to_dict()
        data["can_fly"] = self.can_fly
        return data


class Traning():
    def __init__(self, pet, traner):
        self.pet = pet
        self.traner = traner
        self.ability = []
        pet.set_training(self)

    def skils(self, ability):
        self.ability.append(ability)

    def all_skils(self):
        print(self.ability)

    def delete_skils(self, ability):
        self.ability.remove(ability)


class Eat():
    def __init__(self, pet, omnivorous):
        self.omnivorous = omnivorous
        self.pet = pet
        self.food = []
        self.portions = []
        pet.set_eat(self)

    def what_eat(self, meal, dose):
        self.food.append(meal)
        self.portions.append(dose)

    def get_info(self):
        return f"Питомец {self.pet.name} ест {self.food} порции {self.portions}"

    def remove_food_or_portions(self, meal, dose):
        self.food.remove(meal)
        self.portions.remove(dose)


class Veterinarian():
    def __init__(self, pet, name, date):
        self.pet = pet
        self.name = name
        self.date = date

    def visite(self):
        print(f"{self.date} было посещения ветеринара {self.name} с питомцом {self.pet.name}")


class Vaccination():
    def __init__(self, pet):
        self.pet = pet
        self.vaccine = []
        self.visits = []
        pet.set_vaccination(self)

    def visite(self, vis, vaci):
        self.visits.append(vis)
        self.vaccine.append(vaci)

    def get_info(self):
        print(f"{self.visits} была сделана {self.vaccine} питомцу {self.pet.name}")

    def remove_vaccine_and_visit(self, vis, vaci):
        self.vaccine.remove(vis)
        self.visits.remove(vaci)


class FileManager:
    @staticmethod
    def save_to_json(owners, filename="pets_data.json"):
        data = {
            "owners": [owner.to_dict() for owner in owners]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в {filename}")

    @staticmethod
    def load_from_json(filename="pets_data.json"):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        owners = []
        for owner_data in data["owners"]:
            owner = Owner.from_dict(owner_data)
            owners.append(owner)
        print(f"Данные загружены из {filename}")
        return owners

    @staticmethod
    def save_to_xml(owners, filename="pets_data.xml"):
        root = ET.Element("pets_system")
        for owner in owners:
            owner_elem = ET.SubElement(root, "owner")
            ET.SubElement(owner_elem, "name_own").text = owner.name_own
            ET.SubElement(owner_elem, "phone").text = owner.phone
            ET.SubElement(owner_elem, "address").text = owner.address
            pets_elem = ET.SubElement(owner_elem, "pets")
            for pet in owner.pets:
                pet_elem = ET.SubElement(pets_elem, "pet")
                ET.SubElement(pet_elem, "type").text = pet.__class__.__name__
                ET.SubElement(pet_elem, "name").text = pet.name
                ET.SubElement(pet_elem, "age").text = str(pet.age)
                ET.SubElement(pet_elem, "breed").text = pet.breed
                ET.SubElement(pet_elem, "color").text = pet.color
                if isinstance(pet, Dog):
                    ET.SubElement(pet_elem, "hunting").text = pet.hunting
                    ET.SubElement(pet_elem, "homelike").text = pet.homelike
                elif isinstance(pet, Cat):
                    ET.SubElement(pet_elem, "There_is_wool").text = pet.There_is_wool
                elif isinstance(pet, Fish):
                    ET.SubElement(pet_elem, "need_oxygen").text = pet.need_oxygen
                elif isinstance(pet, Bird):
                    ET.SubElement(pet_elem, "can_fly").text = pet.can_fly
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        print(f"Данные сохранены в {filename}")

    @staticmethod
    def load_from_xml(filename="pets_data.xml"):
        tree = ET.parse(filename)
        root = tree.getroot()
        owners = []
        for owner_elem in root.findall("owner"):
            name_own = owner_elem.find("name_own").text
            phone = owner_elem.find("phone").text
            address = owner_elem.find("address").text
            owner = Owner(name_own, phone, address)
            pets_elem = owner_elem.find("pets")
            for pet_elem in pets_elem.findall("pet"):
                pet_type = pet_elem.find("type").text
                name = pet_elem.find("name").text
                age = int(pet_elem.find("age").text)
                breed = pet_elem.find("breed").text
                color = pet_elem.find("color").text
                if pet_type == "Dog":
                    hunting = pet_elem.find("hunting").text
                    homelike = pet_elem.find("homelike").text
                    pet = Dog(name, age, breed, color, hunting, homelike)
                elif pet_type == "Cat":
                    There_is_wool = pet_elem.find("There_is_wool").text
                    pet = Cat(name, age, breed, color, There_is_wool)
                elif pet_type == "Fish":
                    need_oxygen = pet_elem.find("need_oxygen").text
                    pet = Fish(name, age, breed, color, need_oxygen)
                elif pet_type == "Bird":
                    can_fly = pet_elem.find("can_fly").text
                    pet = Bird(name, age, breed, color, can_fly)
                else:
                    pet = Pet(name, age, breed, color)
                owner.add_pet(pet)
            owners.append(owner)
        print(f"Данные загружены из {filename}")
        return owners
    @staticmethod
    def delete_json_file(filename="pets_data.json"):
        try:
            remove(filename)
            print(f"Файл {filename} удален")
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    @staticmethod
    def delete_xml_file(filename="pets_data.xml"):
        try:
            remove(filename)
            print(f"Файл {filename} удален")
        except FileNotFoundError:
            print(f"Файл {filename} не найден")


if __name__ == "__main__":
    a = Fish("jack", 15, "rock", "red", "Yes")
    b = Fish("lack", 15, "rock", "red", "Yes")
    owner = Owner("Max", "123345", "street")
    a.set_owner(owner)
    owner.add_pet(a)
    owner.add_pet(b)

    bird = Bird("Popug", 3, "pocker", "yellow", "Yes")
    owner.add_pet(bird)

    food = Eat(bird, "Yes")
    food.what_eat("макароны", "150 грамм")
    food.what_eat("мясо", "500 грамм")

    tr = Traning(a, "LUKER")
    tr.skils("сидеть")
    tr.skils("кувырок")

    vac = Vaccination(a)
    vac.visite("21.19.2034", "от бешенаства")
    vac.visite("26.19.2034", "прививка")

    vet = Veterinarian(a, "Max", "21.21.2009")

    file_manager = FileManager()

    file_manager.save_to_json([owner])
    file_manager.save_to_xml([owner])

    print("\nЗАГРУЗКА ИЗ JSON ФАЙЛА:")
    loaded_owners_json = file_manager.load_from_json()
    for loaded_owner in loaded_owners_json:
        loaded_owner.show_all_pets()

    print("\nЗАГРУЗКА ИЗ XML ФАЙЛА:")
    loaded_owners_xml = file_manager.load_from_xml()
    for loaded_owner in loaded_owners_xml:
        loaded_owner.show_all_pets()

    print("\nОРИГИНАЛЬНАЯ ФУНКЦИОНАЛЬНОСТЬ:")
    print(bird.get_info())
    bird.can_fly = "False"
    print(bird.get_info())

    print(food.get_info())
    food.remove_food_or_portions("мясо", "500 грамм")
    print(food.get_info())

    vet.visite()
    vac.get_info()

    tr.all_skils()
    tr.delete_skils("сидеть")
    tr.all_skils()

    print("--------")
    owner.show_all_pets()
    owner.delete_pet(a)
    owner.show_all_pets()