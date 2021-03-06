# Libya-CoalitionFormation
Code used for Journal of Policy and Complex Systems (Fall 2018). *Integrating Computational Tools into Foreign Policy Analysis: Introducing Mesa Packages with a Coalition Algorithm*

Model is designed to assess the impact of foreign aid on the Libyan civil war. 

**To Run:**   
1. (recommended) set up a new environment
2. Clone or download
3. pip install -r requirements.txt
4. execute run.py module

**Change Inputs:**
If the users wants to change from no aid to aid to one group to aid to three groups change the tribal_input variable on line 23
User can also change the output file line 40 and 41.


## Read in Qualitative Assessment
The three csv files provide three different variations of group power within Libya. 

1. "Groups.csv": An assessment of group power based on a summer 2017 estimate. 
2. "Groups_Support_One.csv": The same assessment but with the Al-Ubaidat group receiving significant support. 
3. "Groups_Support_Many.csv": The same assessment with three groups receiving significant support.

## Groups.py
This module reads in the the csv data and develops a preference (ideological affinity) value for each group which is normalized over the inputs. It also reads in the economic and military values, normalizes them and averages them to greater a power value for each group

## bilateralShapley.py
This module conducts the bilateral Shapley value algorithm to assess who the groups will form coalitions both with and without foreign support. These results are then saved in a csv file.  

## Results.ipynb
"Coalition Formation Chart and Graphs.ipynb" is a Jupyter Notebook file which reads in and analyzes the results from the model runs. 


