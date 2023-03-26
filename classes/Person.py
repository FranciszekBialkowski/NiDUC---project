from Insurance import Insurance


class Person:

    def __init__(self, age, if_healthy):
        self.age = age                                  # wiek
        self.if_healthy = if_healthy                    # stan zdrowia
        self.cost = Insurance.count_final_cost(self)    # koszt odszkodowania

    def pay(self):
        """Zapłacenie miesięcznej składki"""
        Insurance.collected_money += self.cost

    def check_if_accident(self):
        """Sprawdzenie, czy nastąpił wypadek"""
        pass

    def accident(self):
        """Akcja wykonywana, gdy nastąpi wypadek"""
        Insurance.collected_money -= Insurance.count_compensation(self)
