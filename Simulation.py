from Person import Person
from RandomGenerator import RandomGenerator
from Insurance import Insurance
import re


class Simulation:
    population_size = Insurance.employees * Insurance.PEOPLE_PER_EMPLOYEE  # wielkość populacji
    people = []  # tablica przechowująca populację
    time = 50  # ilość lat w symulacji
    rng = RandomGenerator()
    month = 1  # aktualny miesiąc
    ACCIDENT_RANGE = 50000000  # zakres losowania
    accident_counter = 0  # ilość wypadków
    death_counter = 0  # liczba osób, które zginęły
    year_counter = 1
    if_acc = 0
    month_money = 0

    below_equal_five = 0
    below_equal_seven = 0
    over_seven = 0

    below_equal_five_acc = 0
    below_equal_seven_acc = 0
    over_seven_acc = 0

    below_equal_five_age = 0
    below_equal_seven_age = 0
    over_seven_age = 0

    @staticmethod
    def main():
        file = open("log.txt", "w+")
        file.write(f"Rok;Miesiąc;Zebrane pieniądze;"
                   f"Koszt składki <500;Średki wiek;Ilość wypadków;"
                   f"Koszt składki 500-700;Średki wiek;Ilość wypadków;"
                   f"Koszt skladki >700;Średki wiek;Ilość wypadków\n")
        file.close()
        """Start symulacji"""
        Simulation.create_population()
        for i in range(Simulation.time):
            Simulation.year()

        print("Końcowe pieniądze ubezpieczalni:", re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(Insurance.collected_money)), "zl")
        print(f"Populacja: {len(Simulation.people)}")

    @staticmethod
    def year():
        """Akcja wykonywana co rok"""
        Simulation.month = 1
        Simulation.death_counter = 0
        while Simulation.month <= 12:
            for person in Simulation.people:
                if Simulation.month == 1:  # początek roku
                    person.accident_ratio()  # wyliczenie szansy na wypadek
                    person.setMonth(Simulation.month)  # ustawienie aktualnego miesiąca
                    person.count_cost()
                    person.pay()  # zapłacenie składki
                    Simulation.month_money += person.cost
                    person.age += 1
                    person.last_accident_counter -= 1
                    if person.last_accident_counter == 0:
                        person.last_accident = 0
                if person.check_if_accident(Simulation.rng.gen_random_between(0, Simulation.ACCIDENT_RANGE)):
                    Simulation.accident_counter += 1
                    Simulation.if_acc = 1  # Sprzezenie zwrotne czy osoba miala wypadek w tym miesiacu
                    Simulation.month_money -= person.accident_cost
                if person.check_death():
                    Simulation.death_counter += 1
                    Simulation.people.remove(person)  # usuwanie ubezpieczonego jeśli zginął

                Simulation.calculate_person(person)  # wliczanie osoby do danego przedzialu
                Simulation.if_acc = 0  # Reset sprzezenia
            Insurance.collected_money -= Insurance.employees * Insurance.SALARY  # wypłata pracowników ubezpieczalni

            Simulation.print_log()
            Simulation.month += 1
            Simulation.month_money = 0

        Simulation.year_counter += 1

        for i in range(Simulation.rng.gen_random_between(Simulation.death_counter - int(0.1*Simulation.death_counter),
                                                         Simulation.death_counter + int(0.1*Simulation.death_counter))):
            Simulation.people.append(Simulation.create_person())  # dodawanie nowego ubezpieczonego

    @staticmethod
    def create_population():
        """Utworzenie populacji"""
        for i in range(Simulation.population_size):
            Simulation.people.append(Simulation.create_person())

    @staticmethod
    def create_person():
        """Dodanie nowej osoby"""
        age = Simulation.rng.gen_random_between(18, 100)
        gender = Simulation.rng.gen_zero_or_one()
        car_cost = Simulation.rng.gen_random_between(5000, 50000)
        driver_exp_years = Simulation.rng.gen_random_between(0, age - 18)

        person = Person(age, gender, car_cost, driver_exp_years)
        return person

    @staticmethod
    def print_log():
        """Zapisywanie do pliku"""
        with open("log.txt", "a") as file:
            file.write(f"{Simulation.year_counter};{Simulation.month};{Simulation.month_money};"
                       f"{Simulation.below_equal_five};"
                       f"{round(Simulation.below_equal_five_age/Simulation.below_equal_five)};"
                       f"{Simulation.below_equal_five_acc}"
                       f"{Simulation.below_equal_seven};"
                       f"{round(Simulation.below_equal_seven_age/Simulation.below_equal_seven)};"
                       f"{Simulation.below_equal_five_acc}"
                       f"{Simulation.over_seven};"
                       f"{round(Simulation.over_seven_age/Simulation.over_seven)};"
                       f"{Simulation.over_seven_acc}\n")

        Simulation.below_equal_five = 0
        Simulation.below_equal_seven = 0
        Simulation.over_seven = 0
        Simulation.below_equal_five_acc = 0
        Simulation.below_equal_seven_acc = 0
        Simulation.over_seven_acc = 0
        Simulation.below_equal_five_age = 0
        Simulation.below_equal_seven_age = 0
        Simulation.over_seven_age = 0

    @staticmethod
    def calculate_person(person):

        person_cost = person.cost
        person_age = person.age

        if person_cost <= 500:
            Simulation.below_equal_five += 1
            if (Simulation.if_acc):
                Simulation.below_equal_five_acc += 1
            Simulation.below_equal_five_age += person_age

        elif (person_cost <= 700):
            Simulation.below_equal_seven += 1
            if (Simulation.if_acc):
                Simulation.below_equal_seven_acc += 1
            Simulation.below_equal_seven_age += person_age

        else:
            Simulation.over_seven += 1
            if (Simulation.if_acc):
                Simulation.over_seven_acc += 1
            Simulation.over_seven_age += person_age


Simulation.main()
