import numpy as np
from copy import deepcopy

class Crossover:
    def __init__(self) -> None:
        pass
    def crossover(self, parent_one: np.array, parent_two: np.array, p1: int, p2: int):

        child_one = deepcopy(parent_one)
        child_two = deepcopy(parent_two)
        child_one[p1:p2] = parent_two[p1:p2]
        child_two[p1:p2] = parent_one[p1:p2]
        
        d1 = {}
        d2 = {}
        
        for i in range(p1, p2):
            d1[parent_two[i]] = parent_one[i]
            d2[parent_one[i]] = parent_two[i]
            
        self.generate_children(child_one, p1, p2, d1, d2)
        self.generate_children(child_two, p1, p2, d2, d1)
        
        return(child_one, child_two)
        
            
    def generate_children(self, child: np.array, p1: int, p2: int, d1: dict, d2: dict) -> np.array:     
        counter = 0
        n = child.shape[0]
        for i in range(p2-n, p1):
            num = d1.get(child[i], -1)
            if d2.get(child[i], -1) != -1:
                counter += 1
                continue
            
            while True:
                tmp = d1.get(num, -1)
                if tmp == -1:
                    break
                else:
                    counter += 1
                    num = tmp
            
            if num != -1:
                child[i] = num
            if p2 - p1 == counter:
                break
            
        return(child)