from Person import Person
from RandomGenerator import RandomGenerator
from Insurance import Insurance
from Visualisation import Visualisation
import re


class Simulation:
    if_visualisation = False
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
    month_expenses = 0
    men_acc = 0
    women_acc = 0

    young_people = 0    # liczba młodych ludzi
    middle_people = 0   # liczba ludzi w średnim wieku
    old_people = 0      # liczba starych ludzi

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
        file = open("log1.txt", "w+")
        file.write(f"Rok;Miesiąc;Zarobki;Wydatki;"
                   f"Liczba osób_<500;Średni wiek_<500;Liczba wypadków_<500;"
                   f"Liczba osób_500-700;Średni wiek_500-700;Liczba wypadków_500-700;"
                   f"Liczba osób_>700;Średni wiek_>700;Liczba wypadków_>700;"
                   f"Liczba wypadków mężczyzn;Liczba wypadków kobiet\n")
        file.close()
        """Start symulacji"""
        Simulation.create_population()
        if Simulation.if_visualisation:
            Visualisation.start_visualisation()
        for i in range(Simulation.time):
            Simulation.year()

        print("Końcowe pieniądze ubezpieczalni:",
              re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(Insurance.collected_money)), "zl")
        print(f"Populacja: {len(Simulation.people)}")

    @staticmethod
    def year():
        """Akcja wykonywana co rok"""
        Simulation.month = 1
        Simulation.death_counter = 0
        while Simulation.month <= 12:
            for person in Simulation.people:
                person.setMonth(Simulation.month)  # ustawienie aktualnego miesiąca
                if Simulation.month == 1:  # początek roku
                    person.accident_ratio()  # wyliczenie szansy na wypadek
                    person.count_cost()
                    person.pay()  # zapłacenie składki
                    Simulation.month_money += person.cost
                    person.age += 1
                    person.last_accident_counter -= 1
                    if person.last_accident_counter == 0:
                        person.last_accident = 0
                if person.check_if_accident(Simulation.rng.gen_random_between(0, Simulation.ACCIDENT_RANGE)):
                    if Simulation.if_visualisation:
                        Visualisation.add_unit_to_section("accident", person.gender)

                    Simulation.accident_counter += 1
                    Simulation.if_acc = 1  # Sprzezenie zwrotne czy osoba miala wypadek w tym miesiacu
                    Simulation.month_expenses += person.accident_cost
                    if person.gender == 1:
                        Simulation.men_acc += 1
                    else:
                        Simulation.women_acc += 1

                if person.check_death():
                    if Simulation.if_visualisation:
                        Visualisation.add_unit_to_section("death", person.gender)
                        Visualisation.remove_unit_from_section("people", person.gender)

                    Simulation.death_counter += 1
                    Simulation.people.remove(person)  # usuwanie ubezpieczonego, jeśli zginął

                if 18 <= person.age <= 38:
                    Simulation.young_people += 1
                if 39 <= person.age <= 69:
                    Simulation.middle_people += 1
                if 70 <= person.age:
                    Simulation.old_people += 1

                Simulation.calculate_person(person)  # wliczanie osoby do danego przedzialu
                Simulation.if_acc = 0  # Reset sprzezenia
            if Simulation.if_visualisation:
                Visualisation.age_young_counter = Simulation.young_people
                Visualisation.age_middle_counter = Simulation.middle_people
                Visualisation.age_old_counter = Simulation.old_people
                Visualisation.start_visualisation()

            Insurance.collected_money -= Insurance.employees * Insurance.SALARY  # wypłata pracowników ubezpieczalni
            if Simulation.if_visualisation:
                Visualisation.budget = Insurance.collected_money
            Simulation.month_expenses += Insurance.employees * Insurance.SALARY

            Simulation.print_log()
            Simulation.month += 1
            Simulation.month_money = 0
            Simulation.month_expenses = 0

        Simulation.year_counter += 1

        for i in range(Simulation.rng.gen_random_between(Simulation.death_counter - int(0.1 * Simulation.death_counter),
                                                         Simulation.death_counter + int(
                                                             0.1 * Simulation.death_counter))):
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
        if Simulation.if_visualisation:
            Visualisation.add_unit_to_section("people", gender)
            if 18 <= person.age <= 35:
                Visualisation.add_unit_to_section("young", gender)
            if 36 <= person.age <= 69:
                Visualisation.add_unit_to_section("middle", gender)
            if 70 <= person.age:
                Visualisation.add_unit_to_section("old", gender)
        return person

    @staticmethod
    def print_log():
        """Zapisywanie do pliku"""
        below_equal_five_avg_age = round(Simulation.below_equal_five_age / Simulation.below_equal_five) \
            if Simulation.below_equal_five > 0 else 0
        below_equal_seven_avg_age = round(Simulation.below_equal_seven_age / Simulation.below_equal_seven) \
            if Simulation.below_equal_seven > 0 else 0
        over_seven_avg_age = round(Simulation.over_seven_age / Simulation.over_seven) \
            if Simulation.over_seven > 0 else 0

        with open("log1.txt", "a") as file:
            file.write(f"{Simulation.year_counter};{Simulation.month};"  # rok, miesiąc
                       f"{Simulation.month_money};{Simulation.month_expenses};"  # zarobki, wydatki
                       f"{Simulation.below_equal_five};"  # liczba osób w grupie 1
                       f"{below_equal_five_avg_age};"  # średni wiek w grupie 1
                       f"{Simulation.below_equal_five_acc};"  # liczba wypadków w grupie 1
                       f"{Simulation.below_equal_seven};"  # liczba osób w grupie 2
                       f"{below_equal_seven_avg_age};"  # średni wiek w grupie 2
                       f"{Simulation.below_equal_seven_acc};"  # liczba wypadków w grupie 2
                       f"{Simulation.over_seven};"  # liczba osób w grupie 3
                       f"{over_seven_avg_age};"  # średni wiek w grupie 3
                       f"{Simulation.over_seven_acc};"  # liczba wypadków w grupie 3
                       f"{Simulation.men_acc};"  # liczba wypadków mężczyzn
                       f"{Simulation.women_acc}\n")  # liczba wypadków kobiet

        Simulation.below_equal_five = 0
        Simulation.below_equal_seven = 0
        Simulation.over_seven = 0
        Simulation.below_equal_five_acc = 0
        Simulation.below_equal_seven_acc = 0
        Simulation.over_seven_acc = 0
        Simulation.below_equal_five_age = 0
        Simulation.below_equal_seven_age = 0
        Simulation.over_seven_age = 0
        Simulation.men_acc = 0
        Simulation.women_acc = 0

    @staticmethod
    def calculate_person(person):

        person_cost = person.cost
        person_age = person.age

        if person_cost <= 500:
            Simulation.below_equal_five += 1
            if Simulation.if_acc:
                Simulation.below_equal_five_acc += 1
            Simulation.below_equal_five_age += person_age

        elif person_cost <= 700:
            Simulation.below_equal_seven += 1
            if Simulation.if_acc:
                Simulation.below_equal_seven_acc += 1
            Simulation.below_equal_seven_age += person_age

        else:
            Simulation.over_seven += 1
            if Simulation.if_acc:
                Simulation.over_seven_acc += 1
            Simulation.over_seven_age += person_age


if_visualisation_input = input("Czy chcesz wyświetlić wizualizacje (T/N): ")

while if_visualisation_input not in ['t', 'T', 'n', 'N']:
    if_visualisation_input = input("Czy chcesz wyświetlić wizualizacje (T/N): ")

if if_visualisation_input in ['t', 'T']:
    Simulation.if_visualisation = True
else:
    print("Symulacja trwa...")

Simulation.main()
