class Insurance:
    BASE_COST = 250  # bazowy koszt ubezpieczenia
    collected_money = 0  # pieniądze ubezpieczalni
    employees = 220  # ilość pracowników ubezpieczalni
    SALARY = 3490  # wysokość wypłaty pracownika
    PEOPLE_PER_EMPLOYEE = 1000  # ilość osób na jednego pracownika

    @staticmethod
    def count_final_cost(person):
        """Liczenie finalnego kosztu ubezpieczenia"""
        return Insurance.BASE_COST + person.last_accident + int(person.car_cost * 0.01)  # do zmiany

    @staticmethod
    def count_compensation(damage_cost):
        """Wyliczenie wysokości odszkodowania"""
        return damage_cost
