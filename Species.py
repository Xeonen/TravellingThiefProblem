import numpy as np

from InstKS import InstKS
from InstTour import InstTour


class Species:
    def __init__(self, instT: InstTour, instKS: InstKS) -> None:
        self.instT = instT
        self.instKS = instKS
        self.generate_tour()
        self.generate_knapsack()
        self.tour_fitness, self.knapsack_fitness = self.calc_fitness(self.tour, self.knapsack)
        # print(self.tour_fitness, self.knapsack_fitness)
        
    def __str__(self) -> str:
        text = f"Tour Fitness: {round(self.tour_fitness, 4)}\t\tKnapsack Fitness: {round(self.knapsack_fitness,4)}"
        return(text)
    
    def get_tour_fitness(self):
        return(self.tour_fitness)
    
    def get_knapsack_fitness(self):
        return(self.knapsack_fitness)
    
    def generate_tour(self):
        self.tour = self.instT.generate_tour()
        
    def generate_knapsack(self):
        self.knapsack = self.instKS.gen_knapsack()

        
    
    def calc_speed(self, weight):
        
        # snewValue = (((oldValue - oldMin)* (newMax - newMin)) / (oldMax - oldMin)) + newMin
        speed =  (((weight - 0)* (self.instT.min_speed - self.instT.max_speed)) / (self.instKS.capacity - 0)) + self.instT.max_speed
        return(speed)
    
    def calc_fitness(self, tour: np.array = None, knapsack: np.array = None) -> tuple:
        NoneType = type(None)
        if isinstance(tour, NoneType) or isinstance(knapsack, NoneType):
            tour = self.tour
            knapsack = self.knapsack
        
        KS_fitness = 0
        tour_fitness = 0
        weight = 0
        speed = self.instT.max_speed
        for i in range(tour.shape[0] -1):
            c1 = tour[i]-1
            c2 = tour[i+1]-1
            steal = knapsack[c1]
            if steal:
                weight = weight + self.instKS.weight[c1]
                speed = self.calc_speed(weight)
                KS_fitness = KS_fitness + self.instKS.profit[c1]
            time = self.instT.distance_matrix[c1, c2]*speed 
            KS_fitness = KS_fitness - time*self.instKS.renting_ratio
            tour_fitness = tour_fitness + time
            
        self.tour_fitness = tour_fitness
        self.knapsack_fitness = KS_fitness
        return(tour_fitness, KS_fitness)
        

