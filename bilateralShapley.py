# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 08:58:07 2017

@author: ymamo
"""

import Groups
import networkx as nx    
import matplotlib.pyplot as plt    
import copy  
import pandas as pd               
    
    
class Attachment(object): 
    
    '''
    Tasks:
        1. Establish two networks graphs based on agent attributes
        2. Execute Bilateral Shapely Value
        3. Output the data into a CSV

    Purpose: Pass in the agents and specificed attributes and run through
             the bilateral Shapely value
    '''

    def __init__(self, comp, efficiencies, t):
       
       # excute calss to read in tribes and attributes to graph for reference
       self.population = Groups.groups_est()
       #same as above however, this is the graph for manipulating
       
       #variable for grou with greatest number of allies
       self.most = 0
       # variable to determine if the gorups have coalesced
       self.coalesced = False
       #dicntionary to keep track of each sub networks graph
       self.subnets = {}
       
       self.comp = comp
       self.efficiencies = efficiencies
       self.run = t
          
    '''
      HELPER FUNCTIONS
      
      1. Make subnet - Allows for detailed look of each coalition
    '''
    
    def make_subnets(self, tribename, node1, node2, newpref):
        
        '''
        Tasks:
            1. Make network graph of each coalition
            2. Store each agents power and preference variables
        '''
        
        #empty list to track groups in subnetwork
        tribe_list = []
        # Get Tribe names out
        start = 0
        stop = 0
        #Iterate through name to look for periods and append to tribe lists involved
        for l in range(len(tribename)):
            if tribename[l] == '.':
                stop = l
                tribe = tribename[start: stop]
                tribe_list.append(tribe) 
                start = stop +1 
        # get last name
        tribe_list.append(tribename[start:])
        #print (tribename)
        #print (tribe_list)
                
        #check if both sub_network exists
        self.subnets[tribename] = nx.Graph()
        # add each node with attributes
        for each in tribe_list: 
            #calculate new preference
            diff = self.population.ref[each]['affinity'] +((newpref - self.population.ref[each]['affinity'])*self.comp)
            self.subnets[tribename].add_node(each)
            self.subnets[tribename].node[each]['affinity'] = diff
            #self.population.ref[each]['affinity'] = diff
            #update reference dictionary with new afifnity value based on alliances
            self.subnets[tribename].node[each]['power'] = self.population.ref[each]['power']
            self.subnets[tribename].node[each]['maybe_mates'] = self.population.ref[each]['maybe_mates']
            self.subnets[tribename].node[each]['g_dis']= self.population.ref[each]['g_dis']
                
        if node1 in self.subnets.keys():
            self.subnets.pop(node1)
        if node2 in self.subnets.keys():
            self.subnets.pop(node2)
            
    def output(self, comp, efficiencies, t):
      
       '''
       Tasks: 
           1. Create lists to caputre values
           2. Seperate Groups which coalesced and those which did not
           3. Place in a dtaframe for easy saving to csv
       '''
        
       r = ["NEW RUN"]
       c =["NEW RUN"]
       eff = ["NEW RUN"]
       names = ["NEW RUN"]
       power = ["NEW RUN"]
       aff = ["NEW RUN"]
       g_dis = ["NEW RUN"]
       for name,graph in self.subnets.items(): 
           r.append(t)
           c.append(comp)
           eff.append(efficiencies)
           names.append(name)
           power.append(self.population.groups.node[name]['power'])
           aff.append(self.population.groups.node[name]['affinity'])
           g_dis.append(self.population.groups.node[name]['g_dis'])
           for node in list(graph.nodes(data=True)):
               c.append(comp)
               eff.append(efficiencies)
               names.append(node[0])
               power.append(node[1]['power'])
               aff.append(node[1]['affinity'])
               g_dis.append(node[1]['g_dis'])
           
           r.append('\n')
           c.append('\n')
           eff.append('\n')
           names.append('\n')
           power.append('\n')
           aff.append('\n')
           g_dis.append('\n')
       
       r.append('NON ALLY')
       c.append('NON ALLY')
       eff.append('NON ALLY') 
       names.append('NON ALLY')
       power.append('NON ALLY')
       aff.append('NON ALLY')
       g_dis.append('NON ALLY')         
       for n in list(self.population.groups.nodes()):
           if n not in names: 
               r.append(t)
               c.append(comp)
               eff.append(efficiencies)
               names.append(n)
               power.append(self.population.groups.node[n]['power'])
               aff.append(self.population.groups.node[n]['affinity'])
               g_dis.append(self.population.groups.node[n]['g_dis'])
           
        
       output = pd.DataFrame({"Run": t, "Compromise": c, "Efficiency": eff, "Groups" : names, "Power" : power, "Affinity": aff})
       
       return output
                    
    def out2(self, comp, efficiencies,t):
        '''
        Save subnetwroks for analysis
        '''
        
        run = ["NEW RUN"]
        c = ["NEW RUN"]
        eff = ["NEW RUN"]
        names = ["NEW RUN"]
        power = ["NEW RUN"]
        for node in list(self.population.groups.nodes(data=True)):
               c.append(comp)
               eff.append(efficiencies)
               names.append(node[0])
               power.append(node[1]['power'])
        output = pd.DataFrame({"Run" : t, "Compromise": c, "Efficieny": eff, "Groups" : names, "Power" : power,})
        
        return output
    
    '''
    MAIN FUNCTIONS

    1. assess_coalitions: determines best matches for every agent
    2. make_alliance: find best option based on
    all the combinations and form link
    3. new_node: create new nodes form aligned
    agents and remove them as a stand alon agent
    '''
    
    
    def assess_coalitions(self, network):
       '''
           Tasks:
               1. As a node iterate through each node 
               2. assess the expected utility of a coalition formation
               3. find the best possible match 
               4. store as an attirbute of the node
           
           Purpose: To look over all combinations and find the best alliance
           
       '''
               
       #iterate over graph and create links with those most like you
       for n1,d1 in network.nodes(data=True): #self.population.groups.nodes(data =True):
           
           #reset maybe_mates for each round of coalition formation
           d1["maybe_mates"] = []
           
           #iterate over nodes to find allies
           for n2,d2 in network.nodes(data=True): #self.population.groups.nodes(data =True): 
               #ensure nodes does not link to self
               if n1 != n2:
                   #determine expected utility of alliance
                   # * 1.10 is an marignal gain based on benefits form alliance - think economy of scale
                   #second half (1 - (abs(d1...) based on SEMPro -Zining, Abdollohian...) 
                   #print (n1, d1, n2, d2)
                   pot_eu = (((d1['power'] +d2['power'])))
                   #print (pot_eu)
                   #determine bilateral shapely value for both agents
                   shape1 = 0.5*d1['power'] + 0.5*(pot_eu -(d2['power']))
                   shape2 = 0.5 *d2['power'] + 0.5*(pot_eu - (d1['power']))
                   #print ("shape1:" , shape1)
                   #print ("u(1):", d1['power'])
                   #ensure no alliance is made which result in a decrease in either parties utility
                   
                   if shape1 > d1['power'] and shape2 > d2['power']: 
                                              
                       #if a coalition increases both expected utilities then add to list of node1
                       d1['maybe_mates'].append([shape1, n2, pot_eu])
        
           #sort list of possible alliances for one with highest shapely value
           d1['maybe_mates'].sort(key=lambda x: x[0], reverse = True)
           if len(d1['maybe_mates']) > self.most:
               self.most = len(d1['maybe_mates'])
               
           #append index number (i.e. rank) of each tribe to list
           for each in d1['maybe_mates']:
               each.append(d1['maybe_mates'].index(each))
             
       #print (ally)
           
    
    def make_alliance(self, network, level): 
        '''
            Tasks: 
                1. iterate through each possible alliance  increasing index value (poss variable)
                2. if best bet form link
        
            Purpose: A computationally efificent way to find best link for each node
        '''
        
        #empty list to keep track of nodes with edges (eaiser than networkx data structure)
        allied = []        
        #iterate through nodes
        poss = 1
        #keep creating links while value is shortet then the greatest number of possible alliances
        #self.most variable
        while poss < self.most: 
            # iterate through nodes
            for each in network.nodes(data=True): #self.population.groups.nodes(data=True):
                #if in allied list pass (already has an edge)
                if each[0] in allied: 
                    pass
                #look at data of potential allies
                else: 
                    # iterate through possible mates 1 index is name
                    for e in each[1]['maybe_mates']:
                        # see if index value (e[3]) is less than current index being examined (poss value)
                        if e[3] <= poss:
                            # ensure node isnot already allied
                            if e[1] not in allied and each[0] not in allied: 
                                #print (self.population.groups.node[e[1]]['maybe_mates'])
                                # iterate through possible mates
                                for i in network.node[e[1]]["maybe_mates"]: 
                                    #print (i[1])
                                    #see if node is a possible mate
                                    if i[1] == each[0]: 
                                        #print ("True")
                                        # ensure it is less than current value to make bestt alliance
                                        if network.node[e[1]]['maybe_mates'].index(i)<= poss:
                                            #if level == 'two':
                                            #    print ("Level 2 edge")
                                            #print (type(each[0]))
                                            #print (type(e[1]))
                                            #make alliance
                                            network.add_edge(each[0], e[1])
                                            #add both nodes to list
                                            allied.append(each[0])
                                            allied.append(e[1])
            #increase  value of poss to explore next best option for remaining nodes
            poss += 1
        if level == 'two':
            self.coalesced = True 
        
        #if no more alliances are made change variable to stop 
        if len(allied) == 0:
            self.coalesced = True
                    #print (e)#find best possible alliance
        #print (c)
        #print (len(allied), allied)
        
        #print (self.population.groups.nodes())
    
    def new_node(self, network):
        '''
        Tasks:
            1. Calculate new agents based on those
            agents who established a link
            2. Form subnet of agents based on agents who joined
            3. Remove individuals agents form network
            who are not part of coalition

        Purpose: Create heirarchies of networks
        '''
        #iterate through each group which has an edge and put in list
        new_nodes = []
        new_pows = []
        new_prefs = []
        g_dis = []
        for one,two in network.edges(): #self.population.groups.edges():
            #use aggressive caching
            
            prefA = network.node[one]['affinity'] #self.population.groups.node[one]['affinity']
            prefB = network.node[two]['affinity'] #self.population.groups.node[two]['affinity']
            powA = network.node[one]['power'] #self.population.groups.node[one]['power']
            powB = network.node[two]['power'] #self.population.groups.node[two]['power']
            #calculate new preference
            newpref = ((prefA *powA) + (prefB * powB))/(powA + powB)
            new_prefs.append(newpref)
            
            
            #calculate new power
            newpow = (powA + powB) * self.efficiencies
            new_pows.append(newpow)
            #new node name         
            new_nodes.append([one, two])
    
        #iterate through list of alliances 
        for i in new_nodes: 
            #print (i)
            #combine goroup names into a new name
            newname = i[0] + "." + i[1]
            #print (newname)
            #get index of item
            idx = new_nodes.index(i)
            #add the new combined node
            network.add_node(newname)
            #add new power attribute
            network.node[newname]['power']= new_pows[idx]
            #add new affinity attributes
            network.node[newname]['affinity']= new_prefs[idx]
            #create empy possible mates key
            network.node[newname]['maybe_mates'] = []
            network.node[newname]['g_dis'] = 'False'
            
            #make new subnetwork
            self.make_subnets(newname, i[0], i[1], new_prefs[idx])            
        
            
            #self.population.groups
            network.remove_node(i[0])
            #self.population.groups
            network.remove_node(i[1])
            
            
        
            #print (newpref, newpow, newname)
            #print (one, two)
    
    def check_alliances(self, subs, nets):
         
         '''
         Tasks:
             1. Determine if any memeber of a coalition wants to leave
             2. Remove from coalition and add back into population

         Purpose: Ensure each agent in the colation still wants to belong
         '''
        
         dis = []
         keys = []
         c = 0
         for key, sub in subs.items():
             for group in sub.nodes(data = True):
                 #print (nets.node[key]['power'])
                 #print (list(sub.nodes()), group[0])
                 pot_eu = (((nets.node[key]['power'] +group[1]['power'])))
                 #print (pot_eu)
                 #determine bilateral shapely value for both agents
                 shape1 = 0.5*nets.node[key]['power'] + 0.5*(pot_eu -(group[1]['power']))
                 shape2 = 0.5*group[1]['power'] + 0.5*(pot_eu - nets.node[key]['power'])
                 
                 
                 if shape1 < nets.node[key]['power'] or shape2 < group[1]['power']:
                     #print ("shape1:", shape1, node[key['power']])
                     first = group[0] + "."
                     mid = "." + group[0] + "."
                     end = "." + group[0]
                     if mid in key: 
                         dis.append([group[0], mid, key])
                     
                     elif first in key:
                         dis.append([group[0],first, key])    
                                                               
                     elif end in key:
                         dis.append([group[0], end, key])                     
                   
                     group[1]['g_dis'] = 'True'
                     #print (shape2, pot_eu, nets.node[key]['power'], group[1]['power'])
                     #print ('True')
                     c += 1
        
         for item in dis: 
             #print (list(subs[item[2]].nodes(data = True)), subs[item[2]].node[item[1]])
             #remove node from subnet
             subs[item[2]].remove_node(item[0])
             #print (item[0])
             nets.add_node(item[0])
             nets.node[item[0]]['power'] = self.population.ref[item[0]]['power']
             nets.node[item[0]]['affinity'] = self.population.ref[item[0]]['affinity']
             nets.node[item[0]]['maybe_mates'] = []
             nets.node[item[0]]['g_dis'] = "True"
         # create_new key
         
         empty_nets = []
         for key, graph in subs.items():
             nodes = list(graph.nodes())
             if len(nodes) == 0: 
                empty_nets.append(key)
         
         #print (empty_nets)   
         for g in empty_nets: 
             del subs[g]
             nets.remove_node(g)
         
         for key, graph in subs.items():
             nodes = list(graph.nodes(data=True))
             new_key = ""
             pow = 0
             aff = []
             for n in nodes: 
                 if nodes.index(n) != (len(nodes) -1):
                     new_key = new_key + n[0] + '.'
                 else: 
                     new_key = new_key + n[0]
                 pow += n[1]['power']
                 aff.append([(n[1]['affinity']*n[1]['power']), n[1]['power']])
                 #calculatenew affinity (long way)
                 aff_top = 0
                 aff_bot = 0
                 for a in aff: 
                    aff_top += a[0]
                    aff_bot += a[1]
                    
             subs[new_key] = subs.pop(key)
             nets.remove_node(key)
             nets.add_node(new_key)
             nets.node[new_key]['power'] = pow * self.efficiencies
             nets.node[new_key]['affinity'] = aff_top/aff_bot
             nets.node[new_key]['maybe_mates'] = []
             nets.node[new_key]['g_dis'] = False
        
        
             
         #print ("subnets")
         #print (subs.keys())
         #print ()
        
        #keys.append([key, new_key])
        
             
         #print (dis, c)
    
    
    
    
    
    def execution(self):
       
       '''
        Tasks:
            1. Run three main functions to form alliance
            2. After colaitions form, see if agents still want to be in group
            3. Store results

        Purpose: Run algorithm and store results
       '''
        
       while self.coalesced == False: 
           self.assess_coalitions(self.population.groups)
           self.make_alliance(self.population.groups, 'one')
           self.new_node(self.population.groups)
           # For future uses when nnodes make alliances with exogenous additions
           
           #print (len(list(self.population.groups.nodes())))
           #print (len(self.subnets))
       #output = pd.DataFrame(columns)
       
       for each in self.subnets.items():
           self.coalesced = False
           #print (each)
           while self.coalesced == False:
               self.assess_coalitions(each[1])
               self.make_alliance(each[1], 'two')
       self.check_alliances(self.subnets, self.population.groups)
           #for node in each[1].nodes(data=True):
               #print (node)
               #for item in node[1]["maybe_mates"]:
                   #print (item)
                  # each[1].add_edge(node[0], item[1])
               
           #print (each[0])
           #nx.draw(each[1])
           #plt.show()
           #plt.clf()
       
       return self.output(self.comp, self.efficiencies, self.run),self.out2(self.comp, self.efficiencies, self.run)
       
       
                
       
    
if __name__ == '__main__':
    
    '''
    initiates model over parameters 
    '''
    
    tribes = []
    results = []
    comps = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.00]
    eff  = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 3, 4, 5, 6, 7]
    #comps = [.96]
    #eff = [4]
    
    t = 0
    for x in comps:
        for y in eff: 
            test = Attachment(x,y,t)
            res, tris = test.execution()
            results.append(res)
            tribes.append(tris)
            t += 1
            print (t)
            plt.clf()
            nx.draw(test.population.groups)
            plt.show()
    out = pd.concat(results, ignore_index= True)
    out2 = pd.concat(tribes, ignore_index=True)
    out.to_csv( "allianceresults_readjusted-no params" + '.csv', encoding = 'utf-8')
    out2.to_csv("alliancetribes_redjusted__no params" + ".csv", encoding = 'utf-8')
    
    
           
    