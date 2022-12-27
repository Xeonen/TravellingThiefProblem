import numpy as np
from Species import Species



    
class TwoOpt:
    def __init__(self) -> None:
        pass
    
    def twoOptTour(self, org: Species) -> None:
        current_fitness, _ = org.calc_fitness(org.tour, org.knapsack)  
        for i in range(52):
            for k in range(i, 52):
                for j in range(k-i+1):
                    org.tour[i+j], org.tour[k-j] = org.tour[k-j], org.tour[i+j]
                    tmp_fitness, _ = org.calc_fitness(org.tour, org.knapsack)
                    if current_fitness > tmp_fitness:
                        current_fitness = tmp_fitness
                    else:
                        org.tour[k-j], org.tour[i+j] = org.tour[i+j], org.tour[k-j]
                        
        org.calc_fitness()
        
    def twoOptKS(self, org: Species) -> None:
        _, current_fitness = org.calc_fitness(org.tour, org.knapsack)  
        for i in range(52):
            for k in range(i, 52):
                for j in range(k-i+1):
                    org.knapsack[i+j], org.knapsack[k-j] = org.knapsack[k-j], org.knapsack[i+j]
                    tmp_fitness, _ = org.calc_fitness(org.tour, org.knapsack)
                    reverse = True
                    if org.instKS.is_valid(org.knapsack):
                        if current_fitness < tmp_fitness:
                            current_fitness = tmp_fitness
                            reverse = False
                    if reverse:
                        org.knapsack[k-j], org.knapsack[i+j] = org.knapsack[i+j], org.knapsack[k-j]
        org.calc_fitness()
        
