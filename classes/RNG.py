import random


class RNG:

    @staticmethod
    def random_between(a, b):
        """Losowanie liczby z przedziału"""
        return random.randint(a, b)
