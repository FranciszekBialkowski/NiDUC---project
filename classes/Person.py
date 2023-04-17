from Insurance import Insurance


class Person:
    MAX_ACC_RATIO = 10000  # maksymalna szansa na wypadek
    MAX_AGE_NUM = 1000  # maksymalna liczba zależna od wieku
    MAX_DRIVER_EXP = 1000  # maksymalna liczba zależna od doświadczenia

    def __init__(self, age, if_healthy, gender, car_cost, driver_exp_years):
        self.age = age  # wiek
        self.gender = gender  # płeć
        self.if_healthy = if_healthy  # stan zdrowia
        self.car_cost = car_cost  # koszt samochodu
        self.driver_exp_years = driver_exp_years  # doświadczenie
        self.accident_ratio_var = 0  # szansa na wypadek
        self.cost = Insurance.count_final_cost(self)  # koszt odszkodowania

    def pay(self):
        """Zapłacenie miesięcznej składki"""
        Insurance.collected_money += self.cost

    def check_if_accident(self, random):
        """Sprawdzenie, czy nastąpił wypadek"""
        if random < self.accident_ratio_var * 100:
            self.accident(random)

    def accident(self, random):
        """Akcja wykonywana, gdy nastąpi wypadek"""
        if_fault = random % 2
        Insurance.collected_money -= Insurance.count_compensation(self, if_fault, self.check_damage(random))

    def check_damage(self, random):
        """Obliczenie wysokości szkód"""
        x = random % 100  # <--------------------------
        if x < 5:  # 5%
            return self.car_cost  # cały samochód zniszczony
        else:  # 95%
            return int(x * self.car_cost / 100)  # samochód uszkodzony

    def accident_ratio(self):
        """Wyliczanie współczynnika określający szanse wypadku"""
        # Wywoływane przy w konstruktorze i przy zmianie stanu osoby
        self.accident_ratio_var = 0
        # Wiek
        if 18 <= self.age <= 24:
            self.accident_ratio_var += 0.4 * self.MAX_AGE_NUM
        elif 25 <= self.age <= 39:
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
