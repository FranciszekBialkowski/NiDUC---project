# liniowymi generatorami kongruencyjnymi liczb pseudolosowych, z modyfikacjami poprawiajcymi losowosc(duzy okres
# powtarzania sekswencji, wykorzystanie zegara czasu rzeczywistego do tworzenia ziarna

import time


class RandomGenerator:
    tab = []

    def __init__(self, in_seed=int(time.time())):
        self.m = 34359738368  # 2**35
        self.a = int(3.14159265358979323846 * 1e9)  # π * 10^9
        self.c = int(2.71828182845904523536 * 1e9)  # e * 10^9
        self.seed = in_seed

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
        return x


#Tescik
# random_gen = RandomGenerator()
# for i in range(0,100):
#     print(random_gen.gen_one_number(1, 10))
