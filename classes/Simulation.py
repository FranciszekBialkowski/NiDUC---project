from Person import Person
from RNG import RNG


class Simulation:
    population_size = 10    # wielkość populacji
    people = []             # tablica przechowująca populację
    time = 20               # ilość miesięcy w symulacji

    @staticmethod
    def main():
        """Start symulacji"""
        Simulation.create_population()
        for i in range(Simulation.time):
            Simulation.month()

    @staticmethod
    def month():
        """Akcja wykonywana co miesiąc"""
        for person in Simulation.people:
            person.pay()
            person.check_if_accident()

    @staticmethod
    def create_population():
        """Utworzenie populacji"""
        for i in range(Simulation.population_size):
            Simulation.people.append(Person(RNG.random_between(18, 100), RNG.random_between(0, 1)))


Simulation.main()
