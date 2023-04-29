from Person import Person
from RandomGenerator import RandomGenerator
from Insurance import Insurance
import re


class Simulation:
    population_size = Insurance.employees * Insurance.PEOPLE_PER_EMPLOYEE  # wielkość populacji
    people = []  # tablica przechowująca populację
    time = 1  # ilość lat w symulacji
    rng = RandomGenerator()
    month = 1  # aktualny miesiąc
    ACCIDENT_RANGE = 50000000  # zakres losowania
    accident_counter = 0  # ilość wypadków
    death_counter = 0  # liczba osób, które zginęły
    new_people_chance = 90  # szansa na przyjście nowej osoby (jeszcze do okreslenia)

    @staticmethod
    def main():
        """Start symulacji"""
        Simulation.create_population()
        for i in range(Simulation.time):
            Simulation.year()

        print("Końcowe pieniądze ubezpieczalni:", re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(Insurance.collected_money)))
        print(f"Ilość wypadków: {Simulation.accident_counter}")
        print(f"ile zginęło: {Simulation.death_counter}")
        print(f"Populacja: {len(Simulation.people)}")

    @staticmethod
    def year():
        """Akcja wykonywana co rok"""
        while Simulation.month <= 12:
            for person in Simulation.people:
                if Simulation.month == 1:  # początek roku
                    person.accident_ratio()  # wyliczenie szansy na wypadek
                    person.setMonth(Simulation.month)  # ustawienie aktualnego miesiąca
                    person.pay()  # zapłacenie składki
                if person.check_if_accident(Simulation.rng.gen_random_between(0, Simulation.ACCIDENT_RANGE)):
                    Simulation.accident_counter += 1
                if person.check_death():
                    Simulation.death_counter += 1
                    Simulation.people.remove(person)  # usuwanie ubezpieczonego jeśli zginął
            if Simulation.rng.gen_random_between(0, 100) < Simulation.new_people_chance:
                Simulation.people.append(Simulation.create_person())  # dodawanie nowego ubezpieczonego

            Insurance.collected_money -= Insurance.employees * Insurance.SALARY  # wypłata pracowników ubezpieczalni
            Simulation.month += 1

    @staticmethod
    def create_population():
        """Utworzenie populacji"""
        for i in range(Simulation.population_size):
            Simulation.people.append(Simulation.create_person())

    @staticmethod
    def create_person():
        # losowanie cech
        age = Simulation.rng.gen_random_between(18, 100)
        gender = Simulation.rng.gen_zero_or_one()
        car_cost = Simulation.rng.gen_random_between(5000, 50000)
        driver_exp_years = Simulation.rng.gen_random_between(0, age - 18)

        person = Person(age, gender, car_cost, driver_exp_years)
        return person


Simulation.main()
