# Libya-CoalitionFormation
Code used for Journal of Policy and Complex Systems (Fall 2018). *INTEGRATING COMPUTATIONAL TOOLS INTO FOREIGN POLICY: INTRODUCING MESA PACKAGES WITH A COALITION ALGORITHM*  

Model is designed to assess the impact of foreign aid on the Libyan civil war. 

**To Run:** bilateralShapley.py runs the model. The "if __name__ == '__main__':" line 530 of the module runs the program. Output is saved to the
2 csv files inidicated in lines 557 and 558.  

**Change the Read In**
The read in file needs to be updated in the Group.py file  if the users wants to change from no aid to aid to one group to aid to three groups. (line 31)


# Read in Qualitative Assessment
The three csv files provide three different variations of group power within Libya. 

1. "Groups.csv": An assessment of group power based on a summer 2017 estimate. 
2. "Groups_Support_One.csv": The same assessment but with the Al-Ubaidat group receiving signiciant support. 
3. "Groups_Support_Many.csv": The same assessment with three groups receiving significant support.

# Groups.py
This module reads in the the csv data and develops a preference (ideological affinity) value for each group which is normalized over the inputs. It also reads in the economic and military values, normalizes them and averages them to greate a power value for each group

# bilateralShapley.py
This module conducts the bilateral shapley value algorithm to assess who the gorups will form coalitions bith with and without foreign support. These results are then saved in a csv file.  

# Results.ipynb
"Coalition Formation Chart and Graphs.ipynb" is a Jupyter Notebook file which reads in and anlayzes the results from the model runs. 


