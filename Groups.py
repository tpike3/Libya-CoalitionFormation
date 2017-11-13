# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 09:19:15 2017

@author: ymamo
"""

import pandas as pd
import networkx as nx
import numpy as np

class groups_est(object):
    
    def __init__(self):
        #create dictionary of all the groups with affinity
        group_names, affinity, power = self.read_in()
        self.groups = self.net(group_names, affinity, power)
        self.ref = self.refdict(group_names, affinity, power)
        #print (self.groups)

    def read_in(self): 
    
        group_data = pd.read_csv("Groups_Support_Many.csv")
        
        #put group data in list
        group_names = group_data["Tribe"].tolist()

        #put affinity data in list
        affinity = group_data["Affinity"].tolist()
        #normalize affinity
        affinity = list(map(lambda x: x/max(affinity), affinity))
        #print (affinity)
        #affinity = list(np.random.power(10, size = len(group_names)))
        
        #economic power- should be read in needs normalization statement when done
        #print (np.random.power(1, size =len(group_names)))
        #economic_resources = list(np.random.power(1, size = len(group_names)))
        #print (economic_resources)
        #print ("economic:", economic_resources)
        #put economic resources in list
        economic_resources = group_data["Economic Resources"].tolist()
        #normalize economic resources
        #economic_resources = list(map(lambda x: x/max(economic_resources), economic_resources))
                
        #military capability - should be read in 
        #military_capability = (np.random.power(1, size = len(group_names)))
        #print (military_capability
        #put military capability in list
        military_capability = group_data["Military Capability"].tolist()
        #normalize military cpability of all the groups
        #military_capability = list(map(lambda x: x/max(military_capability), military_capability))
        
        
        #create power of each group and normalize
        #print (np.amax(economic_resources), np.amax(military_capability))
        power = list(map(lambda x,y: (x+y)/2, economic_resources, military_capability))
        #print (power)
        return (group_names, affinity, power)
    
    
    
    
    def net(self, group_names, affinity, power): 
        
        #create data in from csv assessment of group affinity
        
        
        #print (power)
        #create graph
        net = nx.Graph()
        
               
        #add nodes from tribe names
        net.add_nodes_from(group_names)
        
        #add affinity/ec resources and mil cap attributes to each node
        for group in group_names: 
            #print (net[group])
            net.node[group]["affinity"] = affinity[group_names.index(group)]
            #calculate power- need more elegant algorithm
            net.node[group]["power"] = power[(group_names.index(group))]
            
            #create empty list of potential alliances
            net.node[group]["maybe_mates"] = []
            net.node[group]['g_dis'] = 'False'
        
        return net
            
    def refdict(self, group_names, affinity, power):
        
        ref = {}
        for group in group_names: 
            ref[group] = {'affinity': 0, 'power': 0}
            ref[group]['affinity'] = affinity[group_names.index(group)]
            ref[group]['power'] = power[(group_names.index(group))]
            ref[group]['maybe_mates'] = []
            ref[group]['g_dis'] = 'False'
        return ref            
            
        #print (list(net.nodes(data=True)))
        
        
        

        