import numpy as np
from Species import Species


class Mutate:
    def __init__(self) -> None:
        pass
    
    def mutate(self, org: Species, n: int = 1, tries: int = 100):
        for _ in range(n):
            counter = 0
            trigger = True
            while trigger or tries > counter:
                tries = counter = counter + 1
                idx = np.random.randint(0, org.instKS.n_items)
                org.knapsack[idx] = not org.knapsack[idx]            
                if org.instKS.is_valid(org.knapsack):
                    trigger = False
                else:
                    org.knapsack[idx] = not org.knapsack[idx]
        org.calc_fitness()
                    