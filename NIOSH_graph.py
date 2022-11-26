import sys
import NIOSH as nc
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import numpy as np

class Graph:
    def __init__(self, horizontalMulti, verticalMulti, DistMulti, cm, weight):
        self.horizontialMulti = nc.HMFactor(horizontalMulti)
        self.verticalMulti = nc.VMFactor(verticalMulti)
        self.DistMulti = nc.DMFactor(DistMulti)
        self.cm = nc.couplingMultiplier(cm)
        self.weight = weight

    def create_weight_array(self,weight_arr):
        inital_weight = (int(self.weight)- 10)
        while inital_weight <= (int(self.weight) + 10):
            if(inital_weight >= 0):
                weight_arr.append(inital_weight)
                inital_weight += 1

    def create_risk_array(self,good_risk_index_arr, fair_risk_ar, poor_risk_ar,weight_arr):
        for w in weight_arr:
            good_calc = nc.Calc(self.horizontialMulti,self.verticalMulti,self.DistMulti,"Good", w)
            good_risk = good_calc.liftingIndex()
            good_risk_index_arr.append(good_risk)
            fair_calc = nc.Calc(self.horizontialMulti,self.verticalMulti,self.DistMulti,"Fair", w)
            fair_risk = fair_calc.liftingIndex()
            fair_risk_ar.append(fair_risk)
            poor_calc = nc.Calc(self.horizontialMulti,self.verticalMulti,self.DistMulti,"Poor", w)
            poor_risk = poor_calc.liftingIndex()
            poor_risk_ar.append(poor_risk)


def main():
    #test of the functions 
    hm = input("Please enter the Horizontal Multiplier: ")
    vm = input("Please enter the Vertical Multiplier: ")
    dm = input("Please enter the Distance Multiplier: ")
    cm = input("Please enter the coupling Multiplier: ")

    #take in the weight for the lifting index
    weightOfObj = input("Please enter the weight of the object: ")


    #initalize graph
    graph = Graph(hm,vm,dm,cm,weightOfObj)
    weight_ar = []
    graph.create_weight_array(weight_ar)
    good_risk_ar = []
    fair_risk_ar = []
    poor_risk_ar = []
    #take in three arrays and output for the graphs y's based om weight
    graph.create_risk_array(good_risk_ar, fair_risk_ar, poor_risk_ar, weight_ar)



    #create a graph
    plt.plot(weight_ar, good_risk_ar, 'g-', label='Good Coupling of Box')
    plt.plot(weight_ar, fair_risk_ar, 'g:', label='Fair Coupling of Box')
    plt.plot(weight_ar, poor_risk_ar, 'g--', label='Poor Coupling of Box')
    # red line for when risk is above 1
    plt.axhline(y = 1, color = 'r', linestyle = '-', label = "High Risk") 
    #x and y lables
    plt.xlabel("Weight of Box (lbs)")
    plt.ylabel("Risk Index of NIOSH")
    plt.legend()
    plt.show()
