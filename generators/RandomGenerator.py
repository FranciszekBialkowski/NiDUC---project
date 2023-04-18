import time


class RandomGenerator:
    tab = []

    def __init__(self, in_seed=int(time.time())):
        self.m = 34359738368  # 2**35
        self.a = 3141592653  # π * 10^9
        self.c = 2718281829  # e * 10^9
        self.seed = in_seed
        self.seed_for_zero_one = 99999

    def gen_random_list(self, leng):
        while (leng):
            x = (self.a * self.seed + self.c) % self.m
            self.tab.append(x)
            self.seed = x

            leng -= 1
        return self.tab
    def gen_one_number(self, min, max):
        x = (self.a * self.seed + self.c) % self.m

        self.seed=x

        return (x % (max - min + 1)) + min

    def gen_zero_or_one(self):

        x = (self.a * self.seed + self.c) % self.m

        self.seed = x

        return (((x % ((self.seed_for_zero_one + 1)  + 1) ))) % 2

    def gen_random_between(self, min, max):
        x = (self.a * self.seed + self.c) % self.m

        return x % (max - min + 1) + min


# Tescik
random_gen = RandomGenerator()
for i in range(0,200):
    print(random_gen.gen_zero_or_one())
for i in range(0, 200):
    print(random_gen.gen_one_number(0,100))

#do sprawdzenia
# random_gen = RandomGenerator()
# print(random_gen.gen_random_list(10))

