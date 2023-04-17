class Insurance:
    BASE_COST = 50  # bazowy koszt ubezpieczenia
    collected_money = 0  # łączne, wpłacone pieniądze
    health_cost = 50  # dodatkowy koszt związany ze stanem zdrowia
    employees = 5   # ilość pracowników ubezpieczalni
    salary = 3000   # wysokość wypłaty pracownika

    @staticmethod
    def count_final_cost(person):
        """Liczenie finalnego kosztu ubezpieczenia"""
        if person.if_healthy:
            return Insurance.BASE_COST + person.age
        return Insurance.BASE_COST + person.age + Insurance.health_cost

    @staticmethod
    def count_compensation(person, if_fault, damage_cost):
        """Wyliczenie wysokości odszkodowania"""
        if if_fault:
            return 100 + damage_cost
        return 1000 + damage_cost
