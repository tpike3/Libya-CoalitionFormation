# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 05:36:49 2018

@author: ymamo

Executes Libya coalition formation using bilateral Shapley value
"""

from libya_coalition.bilateralShapley import Attachment
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd 

#Empyt lists for outputs
tribes = []
results = []
#Compromise parameter
comps = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.00]
#Marginal effecitvness parameter
eff  = [1.1, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.7, 1.8, 1.9, 2.0, 3]
#Tribal inputs
tribe_input = "libya_coalition/Groups_Support_Many.csv"
 #"libya_coalition/Groups.csv", "libya_coalition/Groups_Support_One.csv"   ---other input folders

t = 0
for x in comps:
    for y in eff: 
        test = Attachment(x,y,t, tribe_input)
        res, tris = test.execution()
        results.append(res)
        tribes.append(tris)
        t += 1
        print (t)
        #plt.clf()
        #nx.draw(test.population.groups)
        #plt.show()
out = pd.concat(results, ignore_index= True)
out2 = pd.concat(tribes, ignore_index=True)
out.to_csv( "allianceresults_many" + '.csv', encoding = 'utf-8')
out2.to_csv("alliancetribes_many" + ".csv", encoding = 'utf-8')