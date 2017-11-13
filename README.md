# Libya-CoalitionFormation
Code for paper submitted to Spring Sim 2017
Model is designed to assess the impact of foreign aid on the LIbyan civil war. 

# Read in Qualitative Assessment
The three csv files provide three different variations of group power within Libya. An assessment of group power based on a summer 2017 estimate. The same assessment but with the Al-Ubaidat group receiving signiciant support. THe same assessment with three moderate groups receiving significant support.

# Groups.py
This module reads in the the csv data and develops a preference (ideological affinity) value for each group which is normalized over the inputs. It also reads in the economic and military values, normalizes them and averages them to greate a power value for each group

# bilateralShapley.py
This module conducts the bilateral shapley value algorithm to assess hwo the gorups will form coalitions bith with and without foreign support. These results are then saved in a csv file.  
