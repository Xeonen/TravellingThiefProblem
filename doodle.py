# %%
import numpy as np 
from InstTour import InstTour
from InstKS import InstKS
from Species import Species
from TwoOpt import TwoOpt
from Mutate import Mutate
from Crossover import Crossover
from tqdm import tqdm

import pickle

with open("total.pickle", "rb") as fileReader:
    total = pickle.load(fileReader)
  
# %%

total = sorted(total, key=Species.get_tour_fitness)
total = np.array(total, dtype=Species)
paretoDict = {}
paretoNum = 0
def gen_mask(item):
    return(np.ones(len(item)) == 1)
    
while len(total) > 0:
    mask = gen_mask(total)
    for iOrg in range(len(total)-1):    
        for iComp in range(iOrg, len(total)):
            if total[iOrg].get_knapsack_fitness() > total[iComp].get_knapsack_fitness():
                mask[iComp] = False
    paretoDict[paretoNum] = total[mask]
    total = total[~mask]
    mask = gen_mask(total)
    paretoNum = paretoNum + 1
# %%
for key in paretoDict.keys():
    print(f"Pareto: {key}\tSize: {len(paretoDict[key])}")

# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
for key in paretoDict.keys():
    if key == 9:
        break
    X = []
    Y = []
    for i in paretoDict[key]:
        X.append(i.tour_fitness) 
        Y.append(i.knapsack_fitness)
    ax.scatter(X, Y, s=5, label=f"Front: {key}")
    
# plt.xlim([0, 50000])
plt.ylim([0, -6000])
plt.ylabel("Knapsack Fitness; More is Better")
plt.xlabel("Tour Time; Less is Better")
plt.legend()
plt.show()
# %%
