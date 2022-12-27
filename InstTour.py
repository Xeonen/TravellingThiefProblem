import io
import regex as re
import numpy as np
import pandas as pd

class TwoOptInitTour:
    def __init__(self) -> None:
        pass
    
    def get_fitness(self, tour: np.array, dm: np.array) -> float:
        fitness: float = 0
        for i in range(tour.size -1):
            fitness = fitness + dm[tour[i]][tour[i+1]]             
        
        fitness = fitness + dm[tour[0]][tour[i+1]]
        return fitness
 
    def twoOpt(self, tour: np.array, dm: np.array) -> np.array:
        current_fitness = self.get_fitness(tour, dm)  
        for i in range(52):
            for k in range(i, 52):
                for j in range(k-i+1):
                    tour[i+j], tour[k-j] = tour[k-j], tour[i+j]
                    tmp_fitness = self.get_fitness(tour, dm)
                    if current_fitness > tmp_fitness:
                        current_fitness = tmp_fitness
                    else:
                        tour[k-j], tour[i+j] = tour[i+j], tour[k-j]

        return(tour)



class InstTour:
    def __init__(self, file_name: str) -> None:
        self.dimension = 0
        self.min_speed = 0
        self.max_speed = 0
        self.text = self.read_file(file_name)
        self.set_distance()
        self.set_distance_matrix()
        self.set_info()
    
    
    def read_file(self, file_name: str) -> str:
        with open(file_name, "r") as reader:
            text = reader.read()
        return(text)
    
    def set_distance(self) -> None:
        pattern = re.compile(r"Y\):([\s\w\W]*)ITEMS")
        self.distance = pattern.findall(self.text)[0]
        self.distance = pd.read_csv(io.StringIO(self.distance), sep="\t", index_col=0, header=None)
        self.distance.columns = ["X", "Y"]
        
    def set_info(self) -> None:
        pattern = re.compile(r"DIMENSION:\t([\d]*)")
        self.dimension = int(pattern.findall(self.text)[0])
        
        pattern = re.compile(r"MIN SPEED: \t([\d.]*)")
        self.min_speed = float(pattern.findall(self.text)[0])**(-1)

        pattern = re.compile(r"MAX SPEED: \t([\d.]*)")
        self.max_speed = float(pattern.findall(self.text)[0])**(-1)

    def calc_eucledian_distance(self, node1, node2) -> float:
        return ((node1.X - node2.X)**2 + (node1.Y - node2.Y)**2)**0.5
        
    def set_distance_matrix(self) -> None:
        self.distance_matrix = np.zeros(shape=(self.distance.shape[0], self.distance.shape[0]))
        for i in self.distance.index:
            for j in self.distance.index:
                self.distance_matrix[i-1][j-1] = self.calc_eucledian_distance(self.distance.loc[i], self.distance.loc[j])
                
    def calc_initial_fitness(self, tour: np.array) -> float:
        fitness: float = 0
        for i in range(tour.size -1):
            fitness = fitness + self.distance_matrix[tour[i]][tour[i+1]]                    
        fitness = fitness + self.distance_matrix[tour[0]][tour[i+1]]
        return(fitness)
    
    def generate_tour(self) -> np.array:
        opt = TwoOptInitTour()
        tour = np.array(range(self.get_dimension()))
        np.random.shuffle(tour)
        opt.twoOpt(tour, self.get_distance_matrix())
        # print("Initial Fitness:", self.calc_initial_fitness(tour))
        return(tour)
         
    def get_dimension(self) -> int:
        if self.dimension == 0:
            self.set_info()
        return self.dimension
    
    def get_distance_matrix(self) -> np.array:
        return self.distance_matrix

