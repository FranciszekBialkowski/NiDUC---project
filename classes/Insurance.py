class Insurance:
    base_cost = 0           # bazowy koszt ubezpieczenia
    collected_money = 0     # łączne, wpłacone pieniądze
    health_cost = 50        # dodatkowy koszt związany ze stanem zdrowia

    @staticmethod
    def count_final_cost(person):
        """Liczenie finalnego kosztu ubezpieczenia"""
        if person.if_healthy:
            return Insurance.base_cost + person.age
        return Insurance.base_cost + person.age + Insurance.health_cost

    @staticmethod
    def count_compensation(person):
        """Wyliczenie wysokości odszkodowania"""
        pass
