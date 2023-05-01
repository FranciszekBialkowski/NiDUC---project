import time


class RandomGenerator:

    def __init__(self, in_seed=int(time.time())):
        self.m = 34359738368  # 2**35
        self.a = 3141592653  # π * 10^9
        self.c = 2718281829  # e * 10^9
        self.seed = in_seed
        self.seed_for_zero_one = 99999

    def gen_random_between(self, min_val, max_val):
        """Losowanie liczby z zadanego przedziału"""
        x = (self.a * self.seed + self.c) % self.m

        self.seed = x

        return (x % (max_val - min_val + 1)) + min_val

    def gen_zero_or_one(self):
        """Losowanie wartości 0/1"""
        x = (self.a * self.seed + self.c) % self.m

        self.seed = x

        return (x % ((self.seed_for_zero_one + 1) + 1)) % 2
