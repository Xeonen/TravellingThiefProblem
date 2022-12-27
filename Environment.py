# %%
import numpy as np 
from InstTour import InstTour
from InstKS import InstKS
from Species import Species
from TwoOpt import TwoOpt
from Mutate import Mutate
from Crossover import Crossover
from tqdm import tqdm
import matplotlib.pyplot as plt

import pickle
from copy import deepcopy

class Environment:
    def __init__(self, file_name: str, pop_size: int = 10, gen_limit: int = 10,
                 elitism_prop: float = 0.30, mutate_p: float = 0.25, mutations: float = 0.1) -> None:
        self.cycle = 0
        self.cycleDict = {}
        self.pop_size = pop_size
        self.gen_limit = gen_limit
        self.elitism_prop = elitism_prop
        self.mutate_p = mutate_p
        self.mutations = mutations
        self.file_name = file_name
        
        self.instKS = InstKS(file_name)
        self.instT = InstTour(file_name)
        self.mutator = Mutate()
        self.opt = TwoOpt()
        self.cross = Crossover()
        
        self.pop = self.gen_pop()
        self.next_gen = []
    
    def __str__(self) -> str:
        return("None")
    
    def gen_pop(self) -> np.array:
        pop = []
        pbar = tqdm(range(self.pop_size))
        pbar.set_description("Generating Population")        
        for _ in pbar:
            pop.append(Species(self.instT, self.instKS))
        return(pop)
            
    def sort_pop(self, type: str) -> None:
        if type == "tour":
            sorted(self.pop, key=Species.get_tour_fitness)
        else:
            sorted(self.pop, key=Species.get_knapsack_fitness)
            
    def elitism_tour(self) -> None:
        self.sort_pop("tour")
        point = int(self.pop_size*self.elitism_prop)
        rows = point // 2
        couples = np.random.choice(list(range(point)), (rows, 2), replace=False)
        
        self.crossing(couples, "elitism")
        couples = np.random.choice(list(range(point, self.pop_size)), (rows, 2), replace=False)              
        self.crossing(couples, "mediocracy")
        
    def crossing(self, couples, desc: str="mmmYeah") -> None:
        pbar = tqdm(couples) 
        pbar.set_description(f"Elitism Stage C: {self.cycle}:  {desc}")    
        for couple in pbar:
            p1 = np.random.randint(0, self.instT.get_dimension()-1)
            p2 = np.random.randint(p1, self.instT.get_dimension())
            
            parent_1 = self.pop[couple[0]]
            parent_2 = self.pop[couple[1]]
            child_tour_1, child_tour_2 = self.cross.crossover(parent_1.tour, parent_2.tour, p1, p2)
            child_1 = deepcopy(parent_1)
            child_2 = deepcopy(parent_2)
            child_3 = deepcopy(parent_1)
            child_4 = deepcopy(parent_2)
            child_1.tour = child_tour_1
            child_2.tour = child_tour_1      
            child_3.tour = child_tour_2
            child_4.tour = child_tour_2
            
            children = [child_1, child_2, child_3, child_4]
            for child in children:
                child.calc_fitness()
                self.next_gen.append(child)
            
    def mutation(self):
        self.sort_pop("knapsack")
        point = int(self.pop_size*self.elitism_prop)
        n = int(self.mutations*self.instKS.n_items)
        mutated = 0
        
        pbar = tqdm(range(self.pop_size)) 
        
        
        for i in pbar:
            pbar.set_description(f"Mutating Knapsacks M: {mutated} C: {self.cycle}") 
            if i > point and np.random.random() > self.mutate_p:
                continue
            else:
                mutated = mutated + 1
                try:
                    child = deepcopy(self.pop[i])
                    self.mutator.mutate(child, n)
                    self.next_gen.append(child)
                except Exception as e:
                    print(e)
                
    def twoOptification(self):
        pbar = tqdm(self.next_gen) 
        pbar.set_description(f"Two Optifying Next Gen C: {self.cycle}") 
        for org in pbar:
            self.opt.twoOptKS(org)
            self.opt.twoOptTour(org)
            
    def gen_mask(self, item):
        return(np.ones(len(item)) == 1)
    
    def gen_pareto(self):
        total = []
        total.extend(self.pop)
        total.extend(self.next_gen)
        self.pop = []
        self.next_gen = []
        total = sorted(total, key=Species.get_tour_fitness)
        total = np.array(total)
        
        paretoDict = {}
        paretoNum = 0
        
        while len(total) > 0:
            mask = self.gen_mask(total)
            for iOrg in range(len(total)-1):    
                for iComp in range(iOrg, len(total)):
                    if total[iOrg].get_knapsack_fitness() > total[iComp].get_knapsack_fitness():
                        mask[iComp] = False
            paretoDict[paretoNum] = total[mask]
            total = total[~mask]
            mask = self.gen_mask(total)
            paretoNum = paretoNum + 1
            
        self.paretoDict = paretoDict
        
    def unnatural_selection(self):

        self.gen_pareto()
        
        self.pop = []
        self.next_gen = []
        
        pbar = tqdm(self.paretoDict.keys())
        pbar.set_description(f"Unnatural Selection C: {self.cycle}:")
        for key in pbar:
            if len(self.paretoDict[key]) + len(self.pop) > self.pop_size:
                if key == 0:
                    self.pop.extend(self.paretoDict[key])
                    break
                else:
                    for _ in range(self.pop_size - len(self.pop)+1):
                        self.pop.append(Species(self.instT, self.instKS))
                    break
            else:
                self.pop.extend(self.paretoDict[key])
        self.cycleDict[self.cycle] = self.paretoDict
        
    def fit(self):
        for self.cycle in range(self.gen_limit):
            self.elitism_tour()
            self.mutation()
            self.twoOptification()
            self.unnatural_selection()
            # self.plotPareto()
        self.save_state()
    
    def plotPareto(self, paretoDict=None) -> None:
        NoneType = type(None)
        if isinstance(paretoDict, NoneType):
            paretoDict = self.paretoDict
            
        fig, ax = plt.subplots(1)
        fig.set_dpi(320)
        for key in paretoDict.keys():
            if key == 9:
                break
            X = []
            Y = []
            for i in paretoDict[key]:
                X.append(i.tour_fitness) 
                Y.append(i.knapsack_fitness)
            ax.scatter(X, Y, s=3, label=f"Front: {key}")
    
        # plt.xlim([0, 50000])
        # plt.ylim([0, -6000])
        plt.ylabel("Knapsack Fitness; More is Better")
        plt.xlabel("Tour Time; Less is Better")
        plt.legend()
        plt.show()
        
    def save_state(self):
        with open("env.pickle", "wb") as fWriter:
            pickle.dump(self, fWriter)
        print("Save Successful")
            
        
        
# %%  
if __name__ == "__main__":    
    env = Environment("berlin52_n51_bounded-strongly-corr_01.ttp", pop_size=5)
    env.fit()

# %%

    
# %%
