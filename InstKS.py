import io
import regex as re
import numpy as np
import pandas as pd


class InstKS:
    def __init__(self, file_name:str) -> None:
        self.text = self.read_file(file_name)
        self.gen_itemDF()
        self.gen_arrays()
        self.set_info()
        
    def __str__(self) -> str:
        text = f"""Capacity: {self.capacity}\n# Items: {self.n_items}\nRenting Ratio: {self.renting_ratio}"""
        return(text)

    def read_file(self, file_name: str) -> str:
        with open(file_name, "r") as reader:
            text = reader.read()
        return(text)
    
    def set_info(self) -> None:
        pattern = re.compile(r"CAPACITY OF KNAPSACK: \t([\d]*)")
        self.capacity = int(pattern.findall(self.text)[0])
        
        pattern = re.compile(r"RENTING RATIO: \t([\d.]*)")
        self.renting_ratio = float(pattern.findall(self.text)[0])

        pattern = re.compile(r"NUMBER OF ITEMS: \t([\d.]*)")
        self.n_items = int(pattern.findall(self.text)[0]) + 1
    
    def gen_itemDF(self):
        pattern = re.compile(r"NODE NUMBER\): \n([\s\n\W\w]+)\n")
        tempText = pattern.findall(self.text)[0]
        self.itemDF = pd.read_csv(io.StringIO(tempText), sep="\t", index_col= 0, header=None)
        self.itemDF.columns = ["profit", "weight", "node"]
        
    def gen_arrays(self):
        self.profit = np.zeros(shape=self.itemDF.shape[0]+1)
        self.weight = np.zeros(shape=self.itemDF.shape[0]+1)
        
        for i in self.itemDF.index:
            self.profit[i] = self.itemDF.loc[i, "profit"]
            self.weight[i] = self.itemDF.loc[i, "weight"]
            
    def gen_knapsack(self) -> np.array:
        knapsack = np.array(np.zeros(shape=(self.n_items)), dtype=bool)
        while self.is_valid(knapsack):
            idx = np.random.randint(0, self.n_items)
            knapsack[idx] = not knapsack[idx]
        knapsack[idx] = not knapsack[idx]
        
        return(knapsack)
        
    

    
    
    
    def is_valid(self, knapsack: np.array) -> bool:
        valid = False
        if np.sum(self.weight[knapsack]) <= self.capacity:
            valid = True
        return(valid)
            
            
# ks = InstKS("berlin52_n51_bounded-strongly-corr_01.ttp")
# print(ks)

# knapsack = ks.gen_knapsack()
# print(knapsack)
# print("x")