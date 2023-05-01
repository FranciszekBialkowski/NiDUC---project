class Insurance:
    BASE_COST = 250  # bazowy koszt ubezpieczenia
    collected_money = 0  # pieniądze ubezpieczalni
    employees = 220  # ilość pracowników ubezpieczalni
    SALARY = 3490  # wysokość wypłaty pracownika
    PEOPLE_PER_EMPLOYEE = 10000  # ilość osób na jednego pracownika
    NEW_DRIVER_COST = 100

    @staticmethod
    def count_final_cost(person):
        """Liczenie finalnego kosztu ubezpieczenia"""
        if person.driver_exp_years < 5:
            return Insurance.BASE_COST + person.last_accident + int(person.car_cost * 0.01) + Insurance.NEW_DRIVER_COST
            # koszt wiekszy dla nowych kierowców
        return Insurance.BASE_COST + person.last_accident + int(person.car_cost * 0.01) # min 300, max 750 + last_accident

    @staticmethod
    def count_compensation(damage_cost):
        """Wyliczenie wysokości odszkodowania"""
        return damage_cost
