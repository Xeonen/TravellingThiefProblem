# %%
import pickle
import pandas as pd
from Environment import Environment
# %%
with open("env.pickle", "rb") as reader:
    stuff = pickle.load(reader)
    
# %%
stuff
# %%
stuff.cycleDict.keys()
# %%
stuff.plotPareto(stuff.cycleDict[9])
# %%
def calc_hyperVol(df: pd.DataFrame, refX=1.1, refY=1.1) -> float:
    df = df.reset_index(drop=True)
    vol = 0
    vol = vol + (refX - df.loc[0, "f1"]) * (refY - df.loc[0, "f2"])
    for i in df.index:
        if i == 0:
            continue       
        vol = vol + (refX - df.loc[i, "f1"]) * (df.loc[i-1, "f2"] - df.loc[i, "f2"])   
    return(vol)
# %%
d = {"f1": [], "f2": []}
for i in stuff.cycleDict[9][0]:
    d["f1"].append(i.knapsack_fitness)
    d["f2"].append(i.tour_fitness)
df = pd.DataFrame(d)
# %%
df.describe()
# %%
calc_hyperVol(df, -30, 32000)
# %%
for key in stuff.cycleDict.keys():
    print(f"Cycle {key}")
    stuff.plotPareto(stuff.cycleDict[key])
# %%
