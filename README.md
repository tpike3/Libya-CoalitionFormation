# Libya-CoalitionFormation
Code used for Journal of Policy and Complex Systems (Fall 2018)
Model is designed to assess the impact of foreign aid on the Libyan civil war. 

# Read in Qualitative Assessment
The three csv files provide three different variations of group power within Libya. An assessment of group power based on a summer 2017 estimate. The same assessment but with the Al-Ubaidat group receiving signiciant support. THe same assessment with three moderate groups receiving significant support.

**Change the Read In**
The read in file needs to be updated in the Group.py file if the users wants to change form no aid, to aid to one group, to aid to to groups: 


# Groups.py
This module reads in the the csv data and develops a preference (ideological affinity) value for each group which is normalized over the inputs. It also reads in the economic and military values, normalizes them and averages them to greate a power value for each group

# bilateralShapley.py
This module conducts the bilateral shapley value algorithm to assess who the gorups will form coalitions bith with and without foreign support. These results are then saved in a csv file.  


**To Run:** bilateralShapley.py runs the model. The "if __name__ == '__main__':" at the bottom of the module runs the program. Output is saved to the
2 csv files inidicated in this function. 