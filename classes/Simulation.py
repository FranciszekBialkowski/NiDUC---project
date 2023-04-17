from Person import Person
from RandomGenerator import RandomGenerator
from Insurance import Insurance
import time


class Simulation:
    population_size = 2000  # wielkość populacji
    people = []  # tablica przechowująca populację
    time = 10  # ilość lat w symulacji
    rng = RandomGenerator()

    @staticmethod
    def main():
        """Start symulacji"""
        Simulation.create_population()
        for i in range(Simulation.time):
            Simulation.year()
        print(f"Końcowe pieniądze ubezpieczalni: {Insurance.collected_money}")

    @staticmethod
    def year():
        """Akcja wykonywana co rok"""
        month_counter = 1  # licznik miesięcy
        while month_counter <= 12:
            for person in Simulation.people:
                if month_counter == 1:  # początek roku
                    person.pay()  # zapłacenie składki
                person.check_if_accident(Simulation.rng.gen_random_between(0, Person.MAX_ACC_RATIO))

            Insurance.collected_money -= Insurance.employees * Insurance.salary  # wypłata pracowników ubezpieczalni
            month_counter += 1

    @staticmethod
    def create_population():
        """Utworzenie populacji"""
        for i in range(Simulation.population_size):
            # losowanie cech
            age = Simulation.rng.gen_random_between(18, 100)
            if_healthy = Simulation.rng.gen_random_between(0, 1)
            gender = Simulation.rng.gen_random_between(0, 1)
            car_cost = Simulation.rng.gen_random_between(5000, 200000)
            driver_exp_years = Simulation.rng.gen_random_between(0, age - 18)

            print(f"Person{i}: {age},{if_healthy},{gender},{car_cost},{driver_exp_years}")

            # dodanie osoby do listy
            Simulation.people.append(Person(age, if_healthy, gender, car_cost, driver_exp_years))

            Simulation.rng.gen_random_list(1)  # ta linijka do usunięcia


Simulation.main()
