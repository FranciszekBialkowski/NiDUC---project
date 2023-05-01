from Insurance import Insurance
from RandomGenerator import RandomGenerator


class Person:
    MAX_ACC_RATIO = 10000  # maksymalna szansa na wypadek
    MAX_AGE_NUM = 2000  # maksymalna liczba zależna od wieku
    MAX_DRIVER_EXP = 4000  # maksymalna liczba zależna od doświadczenia
    MAX_MONTH = 1000  # maksymalna liczba zależna od aktualnego miesiąca
    MAX_VISION_DEFECT = 2000  # maksymalna liczba zależna od wady wzroku
    MAX_GENDER = 1000
    month = 1  # aktualny miesiąc
    accident_ratio_var = 0  # współczynnik szansy na wypadek
    last_accident = 0  # dodatkowy koszt związany z ostatnim wypadkiem
    cost = 0  # aktualny koszt składki
    random_value = RandomGenerator()  # obiekt klasy generatora liczb losowych

    def __init__(self, age, gender, car_cost, driver_exp_years):
        self.age = age  # wiek
        self.gender = gender  # płeć
        self.car_cost = car_cost  # koszt samochodu
        self.driver_exp_years = driver_exp_years  # doświadczenie
        self.vision_defect = self.set_vision_defect()  # wada wzroku
        self.count_cost()  # obliczenie kosztu składki

    def count_cost(self):
        """Wyliczanie aktualnego kosztu"""
        self.cost = Insurance.count_final_cost(self)

    def setMonth(self, month):
        """Ustawienie aktualnego miesiąca"""
        self.month = month

    def pay(self):
        """Zapłacenie miesięcznej składki"""
        Insurance.collected_money += self.cost

    def check_if_accident(self, random):
        """Sprawdzenie, czy nastąpił wypadek"""
        if random <= self.accident_ratio_var:
            if self.last_accident == 0:
                self.last_accident = int(self.cost * 0.15)

            self.last_accident += int(self.last_accident * 0.15)
            self.accident()
            return 1
        return 0

    def accident(self):
        """Akcja wykonywana, gdy nastąpi wypadek"""
        Insurance.collected_money -= Insurance.count_compensation(self.check_damage())

    def check_damage(self):
        """Obliczenie wysokości szkód"""
        x = self.random_value.gen_random_between(0, 100)
        if x < 15:  # 15%
            return self.car_cost  # cały samochód zniszczony
        else:  # 85%
            return int(x * self.car_cost / 100)  # samochód uszkodzony

    def set_vision_defect(self):
        """Sprawdzenie wystąpienia wady wzroku"""
        defect = self.random_value.gen_random_between(0, 100)
        if defect > 80:  # 80% na wystąpienie wady wzroku
            defect = 0
        else:
            defect = 1
        random_number = self.random_value.gen_random_between(0, 100)
        if self.age < 40:
            # Osoby poniżej 40 roku życia mają mniejsze szanse na wadę wzroku
            if random_number < 65:
                return defect
            else:
                return 0
        elif self.age < 60:
            # Osoby między 40 a 60 rokiem życia mają większą szansę na wadę wzroku
            if random_number < 80:
                return defect
            else:
                return 0
        else:
            # Osoby powyżej 60 roku życia mają bardzo duże szanse na wadę wzroku
            return defect

    def accident_ratio(self):
        """Coroczne wyliczanie współczynnika określającego szanse wypadku"""
        # Wywoływane na początku i przy zmianie stanu osoby

        self.accident_ratio_var = 0  # wyzerowanie szansy na wypadek

        # Wiek
        if 18 <= self.age <= 25:
            self.accident_ratio_var += 0.8 * self.MAX_AGE_NUM
        elif 26 <= self.age <= 39:
            self.accident_ratio_var += 0.1 * self.MAX_AGE_NUM
        elif 40 <= self.age <= 55:
            self.accident_ratio_var += 0.2 * self.MAX_AGE_NUM
        elif 56 <= self.age <= 69:
            self.accident_ratio_var += 0.5 * self.MAX_AGE_NUM
        elif 70 <= self.age <= 79:
            self.accident_ratio_var += 0.7 * self.MAX_AGE_NUM
        else:
            self.accident_ratio_var += self.MAX_AGE_NUM

        # Prawo jazdy
        if 0 <= self.driver_exp_years < 2:
            self.accident_ratio_var += 0.8 * self.MAX_DRIVER_EXP
        elif 2 <= self.age < 4:
            self.accident_ratio_var += 0.6 * self.MAX_DRIVER_EXP
        elif 4 <= self.age < 6:
            self.accident_ratio_var += 0.4 * self.MAX_DRIVER_EXP
        elif 6 <= self.age < 8:
            self.accident_ratio_var += 0.3 * self.MAX_DRIVER_EXP
        elif 8 <= self.age < 10:
            self.accident_ratio_var += 0.2 * self.MAX_DRIVER_EXP
        else:
            self.accident_ratio_var += 0.1 * self.MAX_DRIVER_EXP

        # Miesiąc
        if self.month == 1 or self.month == 8 or self.month == 11:
            self.accident_ratio_var += 0.2 * self.MAX_MONTH
        elif self.month == 2:
            pass
        elif self.month == 4 or self.month == 5 or self.month == 6 or self.month == 7:
            self.accident_ratio_var += 0.4 * self.MAX_MONTH
        elif self.month == 9 or self.month == 12:
            self.accident_ratio_var += 0.6 * self.MAX_MONTH
        elif self.month == 10:
            self.accident_ratio_var += self.MAX_MONTH

        # Wada wzroku
        if self.vision_defect == 0:
            pass
        else:
            self.accident_ratio_var += self.MAX_VISION_DEFECT

        # Płeć
        if self.gender == 0:
            self.accident_ratio_var += 0.71 * self.MAX_GENDER
        else:
            self.accident_ratio_var += self.MAX_GENDER
